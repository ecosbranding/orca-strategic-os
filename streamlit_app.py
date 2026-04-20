import streamlit as st
import requests
import json
import random
from urllib.parse import urlparse

from database import init_db, save_analysis, get_history

# ==============================
# INIT DB
# ==============================

init_db()

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="ORCA SaaS", layout="wide")

st.title("ORCA Strategic OS - SaaS")

# ==============================
# API KEY
# ==============================

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================
# LOGIN SIMPLE (MVP)
# ==============================

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.subheader("Login")

    user = st.text_input("Usuario")
    if st.button("Entrar"):
        if user:
            st.session_state.user = user
            st.rerun()

    st.stop()

# ==============================
# LOGGED IN
# ==============================

st.sidebar.write(f"Usuario: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ==============================
# GEMINI
# ==============================

def call_gemini(prompt):

    if not GEMINI_API_KEY:
        return "Error: API Key faltante"

    models = ["gemini-1.5-pro", "gemini-1.5-flash"]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)

            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]

        except:
            continue

    return "Error Gemini"

# ==============================
# SCRAPING SIMULADO
# ==============================

def scrape(url):
    domain = urlparse(url).netloc

    return {
        "url": url,
        "platform": "Instagram" if "instagram" in domain else "TikTok" if "tiktok" in domain else "Web",
        "followers": random.randint(1000, 90000),
        "engagement": round(random.uniform(1, 9), 2)
    }

# ==============================
# PROMPT
# ==============================

def build_prompt(data, location):
    return f"""
Eres ORCA SaaS Analyst.

Datos:
{json.dumps(data, indent=2)}

Ubicación: {location}

Entrega:
- Marketing
- Estrategia
- Contenido 7 días
- Optimización negocio
"""

# ==============================
# UI
# ==============================

st.subheader("Nuevo análisis")

urls = st.text_area("URLs")
location = st.text_input("Ubicación", "Quito")

if st.button("Analizar"):

    if not urls:
        st.error("Faltan URLs")
    else:

        data = []
        for u in urls.split("\n"):
            if u.strip():
                data.append(scrape(u.strip()))

        prompt = build_prompt(data, location)

        result = call_gemini(prompt)

        st.markdown("## Resultado")
        st.write(result)

        save_analysis(st.session_state.user, urls, result)

# ==============================
# HISTORIAL
# ==============================

st.subheader("Historial")

history = get_history(st.session_state.user)

for h in history[:10]:
    st.markdown("---")
    st.write("Input:", h[0])
    st.write("Fecha:", h[2])
    st.write(h[1])
