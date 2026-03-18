import streamlit as st
from playwright.sync_api import sync_playwright

# Títol i descripció a la web
st.set_page_config(page_title="Agent Navegador", page_icon="🤖")
st.title("🤖 El meu Agent de Navegació Web")
st.write("Introdueix una URL i l'agent buscarà el títol i els enllaços principals.")

# Entrada de dades de l'usuari
url_usuari = st.text_input("URL de la pàgina:", "https://www.wikipedia.org")

if st.button("Llançar Agent 🚀"):
    with st.spinner("L'agent està navegant per la web..."):
        try:
            with sync_playwright() as p:
                # Iniciem el navegador (en mode invisible per al servidor)
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url_usuari, wait_until="networkidle")

                # --- ACCIONS DE L'AGENT ---
                titol = page.title()
                enllacos = page.locator("a").count()
                
                # Exemple de captura de pantalla (opcional)
                screenshot = page.screenshot()
                # --------------------------

                browser.close()

                # Mostrar resultats a la web
                st.success("✅ Tasca completada!")
                st.metric("Títol de la pàgina", titol)
                st.write(f"S'han trobat **{enllacos}** enllaços en aquesta web.")
                st.image(screenshot, caption="Captura de pantalla realitzada per l'agent")

        except Exception as e:
            st.error(f"S'ha produït un error: {e}")