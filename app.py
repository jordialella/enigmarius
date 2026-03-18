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

# URL directa
URL_ENIGMARIUS = "https://www.3cat.cat/catradio/mon-enigmarius/"

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    install_playwright()
    
    with st.spinner("L'agent està buscant la secció 'MÓN ENIGMÀRIUS'..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Posem una resolució de pantalla gran per veure-ho tot bé
                context = browser.new_context(viewport={'width': 1280, 'height': 800})
                page = context.new_page()
                
                # Anem a la web
                page.goto(URL_ENIGMARIUS, wait_until="networkidle", timeout=60000)
                
                # Esperem que aparegui el títol "Món Enigmàrius" per confirmar que som a la pàgina bona
                page.wait_for_selector("text=Món Enigmàrius", timeout=15000)

                # Intentem buscar la imatge del post més recent (el de dalt de tot)
                # A 3Cat solen estar en un article o un contenidor de mitjans
                imatge_final = None
                
                # Busquem la primera imatge que estigui dins del bloc de contingut principal
                # El selector 'main img' sol ser el més fiable per saltar-se logos de capçalera
                selector_contingut = "main img"
                if page.locator(selector_contingut).count() > 0:
                    # Agafem la primera que trobem dins del contingut principal
                    img_element = page.locator(selector_contingut).first
                    img_url = img_element.get_attribute("src")
                    if img_url:
                        if img_url.startswith("/"):
                            img_url = "https://www.3cat.cat" + img_url
                        imatge_final = img_url

                # Fem una captura del que està veient l'agent en aquest moment
                foto_web = page.screenshot(full_page=False)

                browser.close()

                if imatge_final:
                    st.success("✅ He trobat la secció i la imatge!")
                    st.image(imatge_final, caption="Imatge extreta de Món Enigmàrius")
                
                st.write("---")
                st.write("📸 Això és el que l'agent veu actualment (Captura real):")
                st.image(foto_web)

        except Exception as e:
            st.error(f"L'agent s'ha perdut: {e}")
