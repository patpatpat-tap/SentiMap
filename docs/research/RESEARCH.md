Geospatial Sentiment Analysis: A Hybrid NLP Approach for Mapping Traffic Enforcement 
Grievances in Cebu City 

The proliferation of digital platforms has transformed social media into a primary channel 
for public discourse, particularly regarding urban challenges like traffic and transportation. In 
Cebu City, citizens frequently vent their frustrations about gridlock, apprehension, and 
infrastructure failures on platforms like Facebook and Reddit. However, this massive volume of 
data remains unstructured and untapped by government agencies. This study argues that by 
harvesting and analyzing these digital grievances, we can create a real-time, citizen-driven 
monitoring system. Unlike traditional methods that rely on slow, manual complaint filing, this 
research posits that an automated, geospatial sentiment analysis system can serve as an immediate 
sensor for urban anomalies, allowing traffic authorities to identify and visualize "hotspots" of 
dissatisfaction as they happen. 

Existing literature in Natural Language Processing (NLP) has extensively explored sentiment 
analysis for major languages like English and Tagalog. Studies by researchers such as Imperial et 
al. (2022) and various works on "Taglish" code-switching have successfully demonstrated the use 
of machine learning to categorize public opinion. Furthermore, urban planning studies have long 
established the value of Geographic Information Systems (GIS) for plotting accident data and 
traffic volume. However, current research predominantly focuses on high-resource languages or 
formal text sources like news articles. While some recent attempts, such as "CEBUANER," have 
begun to build datasets for Cebuano Named Entity Recognition, the prevailing methodologies still 
rely heavily on translation-based approaches (translating Cebuano to English before analysis), 
which often strips away the cultural nuance and emotional weight of the original text. 

Despite these advancements, there remains a critical "Language-Context Gap" in the current 
technology. Standard sentiment analysis tools (like VADER or TextBlob) utterly fail when applied 
to informal Cebuano (Bisaya), specifically due to its unique morphological structure, the 
prevalence of "Bislish" (Cebuano-English code-switching), and the culture's heavy reliance on 
sarcasm. For instance, a phrase like "Hayahay kaayo ang traffic!" (The traffic is so comfortable!) 
is linguistically positive but contextually negative—a nuance that current English-trained models 
misinterpret. Furthermore, there is no existing system that successfully integrates this vernacular 
sentiment analysis directly with geospatial mapping for the specific domain of traffic 
enforcement in Cebu. The data exists, but the tool to decode it and map it does not. 

This study aims to bridge this gap by developing a "Hybrid Geospatial NLP Framework" 
specifically tailored for Cebuano traffic discourse. Instead of relying on simple translation, the 
researchers will construct a domain-specific Cebuano Sentiment Lexicon, a custom dictionary of 
local slang, curses, and sarcastic descriptors integrated with a Machine Learning classifier to detect 
context and code-switching accurately. This "Hybrid" engine will then be coupled with a 
geolocation module to extract location mentions (e.g., "Mambaling," "SRP") from the text. By 
converting unstructured, sarcastic social media noise into a structured Heatmap of Public 
Grievances, this research will provide the first linguistically accurate, real-time visualization tool 
for monitoring traffic enforcement hotspots in Cebu City. 