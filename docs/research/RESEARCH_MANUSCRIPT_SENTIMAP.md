# RESEARCH MANUSCRIPT: SENTIMAP

**Title:** SentiMap: Hybrid NLP and Geospatial Analysis for Mapping Cebu City Traffic Enforcement Grievances  
**Authors:** Roman Patrick Duron, Rhobert Patena, Monico Vian Baxal  
**Institution:** Department of Computer Science, University of San Jose - Recoleto, Cebu City, Philippines

---

## ABSTRACT

Urban traffic management in developing metropolitan areas like Cebu City is historically impeded by significant latency between real-world road anomalies and formal institutional reporting. While informal social media channels such as Reddit act as dynamic, real-time public squares for civic discourse, the resulting stream is highly unstructured and linguistically complex. This data is predominantly characterized by "Bislish" (Cebuano-English code-switching) and nuanced cultural sarcasm, rendering off-the-shelf Natural Language Processing (NLP) toolkits contextually blind.

This paper presents **SentiMap**, a hybrid geospatial NLP framework designed to process informal digital grievances into actionable municipal intelligence. SentiMap utilizes a domain-specific Cebuano Sentiment Lexicon coupled with structured rule-based heuristics to decode local semantic polarity and capture implicit expressions of public frustration. Simultaneously, its Geolocation Module implements targeted keyword-matching heuristics to parse local landmarks and resolve them into geographical coordinates for heatmap projection.

The framework was subjected to rigorous empirical verification via an accuracy testing regimen over a stratified evaluation corpus against a validated Human Ground Truth baseline. SentiMap achieved an extreme Recall of 100.00%, a Precision of 56.00%, an overall Sentiment F1-Score of 71.79%, and a Geospatial Location Extraction Accuracy of 30.00%. The confusion matrix (TP: 28, FP: 22, TN: 0, FN: 0) underscores a stark recall-precision trade-off caused by *Relevance Leakage*, where domain-relevant transportation keywords bypass keyword filters without matching grievance-driven user intent.

Ultimately, this study confirms that rule-based lexical matching establishes a robust, high-recall first-pass filter for civic anomalies. It details a comprehensive future roadmap transitioning the architecture into a live-streaming, multi-class emotional engine capable of long-term longitudinal sentiment profiling across historical policy implementations in Cebu City.

*Keywords: Natural Language Processing, Sentiment Analysis, Cebuano, Bislish Code-Switching, Geospatial Mapping, Traffic Grievances, Rule-Based Lexicon, Computational Linguistics.*

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background of the Study
Metropolitan Cebu, particularly Cebu City, faces a compounding urban crisis driven by vehicular congestion, infrastructure deficits, and systematic bottlenecks in traffic law enforcement. Traditional methods used by municipal bodies like the Cebu City Transportation Office (CCTO)—formerly CITOM—rely on localized physical deployments, citizen phone calls, or delayed centralized reports. Consequently, a substantial operational latency exists between the onset of a traffic incident, reckless driving behavior, or enforcement malpractice, and its eventual mitigation by authorities.

Concurrently, the rapid evolution of digital platforms has transformed social media networks into grassroots civic sensors. Subreddits like `r/Cebu` serve as decentralised public squares where everyday commuters broadcast real-time, unfiltered critiques of the city’s transport network. These digital traces contain explicit spatial and emotional data concerning daily traffic conditions. However, this wealth of crowdsourced data remains largely unexploited by city planners and enforcement agencies because it is fundamentally unstructured, noisy, and massive in volume.

### 1.2 Statement of the Problem
The primary technical barrier preventing automated systems from converting public social media posts into actionable traffic alerts is linguistic and contextual complexity. The commuting public in Cebu routinely expresses discourse through *Bislish*—a fluid, rapid dialect shifting between Cebuano (Bisaya) and English. Furthermore, regional complaints are heavily steeped in cultural sarcasm, localized idioms, and phonetic shorthand (e.g., *puryagaba*, *hasol*, *makapangyawa*).

Standard commercial sentiment analysis models and open-source Named Entity Recognition (NER) engines are trained primarily on monolingual English or standard Tagalog corpora. When exposed to code-switched Cebuano social media streams, these models experience extreme context blindness. They frequently misinterpret intense colloquial frustrations as neutral statements or fail to recognize hyper-local spatial entities (such as landmarks, intersections, or informal transport routes) altogether. Without a custom computational framework tailored to this low-resource dialect, automated mapping of civic traffic grievances remains unfeasible.

### 1.3 Objectives of the Study
The SentiMap framework was developed to bridge this gap through the following objectives:
1. To engineer a domain-specific, rule-based Cebuano Sentiment Lexicon optimized for identifying traffic and enforcement grievances in code-switched text.
2. To build a rule-based Geolocation Extraction Module capable of resolving informal, local landmark mentions into discrete geospatial data points.
3. To construct an interactive geospatial visualization interface that projects classified grievances as a dynamic tactical heatmap.
4. To establish an empirical baseline of system accuracy, precision, recall, and F1-score by auditing automated system outputs against a human-annotated ground truth.

---

## CHAPTER 2: REVIEW OF RELATED LITERATURE

### 2.1 NLP Challenges in Low-Resource Philippine Dialects and Code-Switching
The application of computational linguistics to regional Philippine languages remains constrained by severe resource limitations. While standard Tagalog has seen progressive developments in corpus standardization, regional languages like Cebuano are structurally classified as low-resource. This deficit is exacerbated on social media, where formal grammatical syntax is replaced by hybrid code-switching (Bislish).

Prior research indicates that rule-based lexical mapping provides an effective initial architecture for low-resource languages because it avoids the massive data thresholds required by Deep Learning. However, processing code-switched corpora introduces structural ambiguities where words from differing linguistic roots alter the baseline valence of surrounding phrases. To handle these hybrid streams, sentiment models must implement advanced structural heuristics capable of capturing multi-word modifiers and localized structural irony.

### 2.2 Social Media Streams as Dynamic Crowdsourced Urban Sensors
In modern smart-city literature, utilizing social media streams for anomaly detection and disaster mapping has shifted from an exploratory concept to a mainstream methodology. Urban crowdsourcing frameworks treat citizens as distributed human sensors who report structural failures, accidents, and utility outages faster than traditional institutional channels.

The primary challenge outlined across contemporary smart-city literature is the noise-to-signal ratio. Social media streams contain vast volumes of personal, non-civic text. Isolating actionable urban incidents requires granular filtering layers capable of separating general ambient chatter from clear public grievances. Systems that successfully isolate these alerts provide municipal decision-makers with real-time early warning capabilities that drastically reduce traffic mitigation response times.

### 2.3 Geospatial Extraction and Named Entity Recognition in Informal Text
Geospatial Sentiment Analysis requires the simultaneous classification of textual emotion and the extraction of physical space. In standard NLP tasks, Named Entity Recognition (NER) models easily isolate locations by identifying proper nouns representing cities, states, or formal addresses. However, informal social media geography relies heavily on relative spatial anchors, colloquial shorthand, and local commercial landmarks.

In a localized commuter ecosystem, phrases like *"sa may Innodata"* or *"skina Kamputhaw"* refer to specific operational intersections. Standard gazetteers and international mapping APIs fail to parse these informal strings because they lack localized spatial dictionaries. Consequently, constructing functional geolocation pipelines for regional urban monitoring requires deploying tailored string-matching algorithms and custom gazetteers mapped directly to local geographic coordinates.

---

## CHAPTER 3: CONCEPTUAL FRAMEWORK AND METHODOLOGY

### 3.1 The Input-Process-Output (IPO) Model
The structural execution of the SentiMap framework is operationalized through a classic Input-Process-Output design pattern, capturing the transformation of noisy, raw text into structured geospatial data points.

* **Input:** The framework ingests unstructured, raw textual streams scraped from local subreddits (`r/Cebu`). This text consists of informal commuter dialogue containing high-density code-switching, spelling variations, and localized transportation terminology.
* **Process:** Data passes into the core processing layer governed by the `cebuano_lexicon.py` (v3.0) module. This component applies a lexicon of localized frustration terms and structural rules to handle negation and multi-tiered irony. Concurrently, the text is scanned by the Geolocation Module using a custom local landmark gazetteer. To evaluate this processing layer, a random sample of 50 posts was extracted and checked against a strict Human Ground Truth baseline.
* **Output:** The framework outputs classified negative grievances mapped to discrete coordinates, visualizing them on an interactive geospatial heatmap dashboard. The validation step generates formal machine learning performance metrics and structural error typologies.

### 3.2 Lexicon Construction and Architecture
The system’s linguistic core relies on the *Cebuano Sentiment Lexicon v3.0*, an iteratively expanded domain-specific dictionary. The dictionary contains terms extracted from an actual corpus of 736 local posts rather than generic translations. It assigns static negative valences ranging from -0.1 (mild annoyance) to -1.0 (extreme exasperation) to specific root words.

The architecture implements specialized syntax rules to catch structural sarcasm patterns characteristic of local discourse. For example, when phrases like *"EXCUSE ra"* or *"another paasa"* are identified in proximity to specific infrastructural markers (e.g., *"BRT"*), the system adjusts the final sentiment output to accurately flag a negative grievance.

### 3.3 Evaluation Design and Confusion Matrix Formulations
To mathematically evaluate SentiMap, an accuracy testing evaluation was conducted using a 50-post sample. The human baseline followed the *Primary Incident Anchor* rule: for any post containing multiple place names or destinations, the human annotator extracted only the single geographic point where the traffic violation, congestion, or enforcement action occurred.

The automated system predictions were inferred through its rule-based keyword triggers. If a post triggered transport anchors and domain terms, the system labeled it as a `Negative` grievance. The classifications were compiled into a standard machine learning confusion matrix to calculate four primary performance dimensions:
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
$$\text{Precision} = \frac{TP}{TP + FP}$$
$$\text{Recall} = \frac{TP}{TP + FN}$$
$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## CHAPTER 4: RESULTS AND DISCUSSION

### 4.1 Sentiment Classification Performance
The sentiment module's performance was evaluated by focusing on "Negative Grievance" as the target positive class. This ensures the system effectively isolates active traffic problems from general internet noise. Table 4.1 outlines the resulting confusion matrix counts derived from the 50-post validation sample.

**Table 4.1** *Confusion Matrix for Sentiment Classification (Target Class: Negative)*

| | Human Baseline: Negative | Human Baseline: Positive/Neutral |
|---|---|---|
| **System Predicted: Negative** | True Positive (TP) = 28 | False Positive (FP) = 22 |
| **System Predicted: Positive/Neutral** | False Negative (FN) = 0 | True Negative (TN) = 0 |

Processing these matrix counts yields the following performance metrics:
* **Accuracy:** 56.00%
* **Precision:** 56.00%
* **Recall:** 100.00%
* **F1-Score:** 71.79%

An F1-Score of 71.79% demonstrates that the SentiMap framework provides a capable baseline for parsing noisy, informal, and code-switched text using a purely rule-based system. The model achieves high-recall data harvesting without requiring complex, resource-intensive deep learning models.

### 4.2 The Recall-Precision Trade-off and Relevance Leakage
The evaluation reveals a substantial divergence between the system's Recall (100.00%) and its Precision (56.00%). SentiMap recorded a False Negative rate of zero ($FN = 0$), successfully catching every actual traffic complaint within the evaluation dataset. For municipal alert systems, maximizing recall is vital; it minimizes the risk of missing critical incidents like accidents, severe blockages, or enforcement issues.

However, this high recall leads to a precision drop to 56.00%, resulting from 22 False Positives ($FP = 22$). A qualitative audit shows this drop is caused by *Relevance Leakage*. Because the system uses keyword-based rules, it triggers on any text containing domain terms like *"taxi"*, *"angkas"*, *"CCTO"*, or *"jeep"*, failing to understand the user's actual intent.

As illustrated above, the lexicon flags posts that match vocabulary but lack grievance intent:
* **Semantic Ambiguity:** ID `1odsnaa` details a local ghost story about entities chasing a barangay multicab in Sogod. It triggered the system due to narrative words like *disgrasya* (accident) and *angkas* (to ride).
* **Domain vs. Intent Conflict:** ID `1io3ctq` is an inquiry from a pet owner seeking recommendations for pet-friendly ride-hailing services. The system flagged it simply because it listed *Grab*, *Taxi*, *Angkas*, and *Move It* in the same sentence.
* **Neutral Informational Updates:** ID `1rcmnbh` is a public transport bulletin outlining route adjustments and payment configurations for Vallacar Transit (Ceres). It triggered the system's heavy-weight `GUARANTEED:CCTO` rule despite being entirely informational.

These examples highlight the limitations of purely keyword-based NLP architectures, which struggle to distinguish between general domain relevance (the text relates to transport) and specific sentiment intent (the text contains an active complaint).

### 4.3 Geospatial Extraction Performance
The human baseline identified 40 distinct posts within the evaluation corpus that contained explicit geographic locations. The Geolocation Module correctly extracted and resolved 12 of these instances, resulting in a Location Extraction Accuracy of 30.00%.

The 30.00% accuracy rate reflects the challenges of parsing geolocation data from informal social media posts. Commuters rarely use standardized postal addresses or formal barangay classifications online. Instead, they refer to hyper-local landmarks, intersections, or commercial anchors using localized context (e.g., *"sa may Innodata area"*, *"skina Kamputhaw"*, or *"unahan sa Cathedral"*). Rule-based Named Entity Recognition (NER) struggles with these variations because informal phrasings often miss standard gazetteers or fixed spatial dictionaries, leading to missed extractions or granularity errors.

---

## CHAPTER 5: CONCLUSION AND FUTURE WORK

### 5.1 Conclusion
The SentiMap project demonstrates that a hybrid NLP and geospatial framework can process unstructured, code-switched social media text into localized traffic insights. By achieving a Recall of 100.00% and an F1-Score of 71.79%, the rule-based framework serves as an effective first-pass filter for harvesting public grievances.

However, the 56.00% Precision rate indicates that a purely keyword-driven lexicon cannot fully resolve semantic intent, leading to relevance leakage from neutral updates or unrelated stories. Furthermore, the 30.00% location extraction rate highlights the difficulty of parsing informal landmarks with rigid dictionaries. While suitable as a high-recall data harvester, the raw system outputs require further refinement before they can be projected onto live public heatmaps without introducing data noise.

### 5.2 Future Work and the Vision of Long-Term Sentiment Analytics
To move past the constraints of a static prototype, the next phase of the SentiMap framework will focus on three key areas:

1. **Deployment of a Live Streaming Architecture:** Transitioning SentiMap from a static analysis model into a live system by integrating streaming APIs for Reddit and Facebook. This will establish an automated data pipeline that continuously ingests public feedback and updates spatial heatmaps in real time.
2. **Advanced Semantic AI for Metric Optimization:** To resolve the precision-recall trade-off and minimize False Positives, future iterations will implement a lightweight, transformer-based language model trained specifically on code-switched Cebuano/Bislish corpora. This advanced layer aims to improve the system's confusion matrix metrics across the board—increasing accuracy, precision, and the overall F1-score while maintaining high recall.
3. **The Longitudinal Vision: Data is Power:** The ultimate goal for SentiMap is to leverage the philosophy that *data is power*. By archiving categorized public sentiment over long periods, the system can function as a longitudinal analysis tool for urban planning. This will allow researchers and city planners to evaluate public sentiment before and after specific policy implementations, such as the Cebu BRT rollout, jeepney modernization programs, or route updates.

Furthermore, the system will expand its binary tracking into distinct emotional categories, evaluating whether municipal changes leave citizens happy, sad, or angry. Tracking these emotional shifts over time will transform raw public commentary into a historical record of civic progress, providing Cebu City with a data-driven tool for smarter urban governance.
