import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius - Classificació", page_icon="🏆")
st.title("🏆 Classificació Món Enigmàrius")

# Nova opció: Cercador de persones
nom_a_buscar = st.text_input("Nom de la persona a buscar (opcional):", "")

if st.button("Anar a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Preparant agent...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 2000})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb 3Cat...")
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="networkidle")
            
            # 1. Neteja de cookies
            try:
                page.click("button:has-text('AGREE'), button:has-text('Acceptar')", timeout=5000)
            except:
                page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")

            # 2. BUSCAR EL BOTÓ DE CLASSIFICACIÓ
            estat.info("🔍 Buscant el botó de Classificació...")
            # Fem scroll cap avall perquè el botó aparegui
            page.evaluate("window.scrollTo(0, 1500)")
            time.sleep(2)
            
            # Cliquem el botó (busquem el text exacte que surt a la web)
            try:
                btn_classificacio = page.locator("text='Veure tota la classificació', text='Classificació'").first
                btn_classificacio.click()
                estat.info("🖱️ Clic fet a la classificació! Esperant dades...")
                time.sleep(5) # Esperem que carregui la taula
            except:
                st.warning("No he trobat el botó directe, intentant captura general...")

            # 3. SI HAS POSAT UN NOM, L'INTENTEM BUSCAR (CTRL+F de l'agent)
            if nom_a_buscar:
                estat.info(f"🕵️ Buscant a '{nom_a_buscar}' a la llista...")
                # L'agent busca el text a la pàgina i fa scroll fins allà
                try:
                    target = page.locator(f"text='{nom_a_buscar}'").first
                    target.scroll_into_view_if_needed()
                    time.sleep(1)
                except:
                    st.error(f"No he trobat a '{nom_a_buscar}' a la pantalla actual.")

            # 4. CAPTURA DE LA TAULA
            foto = page.screenshot(full_page=False)
            
            browser.close()
            
            estat.success("✅ Classificació carregada!")
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha perdut: {e}")        st.error(f"❌ L'agent s'ha encallat: {e}")
