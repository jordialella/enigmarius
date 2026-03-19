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
    
    with st.spinner("L'agent està gestionant el mur de cookies i buscant el repte..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                page = context.new_page()
                
                page.goto(URL_ENIGMARIUS, wait_until="domcontentloaded", timeout=60000)
                
                # 1. ACCIÓ CLAU: Fer clic al botó d'acceptar cookies
                # Busquem el botó que diu "AGREE AND CLOSE" o "Acceptar"
                try:
                    # Esperem que el botó sigui visible uns segons
                    page.wait_for_selector("button:has-text('AGREE AND CLOSE')", timeout=10000)
                    page.click("button:has-text('AGREE AND CLOSE')")
                    # Esperem un segon que marxi la finestra
                    page.wait_for_timeout(2000)
                except:
                    # Si no troba el botó amb aquest text, provem en català
                    try:
                        page.click("button:has-text('Acceptar')")
                    except:
                        pass # Si no surt el banner, continuem

                # 2. Ara que el mur ha marxat, busquem la imatge
                # Busquem imatges dins de la secció principal de la web
                page.wait_for_selector("main img", timeout=10000)
                imatges = page.locator("main img").all()
                
                img_final = None
                for img in imatges:
                    src = img.get_attribute("src")
                    # Busquem una imatge que sembli el repte (evitant logos)
                    if src and ("jpg" in src or "png" in src) and "logo" not in src.lower():
                        img_final = src
                        break
                
                # Fem la captura de pantalla JA SENSE EL MUR
                foto_web = page.screenshot(full_page=False)

                browser.close()

                if img_final:
                    if img_final.startswith("/"):
                        img_final = "https://www.3cat.cat" + img_final
                    st.success("✅ Imatge trobada sense el mur de cookies!")
                    st.image(img_final)
                
                st.write("---")
                st.write("📸 **Captura actual de la web (neta):**")
                st.image(foto_web)

        except Exception as e:
            st.error(f"L'agent ha tingut un problema: {e}")
