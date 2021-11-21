# Ramen Star Prediction

**Contributors:**

This is a project for MDS 522 Group6.

  - Allyson Stoll
  - Irene Yan
  - Wenjia Zhu
  - Xiaohan Chen

## About

We will use the StandardScaler(), CountVector() and other method to transform the data and build a linear regression model which can predict a Ramen restaurant's star based on its brand, variety,style, countries and other indicators. And we can also get some conclusions like What ingredients or flavors are most commonly advertised on ramen package labels? in this process. The star scales from 0 to 5, representing how tasty the Ramen will be. This question may not be of the world-changing kind, but it is a good start of figuring out a result in real-life problems with data science for us. Considering the usefulness of this model for food lovers around the world when choosing nearby ramen restaurants, we think this is a very interesting and meaningful question.

### Dataset
The dataset we used in this project is downloaded from [kaggle](https://www.kaggle.com/residentmario/ramen-ratings), created by the data analysist called Aleksey Bilogur.  Each record in the dataset is a single ramen product review. It is updated as of September 22nd, 2021. Current as of review #3950.
reviews are based on personal preferences, not on sales of popularity.
Scores are in .25 increments – rounding is NOT recommended. Think of letter
grading; a 3.5 score out of 5 stars – (3.5 * 2) * 10 = 70 = C.


## Report

## Usage

Using python:

```
Usage: src/download_data.py --url=<url> --out_file=<out_file>
Options:
--url=<url>              URL from where to download the data (must be in standard xlsx format)
--out_file=<out_file>    Path (including filename) of where to locally write the file
```

## Dependencies

The dependencies is listed in the environment.yaml, which you can find [here](https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/environment.yaml).

## License

The source code for the site is licensed under the MIT license, which you can find [here](https://raw.githubusercontent.com/PANDASANG1231/522_Ramen/main/LICENSE).

## References

<div id="refs" class="references hanging-indent">

<div id="ref-Dua2019">

Updated as of September 22nd, 2021. Current as of review #3950.
reviews are based on personal preferences, not on sales of popularity.
Scores are in .25 increments – rounding is NOT recommended. Think of letter
grading; a 3.5 score out of 5 stars – (3.5 * 2) * 10 = 70 = C.
 <https://www.theramenrater.com/resources-2/the-list/>.
</div>

<div id="ref-Streetetal">

Ramen (ラーメン) is a noodle soup dish that was originally imported from China
 and has become one of the most popular dishes in Japan in recent decades.
Ramen are inexpensive and widely available, two factors that also make them 
an ideal option for budget travelers. Ramen restaurants, or ramen-ya, can 
be found in virtually every corner of the country and produce countless regional 
variations of this common noodle dish.
<https://www.japan-guide.com/e/e2042.html>.
</div>
</div>