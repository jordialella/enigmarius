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
    
    with st.spinner("L'agent està netejant la pantalla i buscant el repte..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(viewport={'width': 1280, 'height': 800})
                page = context.new_page()
                
                # Anem a la web
                page.goto(URL_ENIGMARIUS, wait_until="domcontentloaded", timeout=60000)
                
                # 1. ELIMINEM EL MUR DE COOKIES (Tècnica radical)
                # Provem de fer clic al botó que has vist a la teva captura
                try:
                    # Esperem que qualsevol botó amb aquests textos aparegui
                    page.wait_for_selector("button:has-text('AGREE'), button:has-text('Acceptar')", timeout=8000)
                    page.click("button:has-text('AGREE')")
                    page.wait_for_timeout(2000) # Esperem que marxi la capa blanca
                except:
                    # Si falla el clic, provem de forçar la desaparició per codi
                    page.evaluate("document.querySelector('.ot-sdk-container')?.remove()")
                    page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")

                # 2. BUSQUEM LA IMATGE SENSE ESPERAR SELECTORS COMPLICATS
                # Simplement mirem què hi ha a la pantalla després de 5 segons
                page.wait_for_timeout(5000)
                
                # Busquem la imatge més gran que no sigui un logo
                imatges = page.locator("img").all()
                img_url = None
                max_size = 0
                
                for img in imatges:
                    src = img.get_attribute("src")
                    box = img.bounding_box()
                    if src and box and box['width'] > 200 and "logo" not in src.lower():
                        img_url = src
                        break

                # 3. CAPTURA DE PANTALLA (Per confirmar que veiem el que toca)
                foto_web = page.screenshot()
                browser.close()

                # MOSTRAR RESULTATS
                if img_url:
                    if img_url.startswith("/"):
                        img_url = "https://www.3cat.cat" + img_url
                    st.success("✅ Imatge localitzada!")
                    st.image(img_url)
                
                st.write("---")
                st.write("📸 **Això és el que l'agent veu ara mateix:**")
                st.image(foto_web)

        except Exception as e:
            st.error(f"L'agent s'ha encallat: {e}")
