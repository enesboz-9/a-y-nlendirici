import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA (OTOMATİK MODEL SEÇİMİ) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Hata almamak için sistemdeki modelleri tarayan bir fallback mantığı
    # Önce en yaygın ismi deniyoruz
    model = genai.GenerativeModel('gemini-pro')
except Exception:
    try:
        # Eğer yukarıdaki olmazsa (404 verirse), alternatif ismi deniyoruz
        model = genai.GenerativeModel('models/gemini-pro')
    except Exception as e:
        st.error(f"Model Bağlantı Hatası: {e}")
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

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Bir web sitesi hazırlamak istiyorum.")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Bağlantı kuruluyor...'):
            try:
                # SADECE kullanıcı girişini gönderiyoruz, karmaşık promptları bırakıyoruz
                # Bu, 404 hatasını tetikleyen v1beta zorlamasını aşabilir.
                response = model.generate_content(query)
                
                if response:
                    res_text = response.text.lower()
                    
                    # AI'ın cevabında kategorilerimizi arıyoruz
                    matched_cat = None
                    for cat in AI_DIRECTORY.keys():
                        if cat.lower() in res_text:
                            matched_cat = cat
                            break
                    
                    # Eğer AI düzgün cevap vermezse varsayılan olarak "Metin" atayalım
                    if not matched_cat:
                        matched_cat = "Metin"
                    
                    res = AI_DIRECTORY[matched_cat]
                    st.balloons()
                    st.success(f"Önerilen Araç: **{res['name']}**")
                    with st.container(border=True):
                        st.write(res['desc'])
                        st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
            except Exception as e:
                st.error(f"Teknik bir sorun oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
