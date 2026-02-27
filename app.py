import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 404 hatasını aşmak için en yalın model ismini kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Başlatma Hatası: {e}")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama ve mantık işleri."},
    "Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Görsel ve logo tasarımı."},
    "Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı bilgi arama."},
    "Genel": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Metin ve asistanlık."}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından geliştirilmiştir.")
st.divider()

user_input = st.text_input("Ne yapmak istersiniz?", placeholder="Örn: Python öğrenmek istiyorum.")

if st.button("Hangi AI Uygun?", type="primary"):
    if user_input:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Promptu aşırı basit tutuyoruz
                prompt = f"Kullanıcı isteği: {user_input}. Bu isteğe en uygun kategoriyi seç: Yazılım, Tasarım, Araştırma, Genel. Sadece kategoriyi yaz."
                response = model.generate_content(prompt)
                
                decision = response.text.strip()
                matched = "Genel" # Varsayılan
                for key in AI_DIRECTORY.keys():
                    if key.lower() in decision.lower():
                        matched = key
                        break
                
                res = AI_DIRECTORY[matched]
                st.balloons()
                st.success(f"Tavsiyemiz: **{res['name']}**")
                with st.container(border=True):
                    st.write(res['desc'])
                    st.link_button(f"{res['name']} Uygulamasına Git", res['url'], use_container_width=True)
            except Exception as e:
                st.error(f"Teknik Hata: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
