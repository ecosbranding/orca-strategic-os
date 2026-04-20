import streamlit as st
import requests
import json
import random
from urllib.parse import urlparse

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="ORCA Strategic OS", layout="wide")

st.title("ORCA Strategic OS")
st.write("Sistema de inteligencia estratégica automatizada")

# ==============================
# API KEY SEGURA (CORRECTO)
# ==============================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = None

if not GEMINI_API_KEY:
    st.error("API Key no configurada en Streamlit Secrets")

# ==============================
# UI STYLE
# ==============================

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stTextArea textarea, .stTextInput input {
    background-color: #1c1f26;
    color: white;
}
.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# GEMINI API (ROBUSTO + SEGURO)
# ==============================

def call_gemini(prompt):

    if not GEMINI_API_KEY:
        return "Error: API Key no disponible"

    models = [
        "gemini-1.0-pro",
        "gemini-1.5-flash"
    ]

    last_error = None

    for model in models:

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)

            if r.status_code != 200:
                last_error = r.text
                continue

            data = r.json()

            if "candidates" not in data:
                last_error = "Respuesta inválida"
                continue

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            last_error = str(e)
            continue

    return f"Error Gemini: {last_error}"

# ==============================
# SCRAPING SIMULADO
# ==============================

def scrape(url):

    domain = urlparse(url).netloc

    return {
        "url": url,
        "platform": (
            "Instagram" if "instagram" in domain
            else "TikTok" if "tiktok" in domain
            else "Web"
        ),
        "followers": random.randint(1000, 90000),
        "engagement_rate": round(random.uniform(1, 9), 2),
        "content_type": random.choice(["Reels", "Educativo", "Ventas", "Lifestyle"]),
        "posting_frequency": random.choice(["Alta", "Media", "Baja"]),
        "brand_tone": random.choice(["Premium", "Casual", "Corporativo"])
    }

# ==============================
# PROMPT ORCA
# ==============================

def build_prompt(data, location):

    return f"""
Eres ORCA Strategic OS (consultoría tipo McKinsey + Silicon Valley).

Datos:
{json.dumps(data, indent=2)}

Ubicación: {location}

Entrega:

1. ESTADÍSTICAS
2. MARKETING (AIDA + estrategia local)
3. DISEÑO (luxury editorial)
4. CONTENIDO (7 días + hooks)
5. NEGOCIO (viabilidad + optimización)

Sé claro, estratégico y accionable.
"""

# ==============================
# INPUTS
# ==============================

urls_input = st.text_area("URLs (una por línea)")
location = st.text_input("Ubicación", "Quito, Ecuador")

# ==============================
# TEST GEMINI
# ==============================

if st.button("TEST GEMINI"):
    st.write(call_gemini("Responde solo OK"))

# ==============================
# EJECUCIÓN
# ==============================

if st.button("Ejecutar análisis"):

    if not urls_input.strip():
        st.error("Debes ingresar URLs")
    else:

        urls = urls_input.split("\n")

        st.write("Procesando datos...")

        data = []

        for u in urls:
            u = u.strip()
            if u:
                data.append(scrape(u))

        st.write("Consultando Gemini...")

        prompt = build_prompt(data, location)

        result = call_gemini(prompt)

        st.markdown("## Resultado estratégico")
        st.write(result)

        with st.expander("Datos crudos"):
            st.json(data)

# ==============================
# DEBUG
# ==============================

with st.expander("Debug"):
    st.write("API Key cargada:", bool(GEMINI_API_KEY))
