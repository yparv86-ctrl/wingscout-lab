import os
import sys
import json
import urllib.request
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# --- ARCHITECTURAL CONFIGURATION ---
TARGET_URL = "https://example-delhi-ncr-sports.com/tournaments" 
DATABASE_FILE = "tournaments.json"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBx125fwy9oDXIQMiKjF5v9tbw2Okl-MWs")

# Target schema definition for validation and AI alignment
EXPECTED_SCHEMA = {
    "type": "object",
    "properties": {
        "tournaments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string"},
                    "location": {"type": "string"},
                    "age_group": {"type": "string"}
                },
                "required": ["title", "date", "location", "age_group"]
            }
        }
    },
    "required": ["tournaments"]
}

def fetch_html_content(url):
    """Fetches raw HTML content from the target URL down the network interface."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 WingScoutScraper/2.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"[NETWORK ERROR] Failed to reach target surface matrix: {e}")
        return None

def deterministic_parse(html_content):
    """
    LAYER 1: Standard Deterministic Parsing
    Attempts to extract data via classic BeautifulSoup4 selectors.
    """
    if not html_content:
        return None
        
    soup = BeautifulSoup(html_content, "html.parser")
    tournaments = []
    
    # Simulating standard structural extraction (Adjust selectors based on target structure if needed)
    # e.g., soup.find_all('div', class_='match-card-v2')
    cards = soup.find_all('div', class_='match-card-v2') or soup.find_all('tr', class_='tournament-row')
    
    for card in cards:
        try:
            title = card.find('h3').get_text(strip=True) if card.find('h3') else None
            date = card.find('span', class_='date').get_text(strip=True) if card.find('span', class_='date') else "TBD"
            location = card.find('span', class_='venue').get_text(strip=True) if card.find('span', class_='venue') else "Gurugram"
            age_group = card.find('span', class_='age').get_text(strip=True) if card.find('span', class_='age') else "All Ages"
            
            if title:
                tournaments.append({
                    "title": title,
                    "date": date,
                    "location": location,
                    "age_group": age_group
                })
        except Exception:
            continue # Resilient to minor missing elements inside individual cards
            
    return {"tournaments": tournaments} if tournaments else None

def ai_fallback_reconstruction(html_content):
    """
    LAYER 2: Autonomous LLM Reconstruction
    Triggered when standard parsing returns empty. Strips text noise and passes 
    raw DOM text tokens straight to Gemini 2.5 Flash using strict structural schemas.
    """
    print("[FALLBACK TRIGGERED] Initializing Autonomous LLM Reconstruction Layer...")
    
    soup = BeautifulSoup(html_content, "html.parser")
    # Clean up non-informational script and style tags to conserve input context window token capacity
    for element in soup(["script", "style", "header", "footer", "nav"]):
        element.extract()
        
    # Extract raw, unformatted text payload with structured separators
    raw_text = soup.get_text(separator=' ', strip=True)
    
    if not raw_text or len(raw_text) < 100:
        print("[CRITICAL] Raw text payload extraction pool is insufficient or empty.")
        return None

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        system_instruction = (
            "You are an expert sports data engineer operating an autonomous ingestion pipeline. "
            "Analyze the raw, unformatted scraped webpage text provided and extract all upcoming "
            "youth football/soccer tournaments, leagues, cups, or trials taking place in Gurugram, Delhi NCR, or nearby regions. "
            "Normalize unrenderable text walls or irregular dates into structured strings."
        )
        
        prompt = f"Extract all relevant football tournament arrays from this raw scraped web content:\n\n{raw_text[:10000]}"
        
        # Call Google GenAI SDK using structured output definitions
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1, # Low temperature ensures strict adherence to structural layout realities
                response_mime_type="application/json",
                response_schema=EXPECTED_SCHEMA
            )
        )
        
        # Parse output safely as verified structural JSON data
        return json.loads(response.text.strip())
        
    except Exception as e:
        print(f"[AI EXCEPTION ERROR] Extraction pipeline failure: {e}")
        return None

def main():
    print("[1/4] Initiating external vector crawl sequence...")
    html_data = fetch_html_content(TARGET_URL)
    
    if not html_data:
        print("[CIRCUIT BREAKER] Aborting run due to total network extraction failure. Storage protected.")
        sys.exit(1)
        
    # --- LAYER 1: DETERMINISTIC PARSE ---
    print("[2/4] Executing Layer 1 (Deterministic BeautifulSoup Parsing)...")
    dataset = deterministic_parse(html_data)
    
    # --- LAYER 2: VALIDATION CHECK & FALLBACK TRIGGER ---
    if not dataset or not dataset.get("tournaments") or len(dataset["tournaments"]) == 0:
        print("[VALIDATION WARNING] Layer 1 returned 0 entries. DOM Mutation Trap suspected.")
        dataset = ai_fallback_reconstruction(html_data)
        
    # --- LAYER 3: THE CIRCUIT BREAKER ---
    if not dataset or not dataset.get("tournaments") or len(dataset["tournaments"]) == 0:
        print("\n======================================================================")
        print("[CIRCUIT BREAKER CRITICAL FAILURE] Both parsing pipelines returned 0 results.")
        print("Halting process. Execution aborted to protect database files on disk.")
        print("======================================================================")
        # Exiting with a non-zero code tells GitHub Actions that the build failed,
        # stopping the workflow run completely BEFORE it can commit empty files.
        sys.exit(1)
        
    # --- LAYER 4: SAFE COMMIT TO STORAGE ---
    print(f"[3/4] Integrity validation passed. {len(dataset['tournaments'])} tournament nodes secured.")
    try:
        # Remap root object wrapper array back to match your original schema layout if required
        final_array = dataset["tournaments"]
        
        with open(DATABASE_FILE, "w") as f:
            json.dump(final_array, f, indent=4)
        print(f"[4/4] Ingestion successful. Fresh updates pushed to '{DATABASE_FILE}'.")
        
    except Exception as e:
        print(f"[WRITE FAULT] Failed to commit changes to database tracking files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()