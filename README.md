# Apache SpamAssassin Email Spam Classifier

A binary classification project that detects spam emails under class imbalance.

## Problem Statement

Given an email, predict whether it is Spam (Positive Class) or Ham (Negative Class). The dataset is moderately imbalanced containing only 26.02% Spam instances. Thus, this project has an special emphasis on precision, recall, F1 score and PR-AUC.

## Dataset

- Source: [Spam Assassin Dataset](https://spamassassin.apache.org/old/publiccorpus/)
- Total emails: 10745 emails (containing 1580 duplicates)

## Project Structure

```
Spam Classifier/
├── 01_initial_eda.ipynb              # Data Loading and Initial Exploratory Data Analysis
├── 02_data_cleaning_and_eda.ipynb    # Data Cleaning & More Exploratory Data Analysis
├── 03_model_pipeline.ipynb           # Model Building & Evaluation
├── utils.py                          # Reusable utility functions
├── requirements.txt                  # Python dependencies
├── .gitignore                        # gitignore
├── README.md                         # This file
├── artifacts						  # model related artefacts; gitignored
|   ├── figures
|	├── models
|	└── results
├── figures
├── raw_data/
└── data_split/
    ├── test/
	├── train/
    └── val/
```

- `raw_data/` and `data_split/` are generated artifacts and can be recreated.
- To get started with the project, run the notebooks in order: `01_initial_eda.ipynb` --> `02_data_cleaning_and_eda.ipynb` --> `03_model_pipeline.ipynb`

## Results

TODO

## Key findings

Due to the text nature of the dataset, TDIF was used.
TODO

## Future Work

- Currently, the header is completely chopped to prevent data leakage, specific SPAM-related headers can be censored during the preprocessing.
- Preprocessing such as converting the email to lowercase, removing punctuations, replacing numbers with "Numbers", all URLS with "URL" and perform word stemming can be a future adventure.
- The model developed here can be used for a MLE project for Spam classification in the future.

## Tech Stack

- pandas, numpy
- matplotlib, seaborn
- scikit-learn

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# open 01_initial_eda to inspect the initial data loading and inspection
# open 02_data_cleaning_and_eda.ipynb to inspect the data cleaning and in-depth EDA
# open 03_model_pipeline.ipynb to inspect the model building and evaluation process
```

## Acknowledgements and References

- Apache SpamAssassin corpus maintainers.
- scikit-learn documentation.




## 5. Results

### 5.1 Baseline Metrics Snapshot
| Model | Accuracy | Spam Precision | Spam Recall | Spam F1 | Notes |
|------|----------|----------------|-------------|---------|-------|
| Logistic Regression | TODO | TODO | TODO | TODO | Initial baseline |
| Linear SVM | TODO | TODO | TODO | TODO | Initial baseline |
| Random Forest | TODO | TODO | TODO | TODO | Initial baseline |