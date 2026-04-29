import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", "app", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

url = f"{SUPABASE_URL}/rest/v1/posts"
params = {
    "select": "title,body,full_text",
    "title": "ilike.*Starbuks, Slater and Kryz*"
}
resp = requests.get(url, headers=HEADERS, params=params)
if resp.status_code == 200:
    posts = resp.json()
    for p in posts:
        print("TITLE:", p["title"])
        print("BODY:", p["body"])
        print("FULL_TEXT:", p["full_text"])
else:
    print("Error", resp.text)
