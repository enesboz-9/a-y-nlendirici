import streamlit as st
import google.generativeai as genai

# --- 1. GÜVENLİK VE YAPILANDIRMA ---
# Streamlit Secrets üzerinden API anahtarı çekilir
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 404 hatasını önlemek için model ismini tam yol (models/...) olarak tanımlıyoruz
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Başlatma Hatası: {e}")
    st.stop()

# --- 2. AI ARAÇLARI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", 
        "url": "https://claude.ai", 
        "desc": "Karmaşık yazılım projeleri, hata ayıklama ve teknik analizler için en iyi tercih."
    },
    "Görsel Tasarım": {
        "name": "Midjourney", 
        "url": "https://www.midjourney.com", 
        "desc": "Profesyonel logo, UI/UX tasarımı ve yüksek kaliteli sanatsal görseller üretir."
    },
    "Araştırma ve Bilgi": {
        "name": "Perplexity AI", 
        "url": "https://www.perplexity.ai", 
        "desc": "İnterneti gerçek zamanlı tarayarak kaynak gösteren akıllı arama motoru."
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", 
        "url": "https://lumalabs.ai/dream-machine", 
        "desc": "Gerçekçi ve yüksek çözünürlüklü yapay zeka videoları oluşturur."
    },
    "Metin ve Yazarlık": {
        "name": "ChatGPT", 
        "url": "https://chatgpt.com", 
        "desc": "Blog yazıları, özetleme, çeviri ve genel asistanlık işlerinde lider."
    }
}

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

# Başlık ve İmza
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("<p style='color: #666;'>Enes Boz tarafından tasarlanmıştır.</p>", unsafe_allow_html=True)
st.divider()

# Kullanıcı Girişi
user_query = st.text_input("Ne yapmak istiyorsun?", placeholder="Örn: Python ile bir veri analizi scripti yazdırmak istiyorum...")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if user_query:
        with st.spinner('İsteğiniz analiz ediliyor...'):
            try:
                # Yapay Zeka Analizi
                prompt = f"""
                Kullanıcı İsteği: "{user_query}"
                Bu isteği şu kategorilerden sadece birine ata: {list(AI_DIRECTORY.keys())}.
                Sadece kategori ismini yaz, başka açıklama yapma.
                """
                
                # API Çağrısı
                response = model.generate_content(prompt)
                ai_decision = response.text.strip()
                
                # Eşleştirme Mantığı
                matched_cat = None
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in ai_decision.lower():
                        matched_cat = cat
                        break
                
                if matched_cat:
                    res = AI_DIRECTORY[matched_cat]
                    st.balloons()
                    st.success(f"Analiz Tamamlandı! En uygun araç: **{res['name']}**")
                    
                    # Sonuç Kartı
                    with st.container(border=True):
                        st.subheader(f"🚀 {res['name']}")
                        st.write(res['desc'])
                        st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                else:
                    st.warning("Hangi aracın uygun olduğunu belirleyemedim. Lütfen isteğinizi daha açık yazın.")
            
            except Exception as e:
                # Hata durumunda detaylı bilgi gösterir
                st.error(f"Bir teknik hata oluştu: {e}")
    else:
        st.warning("Lütfen bir cümle yazın.")

# Alt Bilgi
st.markdown("<br><br><br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
