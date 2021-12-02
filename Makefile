# Makefile
# Allyson Stoll, Dec 2021

# This Makefile completes data download and preprocessing
# prior to EDA and model building of a ramen rating model 
# based on ramen ratings from The Ramen Rater.

# Example usage:
# make data/raw/ramen_ratings.csv

#make all dependencies
all : doc/Report.html

# download the dataset from The Ramen Rater website
data/raw/ramen_ratings.csv : src/download_data.py
	python3.9 src/download_data.py --url="https://www.theramenrater.com/wp-content/uploads/2021/09/The-Big-List-All-reviews-up-to-3950.xlsx" \
	--out_file="data/raw/ramen_ratings.csv"

# split the dataset
data/process/train_df.csv data/process/test_df.csv : data/raw/ramen_ratings.csv src/split.py
	python3.9 src/split.py --path="data/raw/ramen_ratings.csv" --out_file_train="data/process/train_df.csv" \
	--out_file_test="data/process/test_df.csv"

# add country codes to the dataset
data/process/train_codes_df.csv : data/process/train_df.csv src/get_countrycode_data.py
	python3.9 src/get_countrycode_data.py --path="data/process/train_df.csv" \
	--out_file="data/eda/train_codes_df.csv"

# complete EDA figures
results/figures/stars_histogram.png results/figures/type_histogram.png \
results/figures/variety_wordcloud.png results/figures/ramen_map.png : data/eda/train_codes_df.csv src/generate_EDA_figures.py
	python3.9 src/generate_EDA_figures.py --path="data/eda/train_codes_df.csv" --out_path="results/figures/"

# preprocess data for modeling
data/process/train_process.csv data/process/test_process.csv : \
data/process/train_df.csv data/process/test_df.csv src/preprocess.py
	python3.9 src/preprocess.py --train_path="data/process/train_df.csv" --test_path="data/process/test_df.csv" \
	--out_file_train="data/process/train_process.csv" --out_file_test="data/process/test_process.csv"

# create model and supporting figures
results/best_model.pkl results/train_metrics.jpg results/Top_20_Good_features.csv results/Top_20_Bad_features.csv : \
data/process/train_process.csv src/train_model.py
	python3.9 src/train_model.py --train_file="data/process/train_process.csv" --out_file_train="results/best_model.pkl" \
	--out_file_result="results/"

# test model predictions
results/prediction/prediction.csv results/test_metrics.jpg : data/process/test_process.csv results/best_model.pkl src/predict.py
	python3.9 src/predict.py --test_file="data/process/test_process.csv" --model_file="results/best_model.pkl" \
	--out_file_result="results/prediction/"

# write the report
doc/Report.html : results/prediction/prediction.csv results/test_metrics.jpg \
results/figures/stars_histogram.png results/figures/type_histogram.png \
results/figures/variety_wordcloud.png results/figures/ramen_map.png
	Rscript -e "rmarkdown::render('doc/Report.Rmd')"

clean :
	rm -rf data/raw/ramen_ratings.csv
	rm -rf data/process/train_df.csv
	rm -rf data/process/test_df.csv
	rm -rf data/process/train_codes_df.csv 
	rm -rf results/figures/stars_histogram.png
	rm -rf results/figures/type_histogram.png
	rm -rf results/figures/variety_wordcloud.png
	rm -rf results/figures/ramen_map.png
	rm -rf data/process/train_process.csv
	rm -rf data/process/test_process.csv
	rm -rf results/best_model.pkl
	rm -rf results/train_metrics.jpg
	rm -rf results/Top_20_Good_features.csv
	rm -rf results/Top_20_Bad_features.csv
	rm -rf results/prediction/prediction.csv
	rm -rf results/test_metrics.jpg