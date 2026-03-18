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

URL_ENIGMARIUS = "https://www.3cat.cat/catradio/mon-enigmarius"

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    install_playwright()
    
    with st.spinner("L'agent està entrant a 3Cat..."):
        try:
            with sync_playwright() as p:
                # Iniciem el navegador
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Anem a la web i esperem que carregui
                page.goto(URL_ENIGMARIUS, wait_until="networkidle")
                
                # 1. Intentem tancar el banner de cookies si apareix
                try:
                    if page.locator("button:has-text('Acceptar')").is_visible():
                        page.click("button:has-text('Acceptar')")
                except:
                    pass

                # 2. Busquem la imatge principal del repte
                # A 3Cat les imatges solen estar dins de classes 'media-img' o 'img-responsive'
                imatge_selector = "div.media-content img, article img, figure img"
                
                # Esperem una mica que les imatges es carreguin realment
                page.wait_for_timeout(2000) 
                
                img_element = page.locator(imatge_selector).first
                img_url = img_element.get_attribute("src")
                
                # 3. Fem una captura de pantalla real de la web per si falla el link
                foto_web = page.screenshot(full_page=False)

                browser.close()

                # Resultats
                if img_url:
                    # Corregim la URL si és relativa
                    if img_url.startswith("/"):
                        img_url = "https://www.3cat.cat" + img_url
                    
                    st.success("✅ He trobat aquesta imatge a la portada:")
                    st.image(img_url, caption="Imatge del repte detectada")
                else:
                    st.warning("No he pogut extreure la URL de la imatge, però aquí tens una captura de la web:")
                    st.image(foto_web)

        except Exception as e:
            st.error(f"S'ha produït un error: {e}")
