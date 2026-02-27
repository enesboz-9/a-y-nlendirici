import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

# API Anahtarı ve Model Ayarı
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # En temel ve kısıtlamalara en az takılan model ismi
    model = genai.GenerativeModel('gemini-pro')
    
except Exception as e:
    st.error("Lütfen Streamlit Secrets kısmına geçerli bir API anahtarı girin.")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım": {"name": "Claude 3.5", "url": "https://claude.ai", "desc": "Kodlama projeleri."},
    "Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Görsel üretim."},
    "Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı bilgi."},
    "Genel": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Yazı ve asistanlık."}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")
st.divider()

user_input = st.text_input("Ne yapmak istiyorsunuz?", placeholder="Örn: Python öğrenmek istiyorum.")

if st.button("Hangi AI Uygun?", type="primary"):
    if user_input:
        with st.spinner('AI Yanıtlıyor...'):
            try:
                # Çok kısa ve net bir sorgu gönderiyoruz
                prompt = f"Soru: {user_input}. Sadece bir kelimeyle şu kategorilerden hangisi uygun: Yazılım, Tasarım, Araştırma, Genel?"
                response = model.generate_content(prompt)
                
                # Yanıtı temizle
                decision = response.text.strip()
                
                # Eşleştirme
                matched = "Genel" # Varsayılan
                for key in AI_DIRECTORY.keys():
                    if key.lower() in decision.lower():
                        matched = key
                        break
                
                res = AI_DIRECTORY[matched]
                st.balloons()
                st.success(f"Tavsiyemiz: **{res['name']}**")
                st.info(res['desc'])
                st.link_button(f"{res['name']} Uygulamasına Git", res['url'], use_container_width=True)
                
            except Exception as e:
                st.error(f"API Hatası: {e}")
                st.info("İpucu: API Studio'daki uyarıyı düzeltene kadar bu hata devam edebilir.")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
