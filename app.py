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

# La URL de la secció on surt el títol "Món Enigmàrius"
URL_ENIGMARIUS = "https://www.3cat.cat/catradio/mon-enigmarius/"

if st.button("Buscar l'Enigmàrius d'avui 🚀"):
    install_playwright()
    
    with st.spinner("L'agent està entrant a 3Cat i buscant el contingut..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Simulem un navegador real per evitar bloquejos de seguretat
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                page = context.new_page()
                
                # Anem a la web i esperem que carregui el contingut bàsic
                page.goto(URL_ENIGMARIUS, wait_until="domcontentloaded", timeout=60000)
                
                # Esperem uns segons extra perquè el JavaScript de 3Cat munti la pàgina
                page.wait_for_timeout(5000)

                # BUSQUEM LA IMATGE:
                # 1. Intentem buscar imatges grans que no siguin logos
                imatges = page.locator("img").all()
                img_detectada = None
                
                for img in imatges:
                    src = img.get_attribute("src")
                    # Filtrem per evitar logos petits o icones
                    if src and ("jpg" in src or "png" in src) and "logo" not in src.lower():
                        if img.bounding_box() and img.bounding_box()['width'] > 200:
                            img_detectada = src
                            break
                
                # 2. Fem una captura de pantalla de SEGURETAT (això no falla mai)
                # Així veuràs el que l'agent té davant dels ulls
                foto_web = page.screenshot(full_page=False)

                browser.close()

                if img_detectada:
                    if img_detectada.startswith("/"):
                        img_detectada = "https://www.3cat.cat" + img_detectada
                    st.success("✅ Imatge del repte trobada!")
                    st.image(img_detectada)
                
                st.write("---")
                st.write("📸 **Captura de pantalla de la web en directe:**")
                st.image(foto_web)

        except Exception as e:
            st.error(f"L'agent ha tingut un problema: {e}")
