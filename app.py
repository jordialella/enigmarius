import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    st.write("🔧 Verificant el navegador invisible al servidor...")
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius - Classificació", page_icon="🏆")
st.title("🏆 Super Agent de Classificació Enigmàrius")

nom_a_buscar = st.text_input("Vols buscar algun nom concret a la llista?", "")

if st.button("Forçar entrada a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Arrencant motors del super agent...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Finestra extremadament alta per forçar que la classificació carregui
            context = browser.new_context(viewport={'width': 1280, 'height': 5000})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb 3Cat (Món Enigmàrius)...")
            # Donem molt de temps per a la connexió inicial
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded", timeout=120000)
            
            # --- NETEJA RADICAL ---
            estat.info("🧹 Netejant cookies i obstacles...")
            # En lloc de clicar botons, esborrem els elements de la memòria per codi
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            page.evaluate("document.querySelector('.ot-sdk-container')?.remove()")
            
            # --- NAVEGACIÓ FORÇADA ---
            estat.info("🔍 Buscant Classificació. Tècnica Bulldozer activada...")
            # Baixem molt cap avall on se suposa que hi ha el botó
            page.evaluate("window.scrollTo(0, 2500)")
            time.sleep(3) # Esperem que el botó s'arrossegui a la vista
            
            # Intentem clicar, però amb un temps d'espera curt. Si falla, continuem
            try:
                # Busquem selectors més genèrics per al botó
                page.click("a:has-text('lassificaci'), button:has-text('lassificaci')", timeout=10000)
                estat.info("🖱️ Clic fet a 'Classificació'! Esperant dades...")
                # Una espera MÉS LLARGA perquè carregui la llista
                time.sleep(10) 
            except:
                st.warning("L'agent no ha pogut confirmar el clic al botó, provaré de fer una captura del que hi hagi a sota.")

            # --- BUSCAR NOM SI CAL ---
            if nom_a_buscar:
                estat.info(f"🕵️ Buscant '{nom_a_buscar}' a la classificació...")
                # L'agent fa un CTRL+F per trobar el nom i moure la pantalla
                try:
                    page.locator(f"text='{nom_a_buscar}'").first.scroll_into_view_if_needed()
                    time.sleep(1)
                except:
                    pass

            # --- CAPTURA FINAL ---
            foto = page.screenshot(full_page=False)
            browser.close()
            
            estat.success("✅ Tasca completada!")
            st.write("---")
            st.write("📸 Això és el que l'agent veu ara mateix:")
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent ha tingut un problema greu: {e}")
