import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Super Agent Classificació", page_icon="🧩")
st.title("🧩 Extractor de Classificació Enigmàrius")

nom_a_buscar = st.text_input("Escriu el nom que vols que l'agent busqui:", "")

if st.button("Extreure Classificació Directament 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Preparant agent especialitzat...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Fem la finestra MOLT llarga (5000 píxels) per veure tota la llista d'un cop
            context = browser.new_context(viewport={'width': 1000, 'height': 5000})
            page = context.new_page()
            
            estat.info("🌐 Saltant a la secció de dades...")
            # Anem directament a la URL de l'enigmàrius
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="networkidle")
            
            # Netegem el mur de cookies per codi ràpid
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            
            estat.info("🖱️ Intentant forçar l'obertura de la taula...")
            # En lloc de clicar, busquem si la classificació està amagada i la mostrem
            page.evaluate("""
                () => {
                    // Busquem qualsevol element que contingui la classificació i el forçem a veure's
                    const elements = document.querySelectorAll('*');
                    for (let el of elements) {
                        if (el.innerText.includes('Classificació') || el.innerText.includes('Punts')) {
                            el.scrollInto_view;
                        }
                    }
                }
            """)
            
            # Si hem posat un nom, forçem la cerca de text al navegador
            if nom_a_buscar:
                estat.info(f"🕵️ Buscant '{nom_a_buscar}'...")
                # Intentem trobar el text i moure la pantalla
                try:
                    target = page.get_by_text(nom_a_buscar, exact=False).first
                    target.scroll_into_view_if_needed()
                    time.sleep(2)
                except:
                    pass
            else:
                # Si no hi ha nom, baixem fins on sol estar la taula (part inferior)
                page.evaluate("window.scrollTo(0, 2800)")
                time.sleep(3)

            foto = page.screenshot(full_page=False)
            browser.close()
            
            estat.success("✅ Classificació capturada!")
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha encallat: {e}")
