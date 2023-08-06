from mle_training_housing.utils import *

# housing_url - Path where the data resides.
# housing_path - Path where the data should be saved.


def main():
    """ 
    Pulls the raw data and creates train and test data.
    The function can be invoked from Command Line Interface (CLI).
    
    CLI Syntax : **pull_data -Folder <user_input>**

    *(Folder is an optional parameter. Default value is 'housing_run_v1'.)*

    Output Files created :

    - /<user_input>/data/raw/housing/housing.csv
    - /<user_input>/data/model/input/train_data.csv
    - /<user_input>/data/model/input/test_data.csv
    """
    logger = configure_logger()

    logger.info("Data pull is started.")

    housing_path_final = HOUSING_PATH
    model_input_path_final = MODEL_INPUT_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument("-Folder", nargs="?", help="Mention the folder to load the files.")
    args = parser.parse_args()
    if args.Folder:
        # print(args.Path)
        logger.info("User argument is specified. The files will be saved in the user specified folder.")
        housing_path_final = os.path.join(args.Folder, "data/raw", "housing")
        model_input_path_final = os.path.join(args.Folder, "data/model", "input")
    else:
        logger.info("User argument is not specified. The files will be saved in the default folder.")

    fetch_housing_data(HOUSING_URL, housing_path_final)

    logger.info("Raw Data is pulled and saved in the path - " + housing_path_final)

