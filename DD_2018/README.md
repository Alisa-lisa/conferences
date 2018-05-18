# Devdays: https://devdays.lt/

## Data used in the show-cases:
1. https://www.kaggle.com/mnavas/taxi-routes-for-mexico-city-and-quito/data
(uio_clean.csv)
2. csv files for the classification case consists of a synthesized data and do not contain any personal value


## Usage on a local machine:
1. start pyspark/jupyter: 
``` docker run -it --rm -p 8888:8888 jupyter/pyspark-notebook```
2. create folder `data/`
#### Regression example:
1. the csv file uio_clean.csv under `/data/raw.csv` name
2. upload ipynb files
#### Classification case
1. upload `training_set.csv` and `test_set.csv` into `data/`
2. upload `example_config.json` into same old `data/` folder
3. upload ipynb file

## Resources used directly/indirectly:
1. Coursera courses from Andrew Ng
2. "Applied Predictive Modeling" by Max Kuhn, Kjell Johnson
3. https://machinelearningmastery.com/discover-feature-engineering-how-to-engineer-features-and-how-to-get-good-at-it/
4. https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf
5. https://elitedatascience.com/feature-engineering-best-practices
6. "Machine Learning: The Art and Science" by Peter Flach

