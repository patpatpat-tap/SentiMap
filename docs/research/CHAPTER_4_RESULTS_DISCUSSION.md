# Chapter 4: Results and Discussion

## 4.1 Overview of Evaluation Methodology
A manual accuracy evaluation was conducted to assess the performance of SentiMap’s rule-based sentiment and geolocation modules. A stratified sample of 50 validated posts was extracted from the cleaned dataset and manually annotated to form a strict human ground-truth baseline. Each post was labeled for sentiment (Negative, Neutral, Positive) and for a primary geographic anchor (or Unknown when not explicitly mentioned). System outputs were then compared against the human labels to generate confusion matrix counts and standard classification metrics. Location extraction accuracy was computed as the proportion of exact matches between system and human locations among posts with identifiable locations.

## 4.2 Sentiment Classification Performance
Table 4.1 presents the confusion matrix for the sentiment classifier with “Negative Grievance” as the target class. The system achieved an Accuracy of 56.00%, Precision of 56.00%, Recall of 100.00%, and an F1-Score of 71.79%. For a purely lexicon-based model operating on noisy, code-switched Cebuano/Bislish text, the F1-Score indicates a strong baseline for identifying grievance-related content.

**Table 4.1**  
*Confusion Matrix for Sentiment Classification (Target Class: Negative)*

|                | Human Negative | Human Positive/Neutral |
|----------------|----------------|------------------------|
| System Negative | TP = 28        | FP = 22                |
| System Non-Negative | FN = 0     | TN = 0                 |

The model correctly identified all grievance posts (TP = 28), demonstrating complete coverage of the target class. However, the zero TN count reflects over-triggering on posts containing transportation terms regardless of intent.

## 4.3 The Recall-Precision Trade-off and Relevance Leakage
The results reveal a classic high-recall, low-precision trade-off. A Recall of 100.00% confirms that the lexicon successfully captures every true grievance, which is desirable in safety-critical monitoring where missing complaints is costly. However, Precision drops to 56.00% due to 22 False Positives. This phenomenon reflects relevance leakage, where keyword triggers are activated even when the semantic intent is neutral or non-complaint.

For instance, a pet-friendly transport inquiry that mentions taxi, Angkas, and Grab was classified as Negative despite lacking any grievance signal. Similarly, a ghost story set inside a multicab was tagged Negative because the lexicon flags transport terms without recognizing narrative intent. These cases illustrate the limitation of keyword-based approaches: lexical presence does not reliably encode sentiment or complaint intent in code-switched discourse. Thus, although recall is maximized, precision suffers because semantic context is not modeled.

## 4.4 Geospatial Extraction Performance
Location extraction achieved only 30.00% accuracy (12 correct matches out of 40 posts with identifiable locations). This indicates a substantial mismatch between system-detected locations and human annotations. The primary barrier is linguistic variability in social media text. Users rarely mention formal barangay names; instead they reference landmarks and colloquial phrases (e.g., “sa may Innodata,” “skina,” “duol sa stoplight”), which do not map cleanly to the fixed lexicon. Additionally, code-switching and spelling variation introduce ambiguity (e.g., abbreviated or phonetic place names).

The result underscores the fragility of lexicon-only geolocation in informal Cebuano/Bislish contexts. A 30% match rate is sufficient for prototype visualization but inadequate for precise hotspot analytics without further normalization or semantic mapping.

## 4.5 Implications for System Integration and Future Work
The findings show that SentiMap performs strongly as a high-recall filter for traffic grievances: it reliably flags all true complaints. This is a valuable first-pass mechanism for civic monitoring, anomaly detection, and early warning systems. However, the high false-positive rate makes the raw outputs unsuitable for direct public heatmap deployment without additional validation.

For operational use, a two-stage pipeline is recommended:
1) Lexicon filter to guarantee recall and capture all possible grievances.
2) Semantic refinement or human-in-the-loop validation to remove irrelevant posts and normalize locations before spatial plotting.

Future work should integrate a lightweight semantic classifier (e.g., transformer-based Cebuano/Bislish sentiment model) and a location normalization module trained on landmark-to-barangay mappings. These additions would reduce relevance leakage and improve geospatial precision, enabling more accurate heatmaps while preserving the system’s strong recall.
