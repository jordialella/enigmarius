import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius - Classificació", page_icon="🏆")
st.title("🏆 Classificació Món Enigmàrius")

# Buscador de text
nom_a_buscar = st.text_input("Nom de la persona a buscar a la classificació:", "")

if st.button("Anar a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Arrencant l'agent...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Posem una finestra alta per veure bé la classificació
            context = browser.new_context(viewport={'width': 1280, 'height': 2500})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb 3Cat...")
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded", timeout=60000)
            
            # Neteja de cookies
            try:
                page.click("button:has-text('AGREE'), button:has-text('Acceptar')", timeout=8000)
                time.sleep(2)
            except:
                page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            
            # Busquem el botó de classificació
            estat.info("🔍 Buscant el botó de la Classificació...")
            page.evaluate("window.scrollTo(0, 1200)") # Baixem una mica
            time.sleep(2)
            
            # Intentem clicar el botó
            try:
                # Busquem per text o per link que contingui 'classificacio'
                btn = page.locator("text='Veure tota la classificació', text='Classificació'").first
                btn.click()
                estat.info("🖱️ Clic fet! Esperant que carregui la llista...")
                time.sleep(5)
            except:
                st.warning("No he pogut clicar el botó, faré una captura general.")

            # Si busquem algú concret
            if nom_a_buscar:
                estat.info(f"🕵️ Buscant '{nom_a_buscar}'...")
                try:
                    # Fem un scroll fins on aparegui el text
                    target = page.get_by_text(nom_a_buscar, exact=False).first
                    target.scroll_into_view_if_needed()
                    time.sleep(1)
                except:
                    pass

            foto = page.screenshot(full_page=False)
            browser.close()
            
            estat.success("✅ Classificació llista!")
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha encallat: {e}")   
