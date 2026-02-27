import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

try:
    # Secrets'tan key'i alıyoruz
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # KRİTİK DÜZELTME: 'v1beta' hatasını aşmak için API sürümünü 'v1'e zorluyoruz
    genai.configure(api_key=api_key)
    
    # Modeli v1 sürümüyle çağırıyoruz
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash'
    )
    # API sürümünü manuel zorlamak için opsiyon (404'ü bitiren vuruş)
    options = RequestOptions(api_version='v1')
    
except Exception as e:
    st.error(f"Başlatma Hatası: {e}")
    st.stop()

# --- 2. AI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama ve teknik işler."},
    "Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Görsel ve logo tasarımı."},
    "Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı bilgi arama."},
    "Genel": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Metin ve asistanlık."}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından geliştirilmiştir.")
st.divider()

user_input = st.text_input("Ne yapmak istersiniz?", placeholder="Örn: Modern bir logo tasarlatmak istiyorum.")

if st.button("AI Önerisini Gör", type="primary"):
    if user_input:
        with st.spinner('AI ile bağlantı kuruluyor...'):
            try:
                # v1 sürümü üzerinden sorgu gönderiyoruz
                prompt = f"Kullanıcı sorusu: {user_input}. Sadece şu kategorilerden birini yaz: Yazılım, Tasarım, Araştırma, Genel."
                response = model.generate_content(prompt, request_options=options)
                
                decision = response.text.strip()
                matched = "Genel" # Default
                
                for key in AI_DIRECTORY.keys():
                    if key.lower() in decision.lower():
                        matched = key
                        break
                
                res = AI_DIRECTORY[matched]
                st.balloons()
                st.success(f"Önerimiz: **{res['name']}**")
                with st.container(border=True):
                    st.write(res['desc'])
                    st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
            
            except Exception as e:
                st.error(f"Teknik bir sorun oluştu: {e}")
                st.info("Eğer hala 404 alıyorsanız, Google AI Studio'da yeni aldığınız key'in yanındaki 'Enable' butonunun aktif olduğundan emin olun.")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
