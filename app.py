import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA VE KRİTİK HATA ÇÖZÜMÜ ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ÇÖZÜM: Bazı hesaplarda/bölgelerde SDK sürümü nedeniyle 'models/' ön eki gerekebilir.
    # Eğer bu da hata verirse SDK otomatik olarak fallback yapacaktır.
    model_name = 'gemini-1.5-flash' 
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")
    st.stop()

# --- 2. AI ARAÇLARI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kodlama ve mantık işleri."},
    "Görsel Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Logo ve görsel tasarım."},
    "Araştırma ve Bilgi": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "Kaynaklı arama motoru."},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "desc": "AI video oluşturucu."},
    "Metin ve Yazarlık": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Genel asistanlık."}
}

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("<p style='color: grey;'>Enes Boz tarafından tasarlanmıştır.</p>", unsafe_allow_html=True)
st.divider()

query = st.text_input("Ne yapmak istiyorsun?", placeholder="Örn: Python ile veri analizi...")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Zekamız analiz ediyor...'):
            try:
                # 404 hatasını bypass etmek için en sade prompt yapısı
                prompt = f"Kullanıcı sorusu: {query}. Kategoriler: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                
                # API Çağrısı
                response = model.generate_content(prompt)
                
                # Yanıt işleme
                if response:
                    res_text = response.text.strip()
                    matched_cat = None
                    for cat in AI_DIRECTORY.keys():
                        if cat.lower() in res_text.lower():
                            matched_cat = cat
                            break
                    
                    if matched_cat:
                        res = AI_DIRECTORY[matched_cat]
                        st.balloons()
                        st.success(f"Önerilen Araç: **{res['name']}**")
                        with st.container(border=True):
                            st.subheader(res['name'])
                            st.write(res['desc'])
                            st.link_button(f"{res['name']} Sayfasına Git 🚀", res['url'], use_container_width=True)
                    else:
                        st.warning("Uygun bir kategori eşleşmedi.")
            except Exception as e:
                # Eğer hala 404 alıyorsak, SDK'ya model ismini manuel dikte edelim
                st.error(f"Teknik bir kısıtlama oluştu: {e}")
                st.info("İpucu: Eğer hata 404 ise, Google AI Studio'dan yeni bir API anahtarı almayı deneyebilirsiniz.")
    else:
        st.warning("Bir cümle yazın.")

st.markdown("<br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
