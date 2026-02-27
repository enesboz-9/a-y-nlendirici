import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ÇÖZÜM: 1.5 Flash hata veriyorsa, en kararlı model olan gemini-pro'ya geçiyoruz.
    # Bu model neredeyse tüm bölgelerde ve SDK sürümlerinde sorunsuz çalışır.
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")
    st.stop()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama işleri."},
    "Görsel Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Görsel ve logo."},
    "Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "Bilgi arama."},
    "Video": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "desc": "Video üretimi."},
    "Metin": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Yazı işleri."}
}

# --- 3. ARAYÜZ ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")
st.divider()

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Python ile oyun yazmak istiyorum.")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Promptu çok sade tutarak hata riskini azaltıyoruz
                prompt = f"Kullanıcı sorusu: {query}. Bunu şu listeden bir kategoriyle eşleştir: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                
                response = model.generate_content(prompt)
                
                if response:
                    res_text = response.text.strip()
                    matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in res_text.lower()), None)
                    
                    if matched_cat:
                        res = AI_DIRECTORY[matched_cat]
                        st.balloons()
                        st.success(f"Öneri: **{res['name']}**")
                        with st.container(border=True):
                            st.write(res['desc'])
                            st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
                    else:
                        st.warning("Kategori tam anlaşılamadı, lütfen daha açık yazın.")
            except Exception as e:
                st.error(f"Teknik Hata: {e}")
                st.info("Not: API anahtarınızın Gemini Pro modeline erişimi olduğundan emin olun.")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
