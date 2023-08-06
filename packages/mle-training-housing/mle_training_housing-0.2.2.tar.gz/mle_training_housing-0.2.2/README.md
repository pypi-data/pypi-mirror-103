# Median housing value prediction

The housing data can be downloaded from https://raw.githubusercontent.com/ageron/handson-ml/master/. The script has codes to download the data. We have modelled the median house value on given housing data. The framework has been uploaded as a package in PyPi (https://pypi.org/project/mle-training-housing/0.1.1/). It can be installed using pip. 

The following techniques have been used: 

 - Linear regression
 - Decision Tree
 - Random Forest

## Steps performed
 - We prepare and clean the data. We check and impute for missing values.
 - Features are generated and the data set is split into train and test.
 - All the above said modelling techniques are tried and evaluated. The final metric used to evaluate is mean squared error.

## To excute the script
pip install mle-training-housing

pull_data -Folder housing_run1

train_model -Folder housing_run1

score_test -Folder housing_run1

