FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get install r-base r-base-dev -y

RUN conda install matplotlib=3.5.0 -y
RUN conda install pandas=1.3.4 -y
RUN conda install requests=2.26.0 -y
RUN conda install scikit-learn=1.0.1 -y
RUN conda install vega_datasets=0.7.0 -y
RUN conda install jinja2=3.0.2 -y
RUN conda install lightgbm=3.2.1 -y
RUN conda install py-xgboost=1.5.0 -y
RUN conda install catboost=0.26.1 -y
RUN conda install spacy=2.3.5 -y
RUN conda install nltk=3.6.5 -y
RUN conda install shap=0.39.0 -y
RUN conda install seaborn=0.11.2 -y
RUN conda install pandas-profiling=2.9.0 -y
RUN conda install ipywidgets=7.6.5 -y
RUN conda install docopt=0.6.2 -y
RUN conda install openpyxl=3.0.9 -y

RUN pip install graphviz==0.19
RUN pip install altair_saver==0.5.0
RUN pip install wikipedia==1.4.0
RUN pip install eli5==0.11.0
RUN pip install imbalanced-learn==0.8.1
RUN pip install pycountry==20.7.3
RUN pip install wordcloud==1.8.1
RUN pip install geopandas==0.10.2
RUN pip install boruta==0.3
RUN pip install mglearn==0.1.9
RUN pip install rpy2==3.4.5

RUN Rscript -e "install.packages('knitr')"
RUN Rscript -e "install.packages('tidyverse')"
Run Rscript -e "install.packages('rmarkdown')"