# Apache SpamAssassin Email Spam Classifier

## 1. Project Overview

### 1.1 Objective
Write a short summary of the goal of this project.

Suggested content:
- Build a machine learning classifier to distinguish spam vs ham emails using the Apache SpamAssassin public corpus.
- Establish an end-to-end baseline pipeline (data download, extraction, train/test split, vectorization, modeling, and evaluation).
- Use this project as an iterative learning/research workflow, with improvements planned over time.

### 1.2 Current Status
Document exactly where the project stands today.

Suggested content:
- Baseline pipeline is implemented in a notebook.
- Models tested: Logistic Regression, linear SVM, and Random Forest.
- Basic evaluation is included (classification report + confusion matrix).
- Dataset imbalance is observed but not yet addressed.
- Codebase refactoring/modularization is not yet done (currently notebook-centric).

### 1.3 Scope and Non-Goals (Current Phase)
Use this section to prevent overpromising.

Suggested content:
- In scope now: reproducible baseline and comparative model performance.
- Not in scope yet: advanced imbalance mitigation, hyperparameter optimization, robust experiment tracking, production deployment.

## 2. Repository Structure

Describe the directory structure and what each part is responsible for.

Suggested format:

```text
.
├── apache_spam_classifier.ipynb   # End-to-end experimentation notebook
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── data/                          # Extracted SpamAssassin corpus files
└── data_split/                    # Train/test split generated from data/
		├── train/
		├── test/
		└── val/ (currently unused in split ratio)
```

Add notes such as:
- `data/` and `data_split/` are generated artifacts and can be recreated.
- The notebook currently contains the canonical workflow.

## 3. Dataset

### 3.1 Source
Document the dataset origin and citation.

Suggested content:
- Apache SpamAssassin public corpus.
- Include source URL and date accessed.

### 3.2 Dataset Composition
Summarize what is loaded.

Suggested content:
- Multiple ham/spam folders across different corpus snapshots.
- Class proportions are imbalanced (spam is a minority class).

### 3.3 Data Integrity and Caveats
Suggested points to document:
- Character encoding handling (`latin-1`).
- Folder naming is used to derive labels.
- Potential duplicate or near-duplicate emails across folders/time periods.
- Potential dataset shift across corpus dates.

## 4. Methodology

### 4.1 Data Acquisition and Extraction
Describe the pipeline stage where corpus files are downloaded and extracted.

Suggested bullets:
- Download compressed corpus artifacts.
- Extract tar.bz2 files.
- Flatten nested directories.
- Move `readme.html` and clean temporary extraction directories.

### 4.2 Label Construction
Document how labels are currently created.

Suggested content:
- Label rule: files with `spam` in path/folder -> label `1`, otherwise `0`.
- Mention assumptions and risk of path-based labeling.

### 4.3 Preprocessing Strategy
Document what was considered and what is currently used.

Suggested content:
- Candidate preprocessing (header stripping, URL/number replacement, stemming-like trimming) was explored.
- Current baseline uses minimal preprocessing because preliminary tests performed better without aggressive text normalization.

### 4.4 Train/Test Split
Document split strategy.

Suggested content:
- Split performed folder-wise with approximately 80/20 train/test ratio.
- Random seed is fixed for reproducibility.
- Validation split is not yet actively used for model selection.

### 4.5 Feature Engineering
Document vectorization settings.

Suggested content:
- TF-IDF vectorization over email files.
- Key settings: lowercase, English stop words, `latin-1` encoding, capped vocabulary (`max_features=10000`).
- Fit on train set; transform test set.
- mention that counter was considered

### 4.6 Modeling
Document baseline models.

Suggested content:
- Logistic Regression baseline.
- SVM with linear kernel.
- Random Forest for non-linear comparison.

### 4.7 Evaluation
Document metrics and visualizations.

Suggested content:
- Classification report (precision, recall, f1-score, support).
- Confusion matrix visualization.
- Compare performance with emphasis on spam recall/precision tradeoff.

## 5. Results (Fill This Iteratively)

Use this section to track outcomes over time.

Suggested template:

### 5.1 Baseline Metrics Snapshot
| Model | Accuracy | Spam Precision | Spam Recall | Spam F1 | Notes |
|------|----------|----------------|-------------|---------|-------|
| Logistic Regression | TODO | TODO | TODO | TODO | Initial baseline |
| Linear SVM | TODO | TODO | TODO | TODO | Initial baseline |
| Random Forest | TODO | TODO | TODO | TODO | Initial baseline |

### 5.2 Error Analysis Notes
Track insights such as:
- Typical false positives (ham predicted as spam).
- Typical false negatives (spam missed as ham).
- Any pattern related to newsletter-like ham or short spam messages.

## 6. Reproducibility

Document exact steps for others to run your baseline.

Suggested structure:

### 6.1 Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6.2 Run Workflow
Suggested steps:
1. Open the notebook.
2. Run cells in order from data download through evaluation.
3. Verify generated `data/` and `data_split/` folders.

### 6.3 Reproducibility Notes
Suggested notes:
- Fixed random seed for split.
- Results may vary with package versions/platform.
- Ensure internet access if downloading corpus from source.

## 7. Known Limitations

Make this section explicit and honest.

Suggested items:
- Dataset imbalance exists and is not yet addressed with class weighting/resampling/threshold tuning.
- No dedicated validation-driven model selection pipeline yet.
- Notebook workflow is not modularized into reusable scripts/packages.
- Limited experiment tracking (no formal run registry).
- Potential risk of data leakage or duplicate leakage has not been formally audited.

## 8. Roadmap

Track future milestones.

Suggested phases:

### 8.1 Near-Term Improvements
- Add class imbalance handling experiments:
	- class weights,
	- resampling (undersampling/oversampling/SMOTE variants where appropriate),
	- threshold optimization.
- Add validation split usage and model comparison protocol.
- Add consistent metric reporting utility.
- Move modeling into a `sklearn.pipeline.Pipeline` and add cross-validation with `scoring='f1'`.
- Run `GridSearchCV` with at least these parameters:
	- `tfidf__max_features`,
	- `tfidf__ngram_range`,
	- `clf__C`.

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

## 10. Acknowledgements and References

Suggested content:
- Apache SpamAssassin corpus maintainers.
- scikit-learn documentation/resources used.
- Any tutorials/papers that informed implementation decisions.

---

## Quick Fill Checklist

Use this checklist to complete documentation quickly:
- Add one-paragraph project objective.
- Add dataset source URL + access date.
- Fill baseline metrics table from current notebook outputs.
- Add 3-5 bullets under known limitations.
- Add next 3 concrete roadmap tasks.
