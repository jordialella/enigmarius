  import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius", page_icon="🏆")
st.title("🏆 Buscador de Classificació Enigmàrius")

# Buscador de text (netegem espais sobrants)
nom_input = st.text_input("Escriu el nom de la persona:", "")
nom_a_buscar = nom_input.strip()

if st.button("Buscar a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Preparant l'agent...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1000, 'height': 1200})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb Món Enigmàrius...")
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="domcontentloaded")
            
            # Neteja de cookies
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            
            # Entrem a la classificació
            try:
                # Busquem el botó i forçem el clic
                btn = page.locator("text='Veure tota la classificació', text='Classificació'").first
                btn.scroll_into_view_if_needed()
                btn.click()
                time.sleep(5) # Espera inicial per la taula
            except:
                st.warning("No he trobat el botó, potser ja sóc dins.")

            trobat = False
            pàgines_maximes = 5 # Anem a provar les primeres 5 pàgines
            
            for p_num in range(1, pàgines_maximes + 1):
                estat.info(f"🕵️ Mirant pàgina {p_num}...")
                
                # Esperem que la taula estigui realment carregada
                page.wait_for_load_state("networkidle")
                time.sleep(3) 

                # Intentem trobar el nom exactament com apareix a la web
                # Fem servir un selector que busca el text dins de la taula
                try:
                    # Busquem el text i mirem si és visible
                    element = page.get_by_text(nom_a_buscar, exact=False).first
                    if element.is_visible():
                        element.scroll_into_view_if_needed()
                        time.sleep(1)
                        trobat = True
                        estat.success(f"✅ TROBAT! '{nom_a_buscar}' és a la pàgina {p_num}")
                        break
                except:
                    pass
                
                if not trobat:
                    estat.info(f"⏭️ No és a la p{p_num}. Clicant 'Següent'...")
                    try:
                        # Busquem el botó de següent (a 3Cat sol ser una icona o la paraula 'Següent')
                        next_btn = page.get_by_role("button", name="Següent").first
                        if not next_btn.is_visible():
                            next_btn = page.locator("text='>', text='Següent'").first
                        
                        if next_btn.is_visible():
                            next_btn.click()
                            # AQUESTA PAUSA ÉS CRUCIAL: Esperem que les dades canviïn
                            time.sleep(6) 
                        else:
                            st.warning("No hi ha més pàgines disponibles.")
                            break
                    except:
                        st.warning("S'ha acabat la llista o el botó no respon.")
                        break

            # Fem la foto del que veu l'agent ara mateix
            foto = page.screenshot(full_page=False)
            browser.close()
            
            if not trobat:
                st.error(f"❌ No he trobat a '{nom_a_buscar}' en cap de les pàgines mirades.")
            
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
