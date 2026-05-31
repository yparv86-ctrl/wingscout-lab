import os
import json
import urllib.request
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# 1. SETUP TARGETS & API KEY
# Replace this URL with a local tournament listing site, school sports blog, or academy page
TARGET_URL = "https://example-delhi-ncr-sports.com/tournaments" 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBx125fwy9oDXIQMiKjF5v9tbw2Okl-MWs")

client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_raw_text(url):
    """Fetches public HTML content and strips it down to clean raw text strings."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"Error scraping target source line: {e}")
        return ""

def extract_tournaments_with_ai(web_text):
    """Uses Gemini to find football tournaments inside raw webpage text and structure them."""
    if not web_text:
        return []
        
    prompt = f"""
    You are an automated data ingestion pipeline. Review the following raw text scraped from a regional sports website.
    Extract all upcoming youth football/soccer tournaments, leagues, or sports meets happening in Gurugram, Delhi NCR, or nearby regions.
    
    Format the output as a strict JSON list of objects. Do not wrap it in markdown code blocks.
    Each object inside the JSON list MUST have exactly these keys:
    - "title": Name of the tournament
    - "sport": Must be exactly "football"
    - "date": Date string or "TBD"
    - "age_group": Age bracket (e.g., "U-14", "U-17", "All Ages")
    - "venue": Specific venue or school name in Gurugram/NCR
    - "link": Use "{TARGET_URL}" if a specific link isn't found
    - "type": Explicitly "offline" or "online"
    
    Raw Scraped Text Content:
    {web_text[:8000]} 
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1 # Low temperature for factual, rigid extractions
            )
        )
        cleaned_text = response.text.strip()
        # Clean up any accidental markdown wrapper strings if the AI included them
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("\n", 1)[1].rsplit("\n", 1)[0]
        return json.loads(cleaned_text.strip())
    except Exception as e:
        print(f"AI Extraction matrix fault: {e}")
        return []

def main():
    print("Initializing automatic vector crawl...")
    raw_content = fetch_raw_text(TARGET_URL)
    
    if not raw_content:
        print("Empty extraction pool. Aborting sequence.")
        return
        
    new_nodes = extract_tournaments_with_ai(raw_content)
    print(f"AI discovered {len(new_nodes)} tournament nodes.")
    
    if new_nodes:
        # Overwrite or merge into tournaments.json
        with open("tournaments.json", "w") as f:
            json.dump(new_nodes, f, indent=4)
        print("Database arrays successfully updated locally.")

if __name__ == "__main__":
    main()