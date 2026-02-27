import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE MODEL BAĞLANTISI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

@st.cache_resource
def initialize_ai():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Denenecek model listesi (En güncelden en kararlıya)
        models_to_try = [
            'gemini-3-flash-preview', # Senin istediğin güncel model
            'gemini-1.5-flash', 
            'gemini-1.0-pro'
        ]
        
        for m_name in models_to_try:
            try:
                test_model = genai.GenerativeModel(m_name)
                # Modeli doğrulamak için boş bir çağrı yapıyoruz
                test_model.generate_content("ping")
                return test_model, m_name
            except:
                continue
        return None, None
    except Exception as e:
        return None, str(e)

model, active_model_name = initialize_ai()

# --- 2. AI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Karmaşık kodlama ve teknik analizler için en iyisi."},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Logo, sanatsal görsel ve profesyonel tasarım için."},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "İnternet taramalı, kaynak gösteren güncel bilgi arama."},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "desc": "E-posta, makale yazımı ve genel asistanlık için."},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "desc": "Yüksek kaliteli yapay zeka videoları için."}
}

# --- 3. ARAYÜZ (UI) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown(f"**Geliştirici:** Enes Boz | **Aktif Beyin:** `{active_model_name}`")
st.divider()

if model is None:
    st.error(f"⚠️ Bağlantı Hatası: {active_model_name}")
    st.info("Lütfen Streamlit Secrets kısmına geçerli bir API anahtarı eklediğinizden emin olun.")
    st.stop()

query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Python ile yılan oyunu yazmak istiyorum.")

if st.button("En Uygun AI'ı Bul", type="primary"):
    if query:
        with st.spinner('Işık hızında analiz ediliyor...'):
            try:
                prompt = f"Kullanıcı sorusu: {query}. Bu soruyu şu kategorilerden biriyle eşleştir: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz, başka açıklama yapma."
                response = model.generate_content(prompt)
                
                # Cevabı temizle ve eşleştir
                res_text = response.text.strip()
                matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                
                res = AI_DIRECTORY[matched_cat]
                
                # Sonuç Ekranı
                st.balloons()
                st.success(f"Senin için en uygun araç: **{res['name']}**")
                
                with st.container(border=True):
                    st.write(f"**Neden bu araç?** {res['desc']}")
                    st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                    
            except Exception as e:
                st.error(f"Analiz hatası: {e}")
    else:
        st.warning("Lütfen bir şeyler yazın.")

st.markdown("<br><hr><center style='opacity: 0.5;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
