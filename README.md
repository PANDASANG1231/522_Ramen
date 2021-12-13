# Ramen Ratings Prediction

**Contributors:**

This is a class project for DSCI 522 (Data Science Workflows), a course in the Master of Data Science program at the University of British Columbia.

  - Allyson Stoll
  - Irene Yan
  - Wenjia Zhu
  - Xiaohan Chen

## About
  How can we know an instant noodle, aka Ramen, tastes good or not before tasting it? Will the brand matter? Does a cup noodle always taste better than a pack one?

  As ramen buyers, we are interested in figuring out what features are important in finding a good ramen and how we can use these features to predict whether a pack of ramen is good or bad. We used a data set with 3950 reviews on all kinds of instant noodles to carry out the analysis. Our target is a binary variable indicating whether the product is good or bad and we aim to classify a ramen based on its features.
  
  We compared 4 classification machine learning models and used hyperparameter tuning, cross validation, and feature selection to find the best performing model based on precision, recall, and F1 scores. Our final model performed well on an unseen test data set, with a precision score of 0.760, a recall score of 0.954, and a F1 score of 0.847. On the 790 test cases, it correctly predicted 581 cases (accuracy of 73.5%).  We hope that our analysis can provide insights to ramen lovers and general consumers during their purchases in stores and help ramen companies decide their marketing strategies to increase sales.

## Report
The final report can be found here: [Report](https://github.com/PANDASANG1231/522_Ramen/blob/main/doc/ramen_ratings_report.html)

## Usage

**Note for TA: that the code needs to run about 2-5 minutes.**
We use python in this project and the workflow and orders of using scripts is as below:
![avatar](workflow.png)

### With Docker

To reproduce the analysis using Docker, first install [Docker](https://www.docker.com/get-started). Then clone this GitHub
repository and run the following command at the command line/terminal
from the root directory of this project:

```
docker run --rm -v $PWD:/home/522ramen/ zwj63518583/dockerfile make -C '/home/522ramen' all
```

To revert to a clean state and redo all the analysis, run the following command at the command line/terminal from the root directory of this project:

```
docker run --rm -v $PWD:/home/522ramen/ zwj63518583/dockerfile make -C '/home/522ramen' clean
```

### Without Docker
To reproduce the analysis without using Docker, clone this GitHub repository, install the [dependencies](#dependencies) listed below, and run the following command at the command line/terminal from the root directory of this project:

<img src="https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/Makefile.png" height="200px">

```
make all
```

To revert to a clean state and redo all the analysis, run the following command at the command line/terminal from the root directory of this project:

```
make clean
```

## Dependencies

The dependencies is listed in the environment.yaml, which you can find [here](https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/environment.yaml).

  - System Packages
    - r-base
    - pandoc
    - pandoc-citeproc

  - Python Packages 
    - matplotlib=3.5.0
    - pandas=1.3.4
    - requests=2.26.0
    - scikit-learn=1.0.1
    - vega_datasets=0.7.0
    - jinja2=3.0.2
    - lightgbm=3.2.1
    - py-xgboost=1.5.0
    - catboost=0.26.1
    - spacy=2.3.5
    - nltk=3.6.5
    - shap=0.39.0
    - seaborn=0.11.2
    - pandas-profiling=2.9.0
    - ipywidgets=7.6.5
    - docopt=0.6.2
    - openpyxl=3.0.9
    - graphviz==0.19
    - altair_saver==0.5.0
    - wikipedia==1.4.0
    - eli5==0.11.0
    - imbalanced-learn==0.8.1
    - pycountry==20.7.3
    - wordcloud==1.8.1
    - geopandas==0.10.2
    - boruta==0.3
    - mglearn==0.1.9
    - rpy2==3.4.5

  - R Packages
    - install.packages('knitr')
    - install.packages('dplyr')
    - install.packages('rmarkdown')

## License

The source code for the site is licensed under the MIT license, which you can find [here](https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/LICENSE).

## References

<div id="refs" class="references hanging-indent">

<div id="ref-Dua2019">

The data set was most recently updated on September 22nd, 2021 with 3950 reviews.
All the reviews are based on the personal preference of the author and are not based on sales or popularity. The rating scores are in .25 increments – rounding is NOT recommended. You may think of it as a letter grading; a 3.5 score out of 5 stars is equivalent to (3.5 * 2) * 10 = 70 = C.
 <https://www.theramenrater.com/wp-content/uploads/2021/09/The-Big-List-All-reviews-up-to-3950.xlsx>.
</div>

</div>
