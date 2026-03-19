import streamlit as st
import subprocess
from playwright.sync_api import sync_playwright

def install_playwright():
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Error instal·lant el navegador: {e}")

st.set_page_config(page_title="Agent Món Enigmàrius", page_icon="🧩")
st.title("🧩 El meu Agent d'Enigmàrius")

URL_ENIGMARIUS = "https://www.3cat.cat/catradio/mon-enigmarius/"

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    install_playwright()
    
    with st.spinner("L'agent està entrant a la web i preparant la imatge..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Posem una mida de finestra que ens permeti veure el contingut principal
                context = browser.new_context(viewport={'width': 1000, 'height': 1200})
                page = context.new_page()
                
                page.goto(URL_ENIGMARIUS, wait_until="domcontentloaded", timeout=60000)
                
                # 1. NETEJEM COOKIES I PUBLICITAT
                try:
                    # Clica "AGREE" si surt el banner
                    if page.locator("button:has-text('AGREE')").is_visible():
                        page.click("button:has-text('AGREE')")
                        page.wait_for_timeout(2000)
                    
                    # ESBORREM LA PUBLICITAT per codi perquè no surti a la foto
                    page.evaluate("document.querySelectorAll('.publicitat, .ads, [id*='google_ads_']').forEach(el => el.remove())")
                except:
                    pass

                # 2. ESPEREM QUE EL CONTINGUT D'ENIGMÀRIUS ESTIGUI A PANTALLA
                page.wait_for_selector("text=Món Enigmàrius", timeout=10000)
                page.wait_for_timeout(3000) # Temps extra perquè carreguin les fotos del jeroglífic

                # 3. FEM LA CAPTURA DE PANTALLA
                # En lloc de tota la web, busquem el contenidor principal de les notícies/enigmes
                foto_web = page.screenshot(full_page=False)

                browser.close()

                # MOSTRAR NOMÉS LA CAPTURA REAL
                st.write("---")
                st.success("✅ Aquí tens el contingut actual de Món Enigmàrius:")
                st.image(foto_web)

        except Exception as e:
            st.error(f"L'agent s'ha encallat: {e}")
