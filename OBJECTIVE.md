Research Context:

Geospatial Sentiment Analysis: A Hybrid NLP Approach for Mapping Traffic Enforcement Grievances in Cebu City

The proliferation of digital platforms has transformed social media into a primary channel 
for public discourse, particularly regarding urban challenges like traffic and transportation. In 
Cebu City, citizens frequently vent their frustrations about gridlock, apprehension, and 
infrastructure failures on platforms like Reddit. However, this massive volume of 
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


TechStack:
Frontend: React, Tailwind.css
Backend: Python
Database:Supabase

Project Title: SentiMap: A Hybrid NLP Geospatial Dashboard for Cebu City Traffic Grievances

1. Project Overview & Research Context
I am developing "SentiMap," a real-time, citizen-driven monitoring system that maps public grievances regarding traffic enforcement in Cebu City.

The Problem: Vast amounts of digital grievances on platforms like Reddit are unstructured and untapped. Current English-trained NLP models fail to accurately interpret local social media discourse due to the unique morphological structure of Cebuano (Bisaya), the prevalence of "Bislish" (Cebuano-English code-switching), and a heavy cultural reliance on sarcasm (e.g., "Hayahay kaayo ang traffic!" meaning "The traffic is so comfortable!" which is linguistically positive but contextually negative).

The Solution: A "Hybrid Geospatial NLP Framework" that couples a custom domain-specific Cebuano Sentiment Lexicon (handling slang, curses, and sarcasm) with a Machine Learning classifier and a Geolocation module to extract specific traffic hotspots (e.g., "Mambaling", "SRP").

2. The Conceptual Framework
The system processes unstructured social media noise into a structured data visualization pipeline:

Data Ingestion: Harvesting raw, citizen-driven text data (currently via no-code scraping of Reddit).

Hybrid NLP Engine: * Sentiment Analysis: Custom lexicon + ML classifier to decode Bislish and sarcasm.

Geolocation Extraction: Identifying specific Cebu City locations mentioned in the text.

Visualization: A frontend dashboard and "Heatmap of Public Grievances" for traffic authorities.

3. Current Technical Architecture (Decoupled Full-Stack)

Data Layer: Currently using a local Excel file (reddit_data.xlsx) containing Reddit post URLs, titles, timestamps, upvotes, and comments.

Backend (Data Processing & API):

Stack: Python 3.14, FastAPI, Pandas, Uvicorn, OpenPyXL.

Environment: Running in a local virtual environment (venv).

Logic: A GET /api/data endpoint reads the .xlsx file, cleans raw scraper column names (e.g., converting "Faceplate-screen-reader-content" to "title"), formats numerical data, and serves structured JSON. CORSMiddleware is enabled.

Frontend (UI & Dashboard):

Stack: Next.js (v16+, App Router), React, Tailwind CSS, Axios.

Environment: Running on localhost:3000.

Logic: A client-side component (SentiMapDashboard) fetches data from http://127.0.0.1:8000/api/data on load and dynamically maps it into a responsive UI grid of "Grievance Cards" displaying the text, engagement metrics, and Reddit links.

4. Current State & Immediate Goals
Both the frontend and backend are successfully communicating locally. The basic data pipeline (Excel -> Python API -> Next.js UI) is fully functional.
My next phases involve integrating the actual Hybrid NLP engine (sentiment + location extraction) into the Python backend and adding the mapping/heatmap visualization to the Next.js frontend.

5. Instructions for AI Assistant
When answering my prompts, keep this full stack and research context in mind. Ensure that backend solutions prioritize Python/FastAPI best practices for ML integration, and frontend solutions align with Next.js/Tailwind paradigms. Pay special attention to how data structures need to evolve to support the Cebuano Sentiment Lexicon and geospatial mapping.




Data Source (Reddit – Ultimate Web Scraper) 
Took messy raw data from reddit using Ultimate Web Scraper Extension and placed it in /backend/data  

Processing Plant (Pandas) - Inside main.py, you called in Pandas. 
In main.py the code tells to Open this Excel file, throw away the columns I don't like, and rename the confusing ones.Transformed “Faceplate-screen-reader-content" (the scraper's name) into "title" (the human name). This is called Data Cleaning. 

Translator (FastAPI) - Next, you used FastAPI to create a bridge. 
Created an "Endpoint" at /api/data. When someone visits that URL, FastAPI runs your Pandas cleaning script and converts the result into JSON. Web browsers and apps can't easily "read" an Excel file, but they love reading JSON. You’ve turned a static file into a live web service. 

Security Guard (CORS) - Added CORS Middleware to your code. 
Told your backend, "If a website at port 3000 (your frontend) asks for data, let them in." Without this, your browser would block the data for security reasons. You've officially "unlocked" the gate for your Next.js app. 

Why is this a pro setup 
Separation of Concerns: Your data logic is completely separate from your design. If you ever want to change your Excel file to a real SQL database, you only have to change 2 lines of code in the backend—the frontend won't even notice the difference. 
Efficiency: Because of the --reload flag, your "Processing Plant" is always live. If you add 100 more rows to your Excel file right now, your API will show them the second you hit refresh. 


1. The "Uvicorn" Engine 

When you run uvicorn main:app --reload, you are starting a web server. 

main:app: Tells the server to look in your main.py file for the app (the FastAPI brain). 

--reload: This is a developer's best friend. It watches your files. In your logs, you see StatReload detected changes. That happened because as soon as you saved your code, the server "rebooted" itself in half a second so your changes were live immediately. 

2. The "Handshake" (The 200 OK) 

In your terminal, you see lines like: INFO: 127.0.0.1 - "GET /api/data HTTP/1.1" 200 OK 

GET: This is your browser asking, "Hey, can I have the data?" 

/api/data: This is the specific "room" or address the browser visited. 

200 OK: This is the universal internet code for "Success!" It means the Python code found the Excel file, processed it, and handed it over without any errors. 

3. JSON: The Universal Language 

Look at your browser screenshot. See all those curly braces { } and square brackets [ ]? That is JSON. Python (Backend) uses JSON to talk to Next.js (Frontend). 

Excel is for humans to read. 

JSON is for apps to read. By seeing that screen, you’ve confirmed that your backend is successfully "translating" your Excel sheet into a format your website can understand. 

4. What's happening in the "Brain" (main.py) 

When you clicked "Execute" in the browser: 

FastAPI heard the request. 

Pandas (the data library) rushed to your data folder and opened reddit_data.xlsx. 

It stripped away the messy scraper names and kept only the 5 columns we asked for. 

It cleaned the "Upvotes" so they are pure numbers (no "k" or "votes" text). 

It sent that clean list back to your browser. 

You now have a working data source. The next big step is to tell your Frontend (Next.js) to go to http://127.0.0.1:8000/api/data, grab that JSON, and display it as beautiful cards on your website instead of raw text. 



