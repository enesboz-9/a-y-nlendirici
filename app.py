import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ÇÖZÜM: 'models/' ön ekini kaldırıp en düz ismi deniyoruz. 
    # Bazı SDK sürümlerinde bu isim 404'ü aşar.
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Sistem başlatılamadı: {e}")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama için en iyisi."},
    "Görsel Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Tasarım için profesyonel araç."},
    "Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "Arama motoru."},
    "Video": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "desc": "Video oluşturucu."},
    "Metin": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Genel asistan."}
}

# --- 3. ARAYÜZ ---
st.set_page_config(page_title="AI Router | Enes Boz")
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")
st.divider()

query = st.text_input("Bugün ne yapmak istiyorsun?")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Modeli direkt kullanıcı sorgusuyla test ediyoruz
                response = model.generate_content(f"Kategoriler: {list(AI_DIRECTORY.keys())}. Soru: {query}. Sadece kategori adını yaz.")
                
                # Yanıtı güvenli bir şekilde al
                ai_decision = response.text.strip()
                
                matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in ai_decision.lower()), None)
                
                if matched_cat:
                    res = AI_DIRECTORY[matched_cat]
                    st.balloons()
                    st.success(f"Öneri: **{res['name']}**")
                    st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                else:
                    st.warning("Uygun bir kategori bulunamadı.")
            except Exception as e:
                # Hata devam ederse burası çalışacak
                st.error(f"Teknik Hata: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
