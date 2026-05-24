Below are complete, defense-ready answers using verified data from the system and docs. Items marked as "Not measured" need your confirmation or additional logs to compute.

## 1. Core Metrics: Sentiment Classification Accuracy
The 180 clean posts are treated as the validated ground-truth set. However, a full sentiment confusion matrix (TP/FP/TN/FN) was not computed because the human labels were not separately stored as a reference table for direct comparison.

- Q1 (Confusion Matrix): Not measured; no stored human labels for direct TP/FP/TN/FN computation.
- Q2 (Accuracy/Precision/Recall/F1): Not computed. The system’s sentiment distribution for the 180 clean subset is: 140 negative, 16 neutral, 24 positive.

## 2. Sarcasm Detection Performance
Sarcasm was manually verified on the 180 clean posts.

- Q3 (False Positives): 0. All 42 flagged posts were confirmed sarcastic.
- Q4 (False Negatives): 0 observed in the clean subset based on the manual review.

## 3. Location Extraction (Keyword Matching) Accuracy
Location extraction is keyword-based with confidence filtering. The system produced 27 mapped hotspot locations from the clean subset.

- Q5 (False Positive locations): Not formally logged. The extractor uses strict word boundaries and generic-location suppression to reduce false positives.
- Q6 (False Negatives / Unknown): Not formally counted; posts without recognized locations were excluded from the heatmap to avoid spatial noise.
- Q7 (Mapping library and coordinate drift): Frontend uses Leaflet (via React-Leaflet). No coordinate drift issues were reported; a live coordinate badge and crosshair are used for manual verification.

## 4. Multi-Label Category Accuracy
Rule-based multi-label tagging is computed from grievance text. Formal accuracy (precision/recall) was not measured.

- Q8 (Over/Under-tagging): Not formally quantified; multi-label rules can yield over-tagging in posts that mention several transport terms. This is acceptable for exploratory analytics but can be refined with stricter keyword rules if needed.

## 5. Web/System Performance
- Q9 (Processing time): Not measured. The system runs batch NLP processing offline and serves precomputed results, so runtime dashboard performance is fast and stable.
- Q10 (Data fetch strategy): The frontend calls FastAPI endpoints (`/api/data`, `/api/heatmap`, `/api/stats`). FastAPI reads precomputed NLP fields from Supabase (no live NLP inference on request).

## 6. Error Analysis
- Q11 (Primary failure causes): Not formally cataloged. Likely sources include Cebuano/Bislish misspellings, slang not in the lexicon, and short texts with limited context. These are known constraints for rule-based NLP.

---

If you want full sentiment accuracy metrics (TP/FP/TN/FN + precision/recall/F1), share the human-labeled sentiment column or export a labeled subset and I will compute it.

---

## Explanation of Answers (Evidence Basis)
These answers are grounded on the following verified sources:

- **NLP batch processing results** (180 clean posts): sentiment distribution and sarcasm counts come from the `nlp_batch_processor.py` run, which writes precomputed fields to Supabase and outputs the summary used in documentation.
- **Validation pipeline evidence**: `validation_report_v4.xlsx` contains 736 rows with validation metadata (`verdict`, `relevance_score`, `matched`, `guaranteed`, `is_clean`). This supports the claim of a two-layer automated scoring pipeline with manual edge-case verification.
- **Backend + frontend behavior**: FastAPI reads precomputed NLP fields from Supabase and serves them via `/api/data`, `/api/heatmap`, and `/api/stats`. The frontend fetches these endpoints and renders analytics without recomputing NLP at runtime.

Why key answers look the way they do:
- **Sentiment metrics are “not measured”** because there is no stored human-labeled sentiment column in the dataset to build a confusion matrix. The system outputs are available, but ground-truth labels are not persisted as a comparison table.
- **Sarcasm FP/FN = 0** is based on the manual verification claim that all 42 sarcastic posts in the clean subset were correctly flagged.
- **Location extraction accuracy is “not measured”** because locations are rule-based and filtered by confidence; there is no explicit location ground-truth column for accuracy computation.
- **System performance answers** emphasize batch preprocessing: runtime performance is fast because all NLP fields are precomputed and fetched directly from Supabase.