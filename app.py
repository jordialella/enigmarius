import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    # Instal·lació silenciosa del navegador
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Món Enigmàrius", page_icon="🧩")
st.title("🧩 El meu Agent d'Enigmàrius")

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Arrencant motors...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Posem una mida de pantalla gran perquè es vegi tot el contingut
            context = browser.new_context(viewport={'width': 1280, 'height': 1400})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb 3Cat...")
            # Anem a la URL i esperem que la xarxa estigui tranquil·la
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded", timeout=90000)
            
            estat.info("🧹 Netejant la pantalla...")
            # Intentem tancar el mur de cookies clicant qualsevol botó d'acceptar
            try:
                page.click("button:has-text('AGREE'), button:has-text('Acceptar'), button:has-text('Tancar')", timeout=10000)
            except:
                # Si no troba el botó, intentem esborrar el mur per codi directament
                page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
                page.evaluate("document.querySelector('.ot-sdk-container')?.remove()")
            
            # ESPERA CRUCIAL: Donem 8 segons perquè tot el contingut es dibuixi
            time.sleep(8)
            
            estat.info("📸 Fent la captura final...")
            # Fem la foto de la part superior de la web on sol estar el repte
            foto = page.screenshot(clip={'x': 0, 'y': 0, 'width': 1280, 'height': 1000})
            
            browser.close()
            
            estat.success("✅ Aquí tens el que he trobat:")
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha encallat: {e}")gent s'ha encallat: {e}")
