import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE OTOMATİK MODEL BULUCU ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Kanka burada sistemdeki tüm modelleri tarayıp 
    # hangisi çalışıyorsa onu kapıyoruz (404'ü bitiren çözüm)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Öncelik sıramız: 1.5 Flash, 1.5 Pro, 1.0 Pro
    target_model = None
    for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro', 'models/gemini-pro']:
        if preferred in available_models:
            target_model = preferred
            break
            
    if not target_model:
        st.error("Hesabınızda kullanılabilir bir Gemini modeli bulunamadı.")
        st.stop()
        
    model = genai.GenerativeModel(target_model)
    active_name = target_model.split('/')[-1]

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama ve teknik işler."},
    "Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Görsel ve logo tasarımı."},
    "Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı bilgi arama."},
    "Genel": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Yazı ve asistanlık."}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.caption(f"Tasarım: Enes Boz | Çalışan Model: {active_name}")
st.divider()

user_input = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Logo tasarlatmak istiyorum.")

if st.button("Hangi AI Uygun?", type="primary"):
    if user_input:
        with st.spinner('Zekamız analiz ediyor...'):
            try:
                prompt = f"Kullanıcı isteği: {user_input}. Bu isteği şu kategorilerden biriyle eşleştir: Yazılım, Tasarım, Araştırma, Genel. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                
                decision = response.text.strip()
                matched = next((k for k in AI_DIRECTORY if k.lower() in decision.lower()), "Genel")
                
                res = AI_DIRECTORY[matched]
                st.balloons()
                st.success(f"Tavsiyemiz: **{res['name']}**")
                with st.container(border=True):
                    st.write(res['desc'])
                    st.link_button(f"{res['name']} Uygulamasına Git", res['url'], use_container_width=True)
            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
