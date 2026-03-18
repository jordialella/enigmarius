import streamlit as st
import subprocess
from playwright.sync_api import sync_playwright

def install_playwright():
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Error instal·lant el navegador: {e}")

st.set_page_config(page_title="Agent Enigmàrius", page_icon="🧩")
st.title("🧩 El meu Agent d'Enigmàrius")

URL_ENIGMARIUS = "https://www.3cat.cat/catradio/mon-enigmarius"

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    install_playwright()
    
    with st.spinner("L'agent està entrant a 3Cat..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Simulem un navegador real per evitar bloquejos
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
                page = context.new_page()
                
                # Anem a la web i esperem només que estigui carregada bàsicament
                page.goto(URL_ENIGMARIUS, wait_until="domcontentloaded")
                
                # Esperem 5 segons per seguretat perquè es carreguin les imatges
                page.wait_for_timeout(5000)

                # Intentem capturar TOTES les imatges de la web i busquem la que sembli el repte
                totes_les_imatges = page.locator("img").all()
                
                img_final = None
                for img in totes_les_imatges:
                    src = img.get_attribute("src")
                    if src and ("jpg" in src or "png" in src) and "logo" not in src.lower():
                        # Si trobem una imatge que no sigui un logo i tingui bona pinta, l'agafem
                        img_final = src
                        break
                
                # També fem una captura de pantalla per si de cas no trobem el fitxer
                foto_web = page.screenshot()

                browser.close()

                if img_final:
                    if img_final.startswith("/"):
                        img_final = "https://www.3cat.cat" + img_final
                    st.success("✅ Imatge trobada!")
                    st.image(img_final)
                else:
                    st.warning("No he trobat la imatge directa, però aquí tens el que veu l'agent:")
                    st.image(foto_web)

        except Exception as e:
            st.error(f"S'ha produït un error: {e}")
