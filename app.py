import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius", page_icon="🏆")
st.title("🏆 Buscador de Classificació Enigmàrius")

nom_input = st.text_input("Escriu el nom de la persona:", "")
nom_a_buscar = nom_input.strip()

if st.button("Buscar a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Arrencant agent...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Fem una finestra MOLT LLARGA (8000 px) per carregar tota la taula d'un cop
            context = browser.new_context(viewport={'width': 1200, 'height': 8000})
            page = context.new_page()
            
            estat.info("🌐 Entrant a Món Enigmàrius...")
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded")
            
            # Esborrem el mur de cookies perquè no ens tapi
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            
            # --- EL TRUC MAESTRE ---
            estat.info("🖱️ Obrint la classificació i fent scroll...")
            # Cliquem qualsevol cosa que digui Classificació sense esperar selectors ràpids
            try:
                page.get_by_text("POSICIÓ").first.click(timeout=5000)
                time.sleep(5)
            except:
                pass

            # Fem un scroll lent cap avall per forçar que la web carregui els noms
            for i in range(5):
                page.evaluate(f"window.scrollTo(0, {i * 1500})")
                time.sleep(1)

            # --- CERCA DEL NOM ---
            estat.info(f"🕵️ Buscant '{nom_a_buscar}' a tota la pàgina...")
            
            # Busquem el text a tota la pàgina
            trobat = False
            # Intentem trobar l'element que conté el nom
            target = page.get_by_text(nom_a_buscar, exact=False).first
            
            if target.count() > 0:
                target.scroll_into_view_if_needed()
                time.sleep(1)
                st.success(f"✅ TROBAT! He localitzat a '{nom_a_buscar}' a la llista.")
                trobat = True
            else:
                st.error(f"❌ No he trobat a '{nom_a_buscar}' a la vista actual.")

            # Captura de pantalla del que veu l'agent
            foto = page.screenshot(full_page=False)
            browser.close()
            
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha perdut: {e}")
