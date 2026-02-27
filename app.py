import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA VE OTOMATİK MODEL SEÇİCİ ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

@st.cache_resource
def get_working_model(api_key):
    genai.configure(api_key=api_key)
    # Denenecek model isimleri (En güncelden en kararlıya)
    models_to_try = [
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-1.0-pro', 
        'gemini-pro'
    ]
    
    for m_name in models_to_try:
        try:
            test_model = genai.GenerativeModel(m_name)
            # Modeli test etmek için boş bir çağrı yapıyoruz
            test_model.generate_content("test")
            return test_model, m_name
        except Exception:
            continue
    return None, None

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    model, active_model_name = get_working_model(api_key)
    
    if not model:
        st.error("Üzgünüm, API anahtarınız şu anki Gemini modellerinin hiçbiriyle eşleşmedi. Lütfen Google AI Studio'dan anahtarınızı kontrol edin.")
        st.stop()
except Exception as e:
    st.error(f"Sistem Hatası: {e}")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5", "url": "https://claude.ai", "desc": "Kodlama projeleri için."},
    "Görsel Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Logo ve görsel için."},
    "Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı bilgi için."},
    "Metin": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Yazı ve asistanlık."}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.caption(f"Tasarım: Enes Boz | Çalışan Model: {active_model_name}")
st.divider()

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Bağlantı kuruluyor...'):
            try:
                prompt = f"Kullanıcı sorusu: {query}. Bunu şu listeden bir kategoriyle eşleştir: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                
                res_text = response.text.strip()
                matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in res_text.lower()), "Metin")
                
                res = AI_DIRECTORY[matched_cat]
                st.balloons()
                st.success(f"Önerilen: **{res['name']}**")
                st.info(res['desc'])
                st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
            except Exception as e:
                st.error(f"Analiz hatası: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
