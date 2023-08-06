from mle_training_housing.utils import *


def main():
    """ 
    Feature generation and model training is done in the function. 
    The function can be invoked from Command Line Interface (CLI).

    CLI Syntax : **train_model -Folder <user_input>**

    *(Folder is an optional parameter. Default value is 'housing_run_v1'.)*

    Inputs required :
    
    - /<user_input>/model/input/train_data.csv    
    - /<user_input>/model/input/test_data.csv

    Outputs :

    - /<user_input>/model/pickle/pickle.p

    Raises
    ------
    FileNotFoundError
        If the train_data.csv is not available in the model/input folder. 
    """
    logger = configure_logger()
    logger.info("Model Training is started.")

    housing_path_final = HOUSING_PATH
    model_dump_final = MODEL_DUMP_PATH
    model_input_path_final = MODEL_INPUT_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument("-Folder", nargs="?", help="Mention the folder to load the files.")
    args = parser.parse_args()
    if args.Folder:
        # print(args.Path)
        logger.info("User argument is specified. The files will be saved in the user specified folder.")
        model_dump_final = os.path.join(args.Folder, "data/model", "pickle")
        model_input_path_final = os.path.join(args.Folder, "data/model", "input")
    else:
        logger.info("User argument is not specified. The files will be saved in the default folder.")

    try:
        housing = read_data("housing.csv", housing_path_final)
    # housing = load_housing_data(housing_path_final)
    except:
        raise FileNotFoundError("housing.csv is not present in the " + model_input_path_final + ". Please create and try again.")
        sys.exit(1)

    housing["income_cat"] = pd.cut(housing["median_income"], bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf], labels=[1, 2, 3, 4, 5],)

    rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

    class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
        def __init__(self, add_bedrooms_per_room=True):  # no *args or **kargs
            self.add_bedrooms_per_room = add_bedrooms_per_room

        def fit(self, X, y=None):
            return self  # nothing else to do

        def transform(self, X):
            rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
            population_per_household = X[:, population_ix] / X[:, households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
                return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]

            else:
                return np.c_[X, rooms_per_household, population_per_household]

    attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
    housing_extra_attribs = attr_adder.transform(housing.values)

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]

    save_data(strat_train_set, "train_data.csv", model_input_path_final)
    save_data(strat_test_set, "test_data.csv", model_input_path_final)

    logger.info("Train and test data are created and saved in the below path - " + model_input_path_final)

    try:
        train_data = read_data("train_data.csv", model_input_path_final)
    except:
        raise FileNotFoundError("train_data.csv is not present in the " + model_input_path_final + ". Please create and try again.")
        sys.exit(1)

    # Model Pipeline Steps
    # Getting the numerical and categorical variables
    numeric_features = [col for col in housing.columns if col not in ["ocean_proximity", "median_house_value"]]
    numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])

    categorical_features = ["ocean_proximity"]
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    # Creating column transformer function (pre-processing) for the sklearn pipeline
    preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, numeric_features), ("cat", categorical_transformer, categorical_features)])

    # Creating a sklearn pipeline (Model used - RandomForestRegressor)
    rfr = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", RandomForestRegressor(random_state=42)),])

    # Separating the dependent and independent data from train data
    y_train = train_data["median_house_value"].copy().to_frame()
    features = [col for col in train_data.columns if col != "median_house_value"]
    X_train = train_data[features].copy()

    # Mentioning the grid search parameters for RF model
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {"regressor__n_estimators": [3, 10, 30], "regressor__max_features": [2, 4, 6, 8],},
        # then try 6 (2×3) combinations with bootstrap set as False
        {"regressor__bootstrap": [False], "regressor__n_estimators": [3, 10], "regressor__max_features": [2, 3, 4],},
    ]

    grid = GridSearchCV(rfr, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True,)

    # Model fitting and scoring

    grid.fit(X_train, y_train.values.ravel())
    print("Best estimator:\n{}".format(grid.best_estimator_))
    # print("model score: %.3f" % lin.score(X_train, y_train))

    final_model = grid.best_estimator_
    # print(type(final_model))
    save_model_pickle(final_model, model_dump_final)

    logger.info("The model is trained using the training data and the model pickle file is stored in the path - " + model_dump_final)
