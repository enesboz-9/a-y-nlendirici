import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE GİZLİLİK ---
# Streamlit Cloud üzerindeki 'Secrets' kısmından anahtarı çeker
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Anahtarı bulunamadı veya hatalı. Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

# --- 2. AI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", 
        "url": "https://claude.ai", 
        "desc": "Karmaşık yazılım projeleri ve mantık yürütme için en iyisi."
    },
    "Görsel Tasarım": {
        "name": "Midjourney", 
        "url": "https://www.midjourney.com", 
        "desc": "Logo, UI/UX tasarımı ve sanatsal görseller için rakipsiz."
    },
    "Araştırma ve Bilgi": {
        "name": "Perplexity AI", 
        "url": "https://www.perplexity.ai", 
        "desc": "İnterneti tarayarak kaynak gösteren en hızlı arama motoru."
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", 
        "url": "https://lumalabs.ai/dream-machine", 
        "desc": "Yüksek kaliteli ve gerçekçi AI videoları oluşturur."
    },
    "Metin ve Yazarlık": {
        "name": "ChatGPT", 
        "url": "https://chatgpt.com", 
        "desc": "Blog yazıları, özetleme ve günlük asistanlık işlerinde lider."
    }
}

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

# Başlık ve İmza
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown(f"<p style='color: grey;'>Enes Boz tarafından tasarlanmıştır.</p>", unsafe_allow_html=True)
st.divider()

# Kullanıcı Girişi
user_query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Modern bir logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if user_query:
        with st.spinner('Zekamız iş başında, analiz ediliyor...'):
            try:
                # Yapay Zekaya Danışma
                prompt = f"""
                Kullanıcı İsteği: "{user_query}"
                Bu isteği şu kategorilerden sadece birine ata: {list(AI_DIRECTORY.keys())}.
                Sadece kategori ismini yaz, açıklama yapma.
                """
                response = model.generate_content(prompt)
                ai_decision = response.text.strip()
                
                # Karar Kontrolü
                matched_cat = None
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in ai_decision.lower():
                        matched_cat = cat
                        break
                
                if matched_cat:
                    res = AI_DIRECTORY[matched_cat]
                    st.balloons()
                    st.success(f"Analiz Tamamlandı! Senin için en iyisi: **{res['name']}**")
                    
                    # Sonuç Kartı
                    with st.container(border=True):
                        st.subheader(res['name'])
                        st.write(res['desc'])
                        st.link_button(f"{res['name']} Sayfasına Git 🚀", res['url'], use_container_width=True)
                else:
                    st.warning("İsteğine uygun bir AI aracı kategorize edilemedi. Lütfen daha detaylı yaz.")
            
            except Exception as e:
                st.error(f"Bir teknik hata oluştu: {e}")
    else:
        st.warning("Lütfen bir iş veya görev giriniz.")

# Alt Bilgi
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='opacity: 0.4;'>© 2026 | Enes Boz tarafından geliştirildi.</center>", unsafe_allow_html=True)
