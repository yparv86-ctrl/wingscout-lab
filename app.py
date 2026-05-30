import streamlit as st
import json
import os
import urllib.parse
from google import genai
from google.genai import types

# --- 1. CONFIGURATION & PRODUCTION STORAGE MANAGEMENT ---
DATABASE_FILE = "tournaments.json"
WATCHLIST_FILE = "watchlist.json"
PROFILE_FILE = "profile.json"
GEMINI_API_KEY = "AIzaSyBx125fwy9oDXIQMiKjF5v9tbw2Okl-MWs"  # <-- Your production API key is preserved!

# Safe Initialization of the Core Gemini Engine
client = genai.Client(api_key=GEMINI_API_KEY)

def load_data(file_path):
    """Production data parser with built-in format containment."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                if not content:
                    return [] if "json" in file_path else {}
                if content.startswith("```"):
                    content = content.split("\n", 1)[1]
                if content.endswith("```"):
                    content = content.rsplit("\n", 1)[0]
                return json.loads(content.strip())
        except Exception as e:
            st.error(f"Ecosystem Data Read Error [{file_path}]: {e}")
            return [] if "json" in file_path else {}
    return [] if "json" in file_path else {}

def save_watchlist(watchlist_data):
    """Ensures data writes securely to persistent disk arrays."""
    try:
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(watchlist_data, f, indent=4)
    except Exception as e:
        st.error(f"Critical Database Write Violation: {e}")

# Core Datasets Extraction
tournaments = load_data(DATABASE_FILE)
watchlist = load_data(WATCHLIST_FILE)
user_profile = load_data(PROFILE_FILE)

# --- 2. UTILITY VECTOR GENERATORS ---
def generate_calendar_url(event):
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    title = urllib.parse.quote(f"🏆 {event.get('title')}")
    details = urllib.parse.quote(f"Sport: {event.get('sport')}\nAge Group: {event.get('age_group')}\nSource: {event.get('link')}")
    location = urllib.parse.quote(event.get('venue', 'Gurugram, India'))
    return f"{base_url}&text={title}&details={details}&location={location}"

def generate_maps_url(venue):
    base_url = "https://www.google.com/maps/search/?api=1&query="
    if "online" in venue.lower() or "discord" in venue.lower():
        return None
    full_query = f"{venue}, Gurugram, Haryana, India"
    return base_url + urllib.parse.quote(full_query)

# --- 3. STARK MINIMALIST DESIGN ARCHITECTURE ---
st.set_page_config(page_title="WingScout Lab | Noir", page_icon="⚽", layout="wide")

# Inject Custom Monochromatic Premium Minimalist CSS
st.markdown("""
    <style>
    /* Absolute Dark Background & Stark Typography */
    .stApp {
        background: #000000;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
    }
    
    /* Elegant Obsidian Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #1A1A1A;
    }
    
    /* Clean Hairline Slate Expanders (Ditching Rounded Corners slightly for a sharper profile) */
    div[data-testid="stExpander"] {
        background: #090909 !important;
        border: 1px solid #1C1C1C !important;
        border-radius: 4px !important;
        margin-bottom: 14px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    div[data-testid="stExpander"]:hover {
        border-color: #4B5563 !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.02);
    }
    
    /* Form Minimalist Containers */
    div[data-testid="stForm"] {
        background: #060606 !important;
        border: 1px solid #1C1C1C !important;
        border-radius: 4px !important;
        padding: 16px !important;
        margin-top: 10px;
    }
    
    /* Translucent Matt-Grey Inputs */
    .stTextInput input {
        background-color: #0E0E0E !important;
        border: 1px solid #262626 !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus {
        border-color: #F3F4F6 !important;
        box-shadow: 0 0 0 1px #F3F4F6 !important;
    }
    
    /* High-Contrast Monochromatic Navigation Tabs */
    button[data-baseweb="tab"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #4B5563 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom-width: 1px !important;
        transition: all 0.2s ease;
    }
    button[data-baseweb="tab"]:hover {
        color: #9CA3AF !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom-color: #FFFFFF !important;
    }
    
    /* Premium Monochromatic Hover Inversion Buttons */
    div.stButton > button {
        background: #0F0F0F !important;
        color: #E5E7EB !important;
        border: 1px solid #262626 !important;
        border-radius: 4px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 8px 16px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button:hover {
        background: #FFFFFF !important;
        color: #000000 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
    }
    
    /* Telemetry Panel Design */
    .telemetry-card {
        background: #080808;
        border: 1px solid #1C1C1C;
        padding: 14px 20px;
        border-radius: 4px;
        text-align: center;
        transition: border-color 0.25s;
    }
    .telemetry-card:hover {
        border-color: #374151;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Identity Header Elements (Stark Design)
st.markdown("<h1 style='color:#FFFFFF; font-weight:800; letter-spacing:-0.8px; margin-bottom:0px; font-size:32px;'>WINGSCOUT LAB</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280; font-size:13px; margin-top:2px; font-weight:600; text-transform: uppercase; letter-spacing: 1.5px;'>Tactical Tournament Intelligence & Winger Analytics</p>", unsafe_allow_html=True)
st.write("")

# --- 4. TELEMETRY SNAPSHOT BAR (MONOCHROME REFACTOR) ---
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown(f"<div class='telemetry-card'><p style='margin:0; color:#4B5563; font-size:10px; font-weight:700; letter-spacing:1px; text-transform: uppercase;'>DATABASE NODES</p><p style='margin:4px 0 0 0; color:#FFFFFF; font-size:20px; font-weight:800;'>{len(tournaments)} Recs</p></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='telemetry-card'><p style='margin:0; color:#4B5563; font-size:10px; font-weight:700; letter-spacing:1px; text-transform: uppercase;'>WATCHLIST</p><p style='margin:4px 0 0 0; color:#FFFFFF; font-size:20px; font-weight:800;'>{len(watchlist)} Targets</p></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='telemetry-card'><p style='margin:0; color:#4B5563; font-size:10px; font-weight:700; letter-spacing:1px; text-transform: uppercase;'>DEPLOYMENT VECTORS</p><p style='margin:4px 0 0 0; color:#FFFFFF; font-size:20px; font-weight:800;'>LW / RW Flank</p></div>", unsafe_allow_html=True)
st.write("")

# --- 5. SIDEBAR CONTROLS ---
st.sidebar.markdown("<p style='color:#4B5563; font-size:11px; font-weight:800; letter-spacing:1.5px; text-transform: uppercase; margin-bottom: 8px;'>👤 ATHLETE BIOMETRICS</p>", unsafe_allow_html=True)
if user_profile:
    st.sidebar.markdown(f"""
    <div style='background: #080808; padding: 14px; border-radius: 4px; border: 1px solid #1C1C1C; border-left: 3px solid #E5E7EB;'>
        <p style='margin:0; color:#4B5563; font-size:9px; font-weight:800; letter-spacing:1px;'>ACTIVE ASSET</p>
        <p style='margin:2px 0 10px 0; color:#FFFFFF; font-weight:800; font-size:17px; letter-spacing:-0.3px;'>{user_profile.get('name')}</p>
        <p style='margin:4px 0; color:#9CA3AF; font-size:12px;'>🏫 <b>School:</b> {user_profile.get('school_name')}</p>
        <p style='margin:4px 0; color:#9CA3AF; font-size:12px;'>🏃‍♂️ <b>Deployment:</b> {user_profile.get('position_or_role')}</p>
        <p style='margin:4px 0; color:#9CA3AF; font-size:12px;'>📅 <b>Age:</b> U-{user_profile.get('age')} Category</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.warning("No active athlete vector profile detected.")

st.sidebar.divider()
st.sidebar.markdown("<p style='color:#4B5563; font-size:11px; font-weight:800; letter-spacing:1.5px; text-transform: uppercase; margin-bottom: 8px;'>🎯 RUNTIME CONTROLS</p>", unsafe_allow_html=True)
search_query = st.sidebar.text_input("🔍 Filter Keywords:", "").lower()

all_ages = ["All Categories"]
for t in tournaments:
    age = t.get('age_group', 'All Ages')
    if age and age not in all_ages:
        all_ages.append(age)

selected_age = st.sidebar.selectbox("👥 Restrict Age Bracket:", all_ages)


def render_tournament_bot(event, unique_key):
    """Production execution container handling layout rendering and persistent session matrices."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        venue_text = event.get('venue', 'N/A')
        st.markdown(f"🧬 **Age Parameters:** <span style='color:#FFFFFF; font-weight:600;'>{event.get('age_group', 'All Ages')}</span>", unsafe_allow_html=True)
        st.markdown(f"🔗 [Access Registration Channel]({event.get('link', '#')})")
        
        maps_url = generate_maps_url(venue_text)
        if maps_url:
            st.markdown(f"📍 **Coordinates:** {venue_text} — [🗺️ Map View]({maps_url})")
        else:
            st.markdown(f"📍 **Coordinates:** {venue_text}")
    
    with col2:
        cal_url = generate_calendar_url(event)
        st.markdown(
            f'<a href="{cal_url}" target="_blank" style="text-decoration:none;">'
            f'<button style="background-color:#0A0A0A; color:#FFFFFF; border:1px solid #222222; padding:8px 16px; '
            f'border-radius:4px; cursor:pointer; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; width:100%; margin-bottom:10px;'
            f'transition: all 0.2s;">📅 Log to Calendar</button></a>', 
            unsafe_allow_html=True
        )
        
        is_bookmarked = any(w.get('title') == event.get('title') for w in watchlist)
        if is_bookmarked:
            if st.button("❌ Drop from Watchlist", key=f"watch_{unique_key}"):
                updated_watchlist = [w for w in watchlist if w.get('title') != event.get('title')]
                save_watchlist(updated_watchlist)
                st.rerun()
        else:
            if st.button("⭐ Secure to Watchlist", key=f"watch_{unique_key}"):
                watchlist.append(event)
                save_watchlist(watchlist)
                st.rerun()

    # --- UNIQUE SESSION STATE REGISTRIES TO SURVIVE UI RE-RENDERS ---
    report_key = f"report_data_{unique_key}"
    counter_key = f"counter_data_{unique_key}"
    saved_opp_key = f"saved_opp_{unique_key}"

    # --- ADVANCED PERSONALIZED BLUEPRINT GENERATOR ---
    st.markdown("<p style='color:#6B7280; font-weight:700; margin-top:15px; margin-bottom:5px; font-size:11px; letter-spacing:1px; text-transform:uppercase;'>📊 ANALYTIC SUITE</p>", unsafe_allow_html=True)
    
    if st.button("⚡ Compile Custom Tactical Blueprint", key=f"btn_report_{unique_key}"):
        with st.spinner("🧠 Syncing environmental vectors and analyzing playstyle parameters..."):
            scout_prompt = f"""
            You are an elite professional athletic sports scout and tactical advisor. 
            Generate a comprehensive, hyper-personalized scouting report specifically tailored for THIS athlete entering this tournament.
            
            ATHLETE PROFILE DATA:
            - Name: {user_profile.get('name')}
            - Current School/Club: {user_profile.get('school_name')}
            - Target Age Group: U-{user_profile.get('age')}
            - Playing Position/Role: {user_profile.get('position_or_role')}
            - Physical Attributes: {user_profile.get('physicality')}
            - Mental Attributes: {user_profile.get('mentality')}
            
            TOURNAMENT SPECS:
            - Title: {event.get('title')}
            - Sport: {event.get('sport')}
            - Venue: {event.get('venue')}
            - Competition Age Bracket: {event.get('age_group')}
            
            Use Google Search grounding to evaluate regional competition context for this specific age tier in Gurugram/Delhi NCR.
            
            Structure your response into these personalized bold markdown sections:
            1. 🎯 Your Personal Matchup Difficulty (Analyze how the tournament's age/skill bracket fits their specific age, playing role, and school)
            2. 🏟️ Custom Venue Adaptation Guidelines (Tell them EXACTLY how to adjust their specific playstyle/position role based on field surfaces and heat metrics)
            3. ⚔️ Direct Tactical Exploits & Warnings (Address their specific strengths and weaknesses from the profile. Give explicit steps to exploit their strengths and hide their weaknesses)
            4. 📋 My Custom Pre-Game Gameplan (Provide step-by-step physical, mental, and spatial instructions tailored exactly to their playing style)
            """
            try:
                config = types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.7
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=scout_prompt,
                    config=config
                )
                st.session_state[report_key] = response.text
            except Exception as e:
                st.error(f"Failed to compile tactical layout: {e}")

    # Persistent Display Logic (Refined Monochrome Slate Box)
    if report_key in st.session_state:
        st.markdown("<div style='background:#090909; padding:15px; border-radius:4px; border:1px solid #262626; margin-top:10px; font-size:14px; line-height:1.6;'>", unsafe_allow_html=True)
        st.markdown(st.session_state[report_key])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        if st.button("🗑️ Purge Blueprint Matrix", key=f"clear_report_{unique_key}"):
            del st.session_state[report_key]
            st.rerun()

    # --- ISOLATED OPPONENT COUNTER FORM BLOCK ---
    st.write("")
    st.markdown("<p style='color:#6B7280; font-weight:700; margin-bottom:5px; font-size:11px; letter-spacing:1px; text-transform:uppercase;'>🛡️ COUNTER-TACTICS SYSTEM</p>", unsafe_allow_html=True)
    
    with st.form(key=f"form_tactics_{unique_key}"):
        opponent_name = st.text_input(
            "Identify Target Opposing Unit (School / Academy):",
            placeholder="E.g., Pathways, Amity, DPS Gurugram..."
        )
        submit_tactics = st.form_submit_button("🔮 Initialize Counter-Intercept Matrix")
        
    if submit_tactics:
        if not opponent_name:
            st.warning("Input required before vector interception.")
        else:
            with st.spinner(f"🕵️‍♂️ Fetching regional athletic matrices for {opponent_name}..."):
                tactical_prompt = f"""
                You are an elite professional football tactician. Generate a highly strategic, customized counter-tactics scouting report.
                
                YOUR ATHLETE'S PROFILE:
                - Name: {user_profile.get('name')}
                - School: {user_profile.get('school_name')}
                - Position: {user_profile.get('position_or_role')}
                - Physical Profile: {user_profile.get('physicality')}
                - Mental Profile: {user_profile.get('mentality')}
                
                THE OPPONENT TO SCOUT:
                - Target Opponent Team: {opponent_name}
                - Tournament Context: {event.get('title')}
                - Sport/Age: {event.get('sport')} ({event.get('age_group')})
                
                Use Google Search grounding to discover any regional context about {opponent_name}'s athletic performance, school football reputation in Gurugram/Delhi NCR, or typical tournament structures they excel in.
                
                Structure your report into these bold markdown headers:
                1. 🔍 Opponent Intelligence Overview (Analyze their school sports reputation/threat level)
                2. ⚔️ Flank Exploits for Parv (Give explicit tactical steps on how Parv, playing as a Winger, can use his dribbling strength to target their fullbacks)
                3. 🛡️ Neutralizing Their Counter-Press (Address Parv's shielding weakness and tell him exactly how to avoid getting physically trapped by {opponent_name}'s defensive system)
                4. 🧠 Conquering the Internal Mind Game (Give Parv 2 mental triggers to bypass his self-doubt specifically when facing this rival team)
                """
                try:
                    config = types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.7
                    )
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=tactical_prompt,
                        config=config
                    )
                    st.session_state[counter_key] = response.text
                    st.session_state[saved_opp_key] = opponent_name
                except Exception as e:
                    st.error(f"Failed to calculate defensive bypass variables: {e}")

    # Persistent Display Logic (Refined Monochrome Slate Box)
    if counter_key in st.session_state:
        st.markdown("<div style='background:#090909; padding:15px; border-radius:4px; border:1px solid #262626; margin-top:10px; font-size:14px; line-height:1.6;'>", unsafe_allow_html=True)
        st.markdown(st.session_state[counter_key])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        if st.button("🗑️ Flush Counter Matrix", key=f"clear_counter_{unique_key}"):
            del st.session_state[counter_key]
            del st.session_state[saved_opp_key]
            st.rerun()

    # --- BASE PLATFORM CHAT BOT ---
    st.write("")
    st.markdown("<p style='color:#6B7280; font-weight:700; margin-bottom:5px; font-size:11px; letter-spacing:1px; text-transform:uppercase;'>💬 COGNITIVE COACH INTERFACE</p>", unsafe_allow_html=True)
    
    with st.form(key=f"form_chat_{unique_key}"):
        user_question = st.text_input("Query advisor regarding mechanics, regulations, or strategy vectors:")
        submit_chat = st.form_submit_button("✉️ Dispatch Stream Query")
        
    if submit_chat and user_question:
        with st.spinner("🧠 Querying cognitive neural models..."):
            bot_prompt = f"""
            You are a helpful personal sports scout coach. Answer this question comprehensively.
            Always customize your answer for this specific athlete:
            Athlete Name: {user_profile.get('name')} | Position: {user_profile.get('position_or_role')} | Physicality: {user_profile.get('physicality')} | Mentality: {user_profile.get('mentality')}
            
            Tournament: {event.get('title')} | Venue: {event.get('venue')}
            User Question: {user_question}
            """
            try:
                config = types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.7
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=bot_prompt,
                    config=config
                )
                st.info(response.text)
            except Exception as e:
                st.error(f"Advisor link dropped: {e}")


# --- 6. CORE DESERIALIZATION FILTER RUNTIME ---
filtered_tournaments = []
for t in tournaments:
    matches_search = search_query in t.get('title', '').lower() or search_query in t.get('sport', '').lower()
    matches_age = (selected_age == "All Categories") or (t.get('age_group') == selected_age)
    if matches_search and matches_age:
        filtered_tournaments.append(t)


# --- 7. COMPONENT ROUTER DISPLAY TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["⚽ Football Hub", "🏀 Alternate Sports", "🌐 Simulation Vectors", "⭐ Watchlist Matrix"])

with tab1:
    football_events = [t for t in filtered_tournaments if t.get('sport', '').lower() == 'football']
    if not football_events:
        st.info("No active football nodes matching filter fields.")
    for idx, event in enumerate(football_events):
        with st.expander(f"➔ {event.get('title', 'Unknown Node')} — [{event.get('date', 'TBD')}]"):
            render_tournament_bot(event, f"fb_{idx}")

with tab2:
    other_events = [t for t in filtered_tournaments if t.get('sport', '').lower() != 'football' and t.get('type', '').lower() == 'offline']
    if not other_events:
        st.info("No offline sports configurations registered.")
    for idx, event in enumerate(other_events):
        with st.expander(f"➔ {event.get('title', 'Unknown Node')} — [{event.get('sport').upper()}]"):
            render_tournament_bot(event, f"other_{idx}")

with tab3:
    online_events = [t for t in filtered_tournaments if t.get('type', '').lower() == 'online']
    if not online_events:
        st.info("No digital network channels currently listening.")
    for idx, event in enumerate(online_events):
        with st.expander(f"🎮 {event.get('title', 'Digital Vector')}"):
            render_tournament_bot(event, f"online_{idx}")

with tab4:
    if not watchlist:
        st.info("Watchlist array empty. Secure tournament vectors to register active tracking markers.")
    for idx, event in enumerate(watchlist):
        with st.expander(f"⭐ {event.get('title', 'Pinned Node')} — [{event.get('date', 'TBD')}]"):
            render_tournament_bot(event, f"watch_tab_{idx}")