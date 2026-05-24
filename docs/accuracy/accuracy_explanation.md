# Accuracy Explanation (LLM-as-Judge Audit)

This document audits the 50-row sample from `accuracy_sample_50.csv` and explains why certain rows were labeled as false positives or location failures in the simulated accuracy test.

## 1) False Positives (System = Negative, Human = Positive/Neutral)
These 27 rows were marked negative by the system inference rules, but the human ground truth labeled them as non-negative.

- Cebu BRT back on track? — Neutral. Question about progress; not a complaint.
- Urban Legends / Horror Stories in Cebu — Neutral. Not a traffic grievance.
- Pam opposes provisional approval of 600 EV Taxis — Neutral. Policy/news update.
- I need an advice. (Maybe legal) — Neutral. Advice request, no grievance.
- New Route from Vallacar Transit Inc (Ceres) and Modern Jeep Cooperatives — Neutral. Informational announcement.
- BRT is now on Test Run after 30 years planning to Test Run — Neutral. Informational update.
- Transpo na mu allow ug furbaby? — Neutral. Question about policy.
- Happy About the Small Things I’ve Done this Week — Positive. Explicitly positive tone.
- Beep operations to stop operations starting October 1 — Neutral. Service notice.
- Questions abt Living in Cebu — Neutral. General inquiry.
- Mayor Garcia wants Cebu City to be walkable, less reliant on cars — Positive. Improvement framing.
- PNP checkpoint innodata area — Neutral. Informational mention.
- "Farmer ko Sir"... LTO 7, PNP to file charges — Neutral. Report of enforcement action.
- Any government employees aware of the reason for this? — Neutral. Inquiry without complaint.
- Jeepney Phaseout topic studies — Neutral. Discussion topic.
- Today I experienced the importance sa dashcam — Neutral. Reflective statement.
- Cebu city transportation office — Neutral. Generic label/title.
- Mandaue adopts AI traffic system to ease congestion — Positive. Improvement framing.
- Work on CBRT project progresses — Positive. Progress update.
- Taxi Drivers nga mga gwapo — Positive. Playful/positive tone.
- GUADALUPE TRANSPORTATION — Neutral. Label/heading.
- Cebu City Transportation Office (CCTO) changes uniforms again — Neutral. Administrative update.
- Commute to Cebu Doc — Neutral. Route inquiry.
- Call me weird, but.. — Neutral. Ambiguous, no grievance in title.
- DOTr/OPAV say Cebu BRT route expanded, improved — Positive. Explicit improvement.
- Finally gi no left turn na ang SRP intersections — Positive. Rule change as improvement.
- Help, pls! Commute to Talisay from Cebu/Mandaue. — Neutral. Help request.

## 2) Location Extraction Failures (14 rows)
These rows had explicit locations inferred by the human judge, but the system outputted a different location or Unknown.

- What is happening in cebu traffic law enforcement??? — True: Cebu City | System: Unknown | Missed D4 location tag.
- Ngano wala pay Number Coding sa Cebu na perti namang Traffika? — True: Cebu City | System: Unknown | Cebu mentioned, no D4 tag.
- Nagkawalay dignidad ang pagcommute sa Cebu? — True: Cebu City | System: Unknown | Cebu mentioned, no D4 tag.
- Worst experience in MCIA T1 last night — True: Mactan | System: Unknown | MCIA implies Mactan, not in D4 tags.
- Mayor Garcia wants Cebu City to be walkable — True: Cebu City | System: Unknown | Cebu mentioned, no D4 tag.
- dyos miyo ang traffic sa consolacion — True: Consolacion | System: Mandaue | Multiple D4 tags, first one chosen.
- Cebu city transportation office — True: Cebu City | System: Guadalupe | Specific D4 tag selected over generic Cebu City.
- Mandaue adopts AI traffic system to ease congestion — True: Mandaue | System: Unknown | No D4 tag.
- Driving in Cebu is not for the Weak! — True: Cebu City | System: Fuente | Specific D4 tag selected.
- Cebu City Transportation Office (CCTO) changes uniforms again — True: Cebu City | System: Unknown | No D4 tag.
- Commute to Cebu Doc — True: Cebu City | System: Basak | Specific D4 tag selected.
- DOTr/OPAV say Cebu BRT route expanded, improved — True: SRP | System: Unknown | SRP in text, no D4 tag.
- Finally gi no left turn na ang SRP intersections — True: SRP | System: Unknown | SRP in text, no D4 tag.
- Help, pls! Commute to Talisay from Cebu/Mandaue. — True: Talisay | System: Unknown | Location implied, no D4 tag.

## 3) Reflection on Methodology
The system inference heuristic labeled every sample as Negative because the rules treated any transport or enforcement anchors (D1/D2/D3, AUTO-KEEP, GUARANTEED) as negative evidence. This overestimates negatives and removes true negatives from the confusion matrix. A better simulation would separate relevance signals from sentiment polarity and allow neutral or positive outcomes when the title is informational or improvement-focused.
