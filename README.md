# Apache SpamAssassin Email Spam Classifier

## 1. Project Overview

### 1.1 Objectives

- Build a end-to-end machine learning classifier(data download, extraction, train/test split, modeling and evaluation) to distinguish ham and spam emails using the Apache SpamAssassin public corpus.
- Use this project as an iterative learning for different MLOps tools.

### 1.2 Current Status

- Baseline pipeline is implemented in [notebooks/apache_spam_classifier.ipynb](notebooks/apache_spam_classifier.ipynb).
- Model search is wired up in the notebook with a `Pipeline` + `GridSearchCV` setup over Logistic Regression, Linear SVC, Multinomial NB, Complement NB, SGD, and Passive Aggressive; the Logistic Regression tuning run is still in progress.
- Basic evaluation is included (classification report + confusion matrix).
- Duplicate email files are removed before the split to reduce leakage risk.
- Dataset imbalance is observed but not yet addressed.
- The notebook now has helper functions for file inspection, train/test file collection, and folder-wise split handling.
- Email preprocessing is still exploratory: the current baseline strips headers with a blank-line split, and `email`-module parsing is being investigated for a more MIME-aware approach.
- Codebase refactoring/modularization is not yet done (currently notebook-centric).

### 1.3 Scope and Non-Goals (Current Phase)

- In scope now: reproducible baseline and comparative model performance.
- Not in scope yet: advanced imbalance mitigation, hyperparameter optimization, robust experiment tracking, production deployment.

## 2. Repository Structure

```text
.
├── notebooks/
│   └── apache_spam_classifier.ipynb   # End-to-end experimentation notebook
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── raw_data/                      # Extracted SpamAssassin corpus files
└── data_split/                    # Train/test split generated from raw_data/
		├── train/
		├── test/
		└── val/ (currently unused in split ratio)
```

- `raw_data/` and `data_split/` are generated artifacts and can be recreated.
- The notebook currently contains the canonical workflow.

## 3. Dataset

### 3.1 Source

- Apache SpamAssassin public corpus.
- Source: https://spamassassin.apache.org/old/publiccorpus/
- Date accessed: July 4, 2026

### 3.2 Dataset Composition

- Multiple ham/spam folders across different corpus snapshots.
- Class proportions are imbalanced (spam is a minority class).

### 3.3 Data Integrity and Caveats

- Character encoding handling (`latin-1`).
- Folder naming is used to derive labels.

## 4. Methodology

### 4.1 Data Acquisition and Extraction

- Download compressed corpus artifacts.
- Extract tar.bz2 files.
- Flatten nested directories.
- Move `readme.html` and clean temporary extraction directories.

### 4.2 Duplicate Removal

- Remove duplicate email files by comparing file contents before the train/test split.
- This step is intended to reduce leakage caused by the same email appearing in multiple places.

### 4.3 Label Construction

- Label rule: files with `spam` in path/folder -> label `1`, otherwise `0`.

### 4.4 Preprocessing Strategy

- Candidate preprocessing still includes header stripping, URL/number replacement, and stemming-like trimming.
- The current baseline preprocessing function strips headers by splitting on the first blank line and lowercasing the body.
- The notebook also includes a short `email`-module experiment to inspect `Subject`, `From`, and body parsing.
- A more robust MIME-aware preprocessing function is still in progress and will replace the blank-line split once it is stable.

### 4.5 Train/Test Split

- Split performed folder-wise with approximately 80/20 train/test ratio after duplicate removal.
- Random seed is fixed for reproducibility.
- Validation split is not yet actively used for model selection.

### 4.6 Feature Engineering

- TF-IDF vectorization over email files.
- Key settings: lowercase, English stop words, `latin-1` encoding, capped vocabulary (`max_features=10000`).
- Fit on train set; transform test set.
- Counter was considered but TF-IDF was preferred.

### 4.7 Modeling

- Logistic Regression baseline.
- SVM with linear kernel.
- Random Forest for non-linear comparison.

### 4.8 Evaluation

- Classification report (precision, recall, f1-score, support).
- Confusion matrix visualization.
- Compare performance with emphasis on spam recall/precision tradeoff.

## 5. Results (Fill This Iteratively)

### 5.1 Baseline Metrics Snapshot
| Model | Accuracy | Spam Precision | Spam Recall | Spam F1 | Notes |
|------|----------|----------------|-------------|---------|-------|
| Logistic Regression | TODO | TODO | TODO | TODO | Initial baseline |
| Linear SVM | TODO | TODO | TODO | TODO | Initial baseline |
| Random Forest | TODO | TODO | TODO | TODO | Initial baseline |

### 5.2 Error Analysis Notes (TODO)

Track insights such as:
- Typical false positives (ham predicted as spam).
- Typical false negatives (spam missed as ham).
- Any pattern related to newsletter-like ham or short spam messages.

## 6. Reproducibility

### 6.1 Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6.2 Run Workflow

1. Open the notebook.
2. Run cells in order from data download through evaluation.
3. Verify generated `raw_data/` and `data_split/` folders.

### 6.3 Reproducibility Notes

- Fixed random seed for split.
- Results may vary with package versions/platform.
- Ensure internet access if downloading corpus from source.

## 7. Known Limitations

- Dataset imbalance exists and is not yet addressed with class weighting/resampling/threshold tuning.
- No dedicated held-out validation workflow yet; current tuning relies on cross-validation inside the training split.
- Notebook workflow is not modularized into reusable scripts/packages.
- Limited experiment tracking (no formal run registry).
- Duplicate files are removed, but the broader leakage audit is still informal.
- The custom preprocessing pipeline is still partially implemented and needs a more robust email-header parser.
- The current grid-search setup still needs cleanup for invalid parameter combinations and model-specific warnings.

## 8. Roadmap

### 8.1 Near-Term Improvements
- Data leakage audit
- Add class imbalance handling experiments:
	- class weights,
	- resampling (undersampling/oversampling/SMOTE variants where appropriate),
	- threshold optimization.
- Add validation split usage and model comparison protocol.
- Add consistent metric reporting utility.
- Keep the model-search notebook section aligned with the baseline evaluation results once the Logistic Regression grid search completes.
- Refine the existing `sklearn.pipeline.Pipeline` + `GridSearchCV` setup, including parameter validity and the scoring choice used for tuning.
- Run `GridSearchCV` with at least these parameters:
	- `tfidf__max_features`,
	- `tfidf__ngram_range`,
	- `clf__C`.
- Finish the custom preprocessing pipeline that will run after the train/test split.

### 8.2 Mid-Term Improvements
- Make the project resume-ready for MLE and DS roles with clear, reproducible structure and outcomes.
- Refactor notebook pipeline into modular Python package/scripts:
	- data ingestion,
	- feature pipeline,
	- training,
	- evaluation.
- Add configuration management for experiments.
- Add saved model artifacts and inference script.
- Introduce reproducible experiment tracking:
	- run metadata (vectorizer settings, model hyperparameters, split seed),
	- versioned metric snapshots,
	- confusion matrices stored as artifacts.
- Add structured validation workflow:
	- use a proper train/validation/test strategy,
	- reserve test set strictly for final reporting,
	- compare models with consistent validation protocol.
- Add targeted hyperparameter search for baseline models:
	- Logistic Regression (`C`, regularization),
	- Linear SVM (`C`),
	- Random Forest (`n_estimators`, `max_depth`, `min_samples_split`).
- Add model persistence and loading standards:
	- save vectorizer + model bundle together,
	- include model metadata (training date, corpus snapshot, feature settings),
	- add a small prediction utility for single email files.
- Add lightweight quality checks:
	- data folder integrity checks,
	- label distribution checks,
	- duplicate filename/content detection before training.
- Add role-focused project polish:
	- concise project story (problem, approach, impact),
	- clear methodology and metrics narrative,
	- reproducible commands and expected outputs,
	- visual artifacts suitable for portfolio/GitHub showcase.

### 8.3 Longer-Term Improvements
#### 8.3.1 Data Science Track Aspirations
- Deep class imbalance analysis and mitigation study.
- Strong precision/recall/F1 comparison across models and settings.
- Precision-recall curve analysis.
- Threshold tuning experiments and decision-threshold justification.
- False-positive and false-negative example analysis.
- Top predictive words analysis for Logistic Regression.
- Discussion of business tradeoffs:
	- false spam (legitimate email blocked),
	- missed spam (spam delivered to inbox).
- Add robust error analysis dashboards and model comparison visuals.

#### 8.3.2 Machine Learning Engineering Track Aspirations
- Introduce production-style project structure:
	- `src/` with reusable modules,
	- `train.py`,
	- `evaluate.py`,
	- `predict.py`.
- Save model artifacts using `joblib`.
- Persist vectorizer and classifier together as one reproducible artifact bundle.
- Keep `requirements.txt` current and minimal.
- Maintain README with exact run commands for training, evaluation, and inference.
- Add config file(s) for model/data/vectorizer settings.
- Store model artifact metadata (training data snapshot, params, metrics, timestamp).
- Provide a simple inference interface:
	- CLI and/or FastAPI endpoint.
- Add CI validation:
	- GitHub Actions test that checks the pipeline runs end-to-end.

## 9. Changelog

- `2026-07-04`: Initialized end-to-end notebook workflow (`apache_spam_classifier.ipynb`) from data acquisition to model evaluation.
- `2026-07-04`: Added corpus download and extraction pipeline (archive extraction, folder flattening, and dataset cleanup).
- `2026-07-04`: Implemented exploratory dataset inspection and class distribution summary; confirmed class imbalance in corpus composition.
- `2026-07-04`: Added train/test split generation (`data_split`) with fixed random seed for reproducibility.
- `2026-07-04`: Implemented TF-IDF feature pipeline (`input='filename'`, English stop-word removal, `latin-1` handling, `max_features=10000`).
- `2026-07-04`: Trained and evaluated baseline models: Logistic Regression, linear SVM, and Random Forest.
- `2026-07-04`: Added evaluation reporting with classification reports and confusion matrix visualizations for model comparison.
- `2026-07-04`: Updated project dependencies snapshot in `requirements.txt` via environment freeze.

- `2026-07-11`: Added duplicate email file removal before splitting to reduce leakage risk.
- `2026-07-11`: Moved the planned preprocessing steps below the split and kept the custom preprocessing function as work in progress.
- `2026-07-18`: Refined the notebook workflow with helper functions for file discovery/splitting and added exploratory `email`-module parsing.
- `2026-07-18`: Updated preprocessing notes to reflect the current baseline header-stripping logic and the remaining MIME-aware parsing work.
- `2026-07-18`: Added `GridSearchCV`-based model-search scaffolding for the baseline classifiers; Logistic Regression tuning is still running.
- `2026-07-19`: Expanded the notebook model search into a `Pipeline` + `GridSearchCV` workflow with multiple baseline classifiers and updated the README to match the current preprocessing and tuning status.
- `2026-08-16`: Working on Email flags hiding.
- `2026-08-20`: Narrowed scope of the project to focus just on data science aspect. Translated the generic notebook into `01_eda.ipynb`, `02_data_cleaning.ipynb`, etc.
- `2026-08-21`: finished with `01_initial_eda.ipynb`.

## 10. Acknowledgements and References

- Apache SpamAssassin corpus maintainers.
- scikit-learn documentation.

## 11. AI Statement

AI was used for documentation.