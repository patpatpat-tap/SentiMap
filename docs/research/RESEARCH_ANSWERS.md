# Research Answers

# Student Name / Group Name: 
- Roman Patrick A. Duron, Rhobert Patena, Monico Vian Baxal
# Research Title: SentiMap:
- Hybrid NLP and Geospatial Analysis for Mapping Cebu City Traffic Enforcement Grievances 
# Selected Testing Method: 
- Accuracy Testing 


## Part 1: Your Research Testing Focus

- Research Title: SentiMap: Hybrid NLP and geospatial analysis for mapping Cebu City traffic enforcement grievances
- Research Output: A Cebu City heatmap and analytics dashboard that summarizes complaint hotspots and sentiment using NLP-enriched Reddit data.
- Main Testing Method Selected: Accuracy testing
- Reason for Choosing This Testing Method: The core contribution of SentiMap is an NLP-driven classification and geolocation pipeline. Accuracy testing verifies that sentiment labels, sarcasm detection, and location extraction match human-validated ground truth, which is essential for reliable hotspot mapping.
- Research Objective Linked to This Testing Method: To measure how accurately the hybrid NLP engine identifies sentiment polarity, sarcasm, and location mentions in Cebuano/Bislish traffic grievances and to ensure the resulting heatmap reflects true grievance distributions.
- Expected Evidence from Testing: Quantitative accuracy metrics (accuracy, precision, recall, F1-score) for sentiment and location extraction, error counts per category, and a confusion matrix or tabulated misclassifications from a labeled validation subset.

## Part 2: Summary of Five Related Studies

| # | Title of Related Study | Author/s and Year | Research Output | Testing Method Used | Metrics / Measurements | Key Testing Result |
|---|---|---|---|---|---|---|
| 1 | Benchmarking PyCaret AutoML Against IndoBERT Fine-Tuning for Sentiment Analysis on Indonesian IKN Twitter Data (arXiv:2604.25392) | Mayzaroh et al., 2026 | Binary sentiment classifier for Indonesian Twitter comments on IKN | Accuracy testing via model benchmarking | Accuracy, F1-score | Logistic Regression: 77.57% accuracy, 77.17% F1; IndoBERT: 89.59% accuracy, 89.37% F1 |
| 2 | LLM-Augmented Therapy Normalization and Aspect-Based Sentiment Analysis for Treatment-Resistant Depression on Reddit (arXiv:2603.12343) | Zhu et al., 2026 | Aspect-based sentiment classifier for medication mentions in Reddit TRD posts | Accuracy testing (classifier evaluation) | Micro-F1 | DeBERTa-v3 model achieved micro-F1 of 0.800 on the shared-task test set |
| 3 | Benchmarking Logistic Regression, SVM, Naive Bayes, and IndoBERT Fine-Tuning for Sentiment Analysis on Indonesian Product Reviews (arXiv:2605.03439) | Zahra et al., 2026 | Three-class sentiment classifier for Tokopedia product reviews | Accuracy testing via model comparison | Accuracy, Macro F1, Weighted F1 | Linear SVC: 97.60% accuracy, Macro F1 0.5510; IndoBERT: 88.70% accuracy, Macro F1 0.5088 |
| 4 | Sentiment Analysis of Mobile Legends App Reviews Using Machine Learning and LSTM-Based Deep Learning Models (arXiv:2605.01317) | Maharani et al., 2026 | Three-class sentiment classifier for Mobile Legends app reviews | Accuracy testing via ML vs LSTM comparison | Accuracy, Weighted F1 | LSTM achieved 92% accuracy and weighted F1 of 91% |
| 5 | Sentiment Analysis of Indonesian Spotify Reviews Using Machine Learning and BiLSTM (arXiv:2605.03443) | Purba et al., 2026 | Three-class sentiment classifier for Spotify user reviews | Accuracy testing via ML vs BiLSTM benchmark | Weighted F1 (reported as main metric) | BiLSTM achieved the highest weighted F1 overall; Decision Tree was best among classical models |

## Part 3.1: Detailed Testing Procedure Analysis - Study 1

- Complete Citation: Mayzaroh, M. A., Ningsih, D. F., Destriani, N., and Manullang, M. C. T. (2026). Benchmarking PyCaret AutoML Against IndoBERT Fine-Tuning for Sentiment Analysis on Indonesian IKN Twitter Data. arXiv:2604.25392.
- Research Problem / Purpose: Compare classical machine learning baselines against a Transformer model (IndoBERT) for binary sentiment classification of Indonesian Twitter comments about IKN.
- Research Output: A benchmarking study that identifies the best-performing sentiment classifier for the IKN Twitter dataset.
- Testing Method Used: Accuracy testing through model benchmarking and evaluation on labeled data.
- How Testing Was Conducted: Classical models (Logistic Regression, Naive Bayes, SVM) were evaluated using 10-fold cross-validation; IndoBERT (indobenchmark/indobert-base-p1) was fine-tuned for five epochs and evaluated on a test set.
- Testing Participants / Data / Test Cases: 1,472 manually labeled Twitter comments (780 negative, 692 positive) related to IKN.
- Metrics or Measurements Used: Accuracy and F1-score.
- Success Criteria or Basis for Interpretation: Higher accuracy and F1 indicate a better-performing model for sentiment classification.
- Key Testing Result: IndoBERT achieved 89.59% test accuracy and 89.37% F1; the best classical model (Logistic Regression) reached 77.57% accuracy and 77.17% F1.
- Strength of Their Testing Approach: Direct comparison of multiple baselines and a Transformer model on the same labeled dataset with consistent metrics.
- Weakness / Limitation / Unclear Part: Limited to binary sentiment and a relatively small dataset; evaluation details for the test split vs. cross-validation are not fully comparable.
- Insight You Can Apply to Your Own Research: Use a clear benchmark framework (baseline vs. advanced model) and report accuracy and F1 to justify the selected model for sentiment classification in SentiMap.

## Part 3.2: Detailed Testing Procedure Analysis - Study 2

- Complete Citation: Zhu, Y., Lakamana, S., Rouhizadeh, M., Bozkurt, S., Hershenberg, R., and Sarker, A. (2026). LLM-Augmented Therapy Normalization and Aspect-Based Sentiment Analysis for Treatment-Resistant Depression on Reddit. arXiv:2603.12343.
- Research Problem / Purpose: Normalize medication mentions and classify sentiment toward treatments in TRD-related Reddit posts.
- Research Output: An aspect-based sentiment classifier applied to Reddit medication mentions with sentiment distributions by drug and time.
- Testing Method Used: Accuracy testing via classifier evaluation on a labeled test set.
- How Testing Was Conducted: DeBERTa-v3 was fine-tuned on the SMM4H 2023 therapy-sentiment dataset with LLM-based data augmentation and evaluated on the shared-task test set.
- Testing Participants / Data / Test Cases: 5,059 Reddit posts mentioning TRD; 3,839 posts with medication mentions (23,399 mentions). Classifier training/testing referenced the SMM4H 2023 therapy-sentiment dataset.
- Metrics or Measurements Used: Micro-F1.
- Success Criteria or Basis for Interpretation: Higher micro-F1 indicates better multi-class sentiment classification performance.
- Key Testing Result: Micro-F1 of 0.800 on the shared-task test set.
- Strength of Their Testing Approach: Uses a standardized shared-task benchmark and applies the trained model to a large real-world Reddit corpus.
- Weakness / Limitation / Unclear Part: Domain shift between the shared-task dataset and Reddit posts may affect generalization; some evaluation details are based on the shared-task set rather than in-domain Reddit labels.
- Insight You Can Apply to Your Own Research: Use an external benchmark to validate model quality, then report in-domain application results separately for transparency.

## Part 3.3: Detailed Testing Procedure Analysis - Study 3

- Complete Citation: Zahra, N. Z., Farhanatussaidah, S., Afifah, N. N., Muthoharoh, L., and Satria, A. (2026). Benchmarking Logistic Regression, SVM, Naive Bayes, and IndoBERT Fine-Tuning for Sentiment Analysis on Indonesian Product Reviews. arXiv:2605.03439.
- Research Problem / Purpose: Compare classical ML baselines and IndoBERT for three-class sentiment analysis on Indonesian product reviews.
- Research Output: A benchmarked sentiment classifier and evaluation of model performance under class imbalance.
- Testing Method Used: Accuracy testing via model benchmarking.
- How Testing Was Conducted: TF-IDF features were used with Logistic Regression, Linear SVM, and Multinomial Naive Bayes; IndoBERT was fine-tuned with weighted loss to address class imbalance; performance was compared on the same dataset.
- Testing Participants / Data / Test Cases: Tokopedia Product Reviews 2025 dataset (three-class labels: positive, neutral, negative).
- Metrics or Measurements Used: Accuracy, Macro F1, Weighted F1.
- Success Criteria or Basis for Interpretation: Higher accuracy and F1 indicate better classification performance; macro F1 reflects balance across classes.
- Key Testing Result: Linear SVC achieved 97.60% accuracy and Macro F1 of 0.5510; IndoBERT achieved 88.70% accuracy and Macro F1 of 0.5088.
- Strength of Their Testing Approach: Clear baseline vs Transformer comparison with explicit handling of class imbalance and multiple F1 variants.
- Weakness / Limitation / Unclear Part: Sampling differences between baseline and Transformer training may affect fairness of comparison.
- Insight You Can Apply to Your Own Research: Report macro and weighted F1 for imbalanced sentiment classes to avoid overstating performance.

## Part 3.4: Detailed Testing Procedure Analysis - Study 4

- Complete Citation: Maharani, V. P., Harvanny, K., Samudra, D., Muthoharoh, L., and Satria, A. (2026). Sentiment Analysis of Mobile Legends App Reviews Using Machine Learning and LSTM-Based Deep Learning Models. arXiv:2605.01317.
- Research Problem / Purpose: Compare ML and LSTM models for three-class sentiment analysis of app reviews.
- Research Output: A comparative evaluation showing LSTM performance for informal review text.
- Testing Method Used: Accuracy testing via model comparison.
- How Testing Was Conducted: Classical ML models with TF-IDF and PyCaret AutoML were compared against an LSTM model; performance was measured on a labeled review dataset.
- Testing Participants / Data / Test Cases: 10,000 labeled Mobile Legends app reviews (positive, negative, neutral).
- Metrics or Measurements Used: Accuracy, Weighted F1.
- Success Criteria or Basis for Interpretation: Higher accuracy and weighted F1 indicate stronger classification performance.
- Key Testing Result: LSTM achieved 92% accuracy and weighted F1 of 91%.
- Strength of Their Testing Approach: Direct ML vs deep learning comparison on the same labeled dataset with clear metrics.
- Weakness / Limitation / Unclear Part: Limited to a single app domain; may not generalize to other review corpora or languages.
- Insight You Can Apply to Your Own Research: Compare simple baselines against a stronger model to justify added complexity in the NLP pipeline.

## Part 3.5: Detailed Testing Procedure Analysis - Study 5

- Complete Citation: Purba, U. W., Parhusip, A. H. R., Maulana, S., Muthoharoh, L., and Satria, A. (2026). Sentiment Analysis of Indonesian Spotify Reviews Using Machine Learning and BiLSTM. arXiv:2605.03443.
- Research Problem / Purpose: Evaluate machine learning baselines versus BiLSTM for three-class sentiment classification of Indonesian Spotify reviews.
- Research Output: A benchmarked sentiment classifier and analysis of class imbalance effects.
- Testing Method Used: Accuracy testing via ML vs BiLSTM benchmark.
- How Testing Was Conducted: SVM, Multinomial Naive Bayes, and Decision Tree were evaluated against a two-layer BiLSTM using the same preprocessing pipeline (slang normalization, stopword removal, stemming).
- Testing Participants / Data / Test Cases: 100,000 scraped reviews with 70,155 cleaned samples for three-class sentiment labels.
- Metrics or Measurements Used: Weighted F1 (reported as the main metric).
- Success Criteria or Basis for Interpretation: Higher weighted F1 indicates stronger overall classification performance under class imbalance.
- Key Testing Result: BiLSTM achieved the highest weighted F1 overall; Decision Tree was best among classical models.
- Strength of Their Testing Approach: Large dataset and consistent preprocessing for fair model comparison.
- Weakness / Limitation / Unclear Part: Reported weakness on the minority neutral class suggests imbalance sensitivity.
- Insight You Can Apply to Your Own Research: Use weighted metrics and describe minority-class behavior when reporting sentiment performance.

## Part 4: Comparison of Testing Approaches

Comparison points:
- Common testing methods used: Supervised model evaluation with accuracy testing and benchmark comparisons.
- Common metrics used: Accuracy, F1-score (macro, weighted, or micro), and sometimes precision/recall when available.
- Common participants, datasets, or test cases used: Labeled text datasets from social media or user reviews with positive/neutral/negative classes.
- Differences in how testing was conducted: Some studies use cross-validation for baselines and a held-out test set for deep models; others fine-tune Transformers and report a single test-set score; dataset sizes range from thousands to tens of thousands with varying class imbalance strategies.
- Most useful testing approach among the five studies: Benchmarking multiple baselines against a stronger model with clearly reported F1 variants and class-imbalance handling.
- Testing practice you can apply to your own research: Report macro and weighted F1 in addition to accuracy and describe class imbalance effects.
- Testing practice you should avoid: Comparing models trained on different sampling regimes without clear normalization or fairness notes.

Comparison matrix:

| Study | Most Similar to Your Research? | Strongest Testing Practice | Weakest / Missing Part | How It Can Improve Your Test Plan |
|---|---|---|---|---|
| Study 1 | Partly similar (social media sentiment) | Baseline vs Transformer benchmark with clear accuracy/F1 | Binary labels only | Use a baseline + advanced model comparison in SentiMap |
| Study 2 | Moderately similar (Reddit text) | Shared-task test set with micro-F1 | Domain shift between benchmark and Reddit | Add a small in-domain labeled subset for validation |
| Study 3 | Partly similar (three-class sentiment) | Macro and weighted F1 with imbalance handling | Sampling differences across models | Standardize splits for fair comparison |
| Study 4 | Partly similar (app review sentiment) | Simple ML vs LSTM comparison with clear metrics | Single-domain dataset | Include cross-domain checks if possible |
| Study 5 | Partly similar (review sentiment) | Large dataset with consistent preprocessing | Weak neutral-class performance | Track minority-class errors in SentiMap |

## Part 5: Insights for Your Own Research

Student responses:
- What did you learn from the way other researchers tested their projects? Consistent, transparent reporting of accuracy and F1 across multiple models is essential for credibility, especially when data are noisy and class distributions are imbalanced.
- What testing method, metric, or procedure can you adopt for your own research? Use baseline vs advanced model benchmarking and report macro/weighted F1 in addition to accuracy, with a held-out test set for final reporting.
- What will you improve in your original Testing Plan Matrix? Include class imbalance handling, per-class error analysis, and a small manually labeled Cebuano/Bislish validation subset.
- What mistakes or weaknesses should you avoid when conducting your own testing? Avoid comparing models trained on different data subsets or reporting only accuracy without F1, especially with imbalanced sentiment classes.

Final reflection paragraphs:

Paragraph 1:
The related studies show that accuracy testing is most convincing when it benchmarks multiple models on the same labeled dataset and reports both accuracy and F1 variants. Studies that combine baselines with Transformer models provide a clear justification for why a more advanced method is used. This approach is important for SentiMap because Cebuano and Bislish traffic discourse contains sarcasm and slang, which can lower performance if evaluation is too shallow or metrics are incomplete.

Paragraph 2:
For SentiMap, I will adopt a baseline-versus-advanced comparison and include macro and weighted F1 to reflect class imbalance in sentiment labels. I will also add a small, manually labeled Cebuano/Bislish validation subset to check performance on in-domain text. I will avoid reporting only accuracy or mixing different sampling regimes across models, which can hide weaknesses and make results difficult to compare fairly.

## Part 6: References (APA)

1. Mayzaroh, M. A., Ningsih, D. F., Destriani, N., & Manullang, M. C. T. (2026). Benchmarking PyCaret AutoML against IndoBERT fine-tuning for sentiment analysis on Indonesian IKN Twitter data. arXiv. https://doi.org/10.48550/arXiv.2604.25392
2. Zhu, Y., Lakamana, S., Rouhizadeh, M., Bozkurt, S., Hershenberg, R., & Sarker, A. (2026). LLM-augmented therapy normalization and aspect-based sentiment analysis for treatment-resistant depression on Reddit. arXiv. https://doi.org/10.48550/arXiv.2603.12343
3. Zahra, N. Z., Farhanatussaidah, S., Afifah, N. N., Muthoharoh, L., & Satria, A. (2026). Benchmarking logistic regression, SVM, naive Bayes, and IndoBERT fine-tuning for sentiment analysis on Indonesian product reviews. arXiv. https://doi.org/10.48550/arXiv.2605.03439
4. Maharani, V. P., Harvanny, K., Samudra, D., Muthoharoh, L., & Satria, A. (2026). Sentiment analysis of Mobile Legends app reviews using machine learning and LSTM-based deep learning models. arXiv. https://doi.org/10.48550/arXiv.2605.01317
5. Purba, U. W., Parhusip, A. H. R., Maulana, S., Muthoharoh, L., & Satria, A. (2026). Sentiment analysis of Indonesian Spotify reviews using machine learning and BiLSTM. arXiv. https://doi.org/10.48550/arXiv.2605.03443

## Part 7: Submission Checklist

- I identified one testing method from my Testing Plan Matrix.
- I reviewed five related computing research studies.
- Each related study uses the same or similar testing method.
- I explained how testing was conducted in each study.
- I identified participants, datasets, test cases, or devices used in testing.
- I identified metrics, measurements, or success criteria.
- I provided insights that can improve my own testing plan.
- I included complete references for all five studies.
