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
  
  We compared 4 classification machine learning models and used hyperparameter tuning, cross validation, and feature selection to find the best performing model based on scores. Our final model performed well on an unseen test data set, with a precision score of 0.760, a recall score of 0.954, and a F1 score of 0.847. On the 790 test cases, it correctly predicted 581 cases (accuracy of 73.5%).  We hope that our analysis can provide insights to ramen lovers and general consumers during their purchases in stores and help ramen companies decide their marketing strategies to increase sales.

## Report
The final report can be found here: [Report](https://github.com/PANDASANG1231/522_Ramen/blob/main/doc/ramen_ratings_report.html)

## Usage

We use python in this project and the workflow and orders of using scripts is as below:
![avatar](workflow.png)
### With Docker
You can run the pipeline with:
>To be added

### Without Docker
To reproduce the analysis without using Docker, clone this GitHub repository, install the [dependencies](#dependencies) listed below, and run the following command at the command line/terminal from the root directory of this project:

```
make all
```

To revert to a clean state and redo all the analysis, run the following command at the command line/terminal from the root directory of this project:

```
make clean
```

## Dependencies

The dependencies is listed in the environment.yaml, which you can find [here](https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/environment.yaml).

 - ipykernel
  - matplotlib>=3.2.2
  - scikit-learn>=1.0
  - pandas>=1.3.*
  - requests>=2.24.0
  - altair_saver
  - vega_datasets
  - graphviz
  - python-graphviz
  - jinja2y
  - pip
  - py-xgboost==1.3.0
  - spacy
  - wikipedia
  - nltk
  - imbalanced-learn
  - pandas-profiling
  - ipywidgets
  - docopt
  - pycountry
  - wordcloud
  - geopandas
  - openpyxl
  - pip:
    - boruta=0.3
    - seaborn=0.11.2
    - shap-0.4.0.0
    - catboost=1.0.3
    - mglearn
    - psutil>=5.7.2
    - rpy2

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
