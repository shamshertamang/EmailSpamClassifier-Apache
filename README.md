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

**6 models** were trained on the dataset with **cross validation**, all being adjusted for the class imbalance dataset. The models were scored on accuracy, precision, recall, F1 Score, ROC-AUC and PR-AUC. Because of the imbalanced nature of the dataset, we place a **heavy emphasis on metrics** of **Precision, Recall, F1 score and PR-AUC**.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.934 | 0.984 | 0.759 | 0.857 | 0.995 | 0.984 | TODO
| Gradient Boosting | 0.925 | 0.988 | 0.722 | 0.835 | 0.992 | 0.980 | TODO
| SVM (RBF Kernel) calibrated | 0.918 | 0.979 | 0.701 | 0.817 | 0.994 | 0.982 | TODO
| Logistic Regression | 0.914 | 0.947 | 0.709 | 0.811 | 0.987 | 0.959 | TODO
| Multinomial Naive Bayes | 0.894 | 0.841 | 0.731 | 0.782 | 0.972 | 0.903 | TODO
| Decision Tree | 0.888 | 0.936 | 0.612 | 0.739 | 0.793 | 0.806 | TODO

## Key findings

- Due to the text nature of the dataset, TDIF was used.

- Our classification problem had only 26.02% SPAM instances which meant, even if a model that always classify to HAM, would still be 73.98% accurate. So accuracy is not a good metric here. It is important to use the precision recall to evaluate the effectiveness and threshold selection.

- SVM, Random Forest and Gradient Boosting all had a very high PR-AUC of 98%. We ended up choosing SVM because it had a higher precision and better performance on F1 score. Although random forest would have been a good compromise for computational reasons.

- Random Forest, Gradient Boosting, and SVM demonstrated the highest overall precision–recall performance. Generally, increasing precision comes at the expense of recall and vice versa, depending on the classification threshold. However, our models maintained high precision across a wide range of recall values, demonstrating a favorable trade-off.

- Training SVM took forever and it was painfully slow. Dataset sampling could have made the training and inference faster. Random Forest could also have been a good compromise for computational and inference benefits.

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

# open and inspect each file in order
# 01_initial_eda --> initial data loading and inspection
# 02_data_cleaning_and_eda.ipynb --> data cleaning and in-depth EDA
# 03_model_pipeline.ipynb --> model building and evaluation process
```

## Acknowledgements and References

- Apache SpamAssassin corpus maintainers.
- scikit-learn documentation.