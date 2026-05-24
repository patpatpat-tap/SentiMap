# SentiMap: Hybrid NLP and Geospatial Analysis for Mapping Cebu City Traffic Enforcement Grievances

**Authors:** Roman Patrick A. Duron; Rhobert Patena; Monico Vian Baxal  
**Affiliation:** Bachelor of Science in Information Technology, University of San Jose-Recoletos  
**Date:** May 15, 2026

## Abstract
SentiMap is a hybrid NLP and geospatial analytics system designed to convert Cebu City traffic enforcement grievances into actionable hotspot intelligence. The system ingests Reddit posts, filters and validates relevance, enriches text with Cebuano/Bislish-aware sentiment, sarcasm, and emotion signals, and maps grievances to locations for heatmap visualization. The output is a dashboard that supports hotspot detection and qualitative oversight through a grievance feed and analytics panels. This study documents the architecture and pipeline of SentiMap and frames an accuracy-testing plan for sentiment and emotion categorization. Initial system outputs show a predominantly negative grievance distribution and measurable sarcasm incidence in the cleaned dataset. Limitations include the absence of a gold-standard labeled set for formal accuracy metrics, which is addressed in the proposed evaluation plan.

## Introduction
Cebu City traffic enforcement complaints are frequently shared on social platforms but remain unstructured and difficult to analyze at scale. General sentiment tools often underperform on Cebuano/Bislish text because of slang, code-switching, and sarcasm, which can invert literal polarity. SentiMap addresses this gap by combining a Cebuano lexicon, sarcasm detection, and location extraction to generate a map-based view of grievance intensity. The system focuses on three core questions: (1) where grievances cluster, (2) how severe sentiments are, and (3) how often sarcasm or strong emotions appear. This paper presents the system architecture, workflow, and an accuracy-testing plan for the NLP module.

## Review of Related Literature/Works
Recent sentiment-analysis studies emphasize benchmark-based accuracy testing and multiple evaluation metrics. Mayzaroh et al. (2026) showed that Transformer-based models substantially outperform classical baselines on social media sentiment. Zhu et al. (2026) demonstrated that carefully evaluated models can generalize to Reddit-scale corpora, provided evaluation is transparent. Zahra et al. (2026), Maharani et al. (2026), and Purba et al. (2026) highlighted the importance of reporting macro or weighted F1 to account for class imbalance. These studies inform SentiMap's evaluation approach: accuracy and F1 should be reported for sentiment and emotion classes, with attention to imbalanced labels common in grievance datasets.

## Conceptual/Theoretical Framework (IPO)
SentiMap follows an Input-Process-Output framework aligned with the system architecture.

**Input**
- Reddit posts related to Cebu City traffic enforcement grievances.
- Metadata: timestamps, upvotes, comments, and URLs.

**Process**
- Data collection and filtering (two-layer relevance scoring).
- Cleaning and validation to produce a trusted subset.
- NLP enrichment: sentiment scoring, sarcasm detection, and multi-label emotions.
- Location extraction and confidence filtering.
- Geospatial clustering and severity computation.

**Output**
- Heatmap of complaint hotspots.
- Analytics dashboard (sentiment mix, sarcasm rate, emotion distribution).
- Grievance feed for qualitative inspection.

## Methodology
### System Design
SentiMap uses a layered architecture: a Next.js frontend communicates with a FastAPI backend that reads and writes to a Supabase (PostgreSQL) database. NLP enrichment is precomputed through batch processing to reduce runtime overhead.

### Data Collection and Preparation
Reddit posts are collected using a targeted scraper with two-layer filtering. Posts are merged, deduplicated, and cleaned before being marked as eligible for analytics. Only entries flagged as clean are used in the dashboard and heatmap.

### NLP and Geospatial Processing
The NLP module uses a Cebuano lexicon with phrase-first matching, negation and intensifier handling, emoji scoring, and sarcasm detection. Emotions are tagged as multi-label outputs (anger, frustration, fear, disgust, sadness, resignation, trust). Locations are extracted using keyword matching with confidence weighting to prevent generic location noise. Grievances are clustered by location to generate heatmap intensity radii and severity colors.

### Accuracy Testing Plan
Accuracy evaluation is framed as a supervised classification assessment for sentiment and emotion labels:
- Build a labeled validation subset of Cebuano/Bislish grievances.
- Compute accuracy, precision, recall, and F1 for sentiment polarity and each emotion class.
- Report macro and weighted F1 to reflect class imbalance.
- Conduct error analysis for sarcasm and location ambiguity.

## Results and Discussion
### Operational Results (System Outputs)
The current dataset in Supabase contains 736 posts, with 180 clean entries used for analytics. Within the clean subset, sentiment labels are dominated by negative posts (140 negative, 16 neutral, 24 positive). Sarcasm is detected in 42 posts (23.3 percent), indicating a substantial portion of grievances contain ironic or inverted sentiment. These distributions justify the need for specialized sarcasm handling and emotion tagging in Cebuano/Bislish contexts.

### Accuracy Findings and User Testing
Formal accuracy metrics are not yet available because a gold-standard labeled set has not been finalized. The system currently demonstrates functional correctness in producing stable sentiment, emotion, and location outputs and supports visual inspection through the grievance feed and analytics panels. The planned evaluation will quantify how accurately SentiMap categorizes emotions and sentiment using the metrics defined in the accuracy testing plan. A user testing component is also planned to measure task completion time and interpretability for intended users (traffic analysts and administrators).

### Limitations
- No finalized gold-standard dataset for sentiment and emotion accuracy metrics.
- Keyword-based location extraction may miss spelling variants or indirect references.
- Sarcasm detection focuses on explicit cues and may under-detect subtle cases.
- Snapshot-only dataset limits temporal trend analysis.

## Conclusion and Future Work
SentiMap provides a structured, location-aware view of Cebu City traffic enforcement grievances using a hybrid NLP and geospatial workflow. The system is operational, produces interpretable outputs, and is designed for accuracy testing once labeled data are finalized. Future work includes expanding coverage beyond Cebu, adding more emotion categories, improving accuracy through richer labeled datasets, and enabling longitudinal sentiment comparisons between historical and current grievance patterns.

## References
Mayzaroh, M. A., Ningsih, D. F., Destriani, N., & Manullang, M. C. T. (2026). Benchmarking PyCaret AutoML against IndoBERT fine-tuning for sentiment analysis on Indonesian IKN Twitter data. arXiv. https://doi.org/10.48550/arXiv.2604.25392

Zhu, Y., Lakamana, S., Rouhizadeh, M., Bozkurt, S., Hershenberg, R., & Sarker, A. (2026). LLM-augmented therapy normalization and aspect-based sentiment analysis for treatment-resistant depression on Reddit. arXiv. https://doi.org/10.48550/arXiv.2603.12343

Zahra, N. Z., Farhanatussaidah, S., Afifah, N. N., Muthoharoh, L., & Satria, A. (2026). Benchmarking logistic regression, SVM, naive Bayes, and IndoBERT fine-tuning for sentiment analysis on Indonesian product reviews. arXiv. https://doi.org/10.48550/arXiv.2605.03439

Maharani, V. P., Harvanny, K., Samudra, D., Muthoharoh, L., & Satria, A. (2026). Sentiment analysis of Mobile Legends app reviews using machine learning and LSTM-based deep learning models. arXiv. https://doi.org/10.48550/arXiv.2605.01317

Purba, U. W., Parhusip, A. H. R., Maulana, S., Muthoharoh, L., & Satria, A. (2026). Sentiment analysis of Indonesian Spotify reviews using machine learning and BiLSTM. arXiv. https://doi.org/10.48550/arXiv.2605.03443
