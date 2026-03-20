import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    st.write("🔧 Preparant motors a nivell de servidor (això pot trigar 1-2 min)...")
    try:
        # Forçem la instal·lació de Chromium
        subprocess.run(["playwright", "install", "chromium"], check=True)
        st.success("✅ Navegador invisible a punt!")
    except Exception as e:
        st.error(f"❌ Error greu instal·lant navegador: {e}")

st.set_page_config(page_title="Super Agent Enigmàrius", page_icon="🧩")
st.title("🧩 El Super Agent d'Enigmàrius")

# Buscador de text opcional
nom_a_buscar = st.text_input("Vols buscar un nom concret a la classificació?", "")

if st.button("Forçar entrada a la Classificació 🚀"):
    # Missatges d'estat en temps real per saber que no està mort
    estat_app = st.empty()
    
    try:
        estat_app.info("1️⃣ Verificant el motor de navegació remota...")
        install_playwright()
        
        with sync_playwright() as p:
            # Llançem el navegador
            browser = p.chromium.launch(headless=True)
            # Finestra extremadament gran perquè la web no amagui res
            context = browser.new_context(viewport={'width': 1280, 'height': 5000})
            page = context.new_page()
            
            # 2️⃣ Connexió a la web
            estat_app.info("2️⃣ Connectant amb 3Cat (Món Enigmàrius)...")
            # Donem MOLT de temps de Timeout (2 minuts) per si la web va lenta
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded", timeout=120000)
            
            # 3️⃣ Neteja radical d'obstacles per codi
            estat_app.info("3️⃣ Netejant cookies i obstacles per codi directament...")
            # Eliminem els murs de cookies directament de la memòria de la web
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            page.evaluate("document.querySelector('.ot-sdk-container')?.remove()")
            
            # 4️⃣ Scroll i Clic forçat
            estat_app.info("4️⃣ Buscant botó de Classificació. Tècnica 'Trituradora'...")
            # Baixem molt cap avall de la web per forçar que el botó s'arrossegui a la vista
            page.evaluate("window.scrollTo(0, 2500)")
            time.sleep(4) # Temps perquè la web reaccioni a l'scroll
            
            # Cliquem el botó amb un selector súper genèric (qualsevol cosa que porti "lassificaci")
            try:
                page.click("text=/lassificaci/i", timeout=15000)
                estat_app.info("🖱️ Clic fet a 'Classificació'! Esperant dades...")
                # Una espera MÉS LLARGA perquè carregui la llista sencer
                time.sleep(12) 
            except:
                st.warning("L'agent no ha rebut confirmació del clic, però provaré de fer una captura del que hi hagi.")

            # 5️⃣ Si busquem algú, forçem el scroll fins a la línia
            if nom_a_buscar:
                estat_app.info(f"🕵️ Buscant a '{nom_a_buscar}' a la classificació...")
                # L'agent fa un CTRL+F per trobar el nom i moure la pantalla
                try:
                    target = page.locator(f"text='{nom_a_buscar}'").first
                    target.scroll_into_view_if_needed()
                    time.sleep(1)
                except:
                    st.error(f"No he trobat a '{nom_a_buscar}' a la vista actual.")

            # 6️⃣ Captura final
            foto = page.screenshot(full_page=False)
            browser.close()
            
            # Mostrar resultat
            estat_app.success("✅ Tasca completada!")
            st.write("---")
            st.write("📸 Captura real de la zona on l'agent s'ha aturat:")
            st.image(foto)
            
    except Exception as e:
        # Mostrem l'error exacte si s'atura
        st.error(f"❌ L'agent ha tingut un problema greu: {e}")
