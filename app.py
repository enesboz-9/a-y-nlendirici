import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env yükle
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Arayüz Ayarları
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

# Tasarımcı İmzası
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")
st.markdown("---")

# API Yapılandırma ve Kontrol
if not api_key:
    st.error("HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Yapılandırma Hatası: {e}")

AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 4.5", "url": "https://claude.ai", "desc": "Kod yazımı ve teknik işler."},
    "Görsel Oluşturma": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Logo ve görsel tasarım."},
    "Araştırma ve Bilgi": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı ve kaynaklı bilgi."},
    "Video Üretimi": {"name": "Sora / Veo", "url": "https://openai.com/sora", "desc": "Yapay zeka videoları."},
    "Metin ve Yazarlık": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Genel metin işleri."}
}

query = st.text_input("Ne yapmak istiyorsunuz?", placeholder="Örn: Python ile veri analizi yapacağım.")

if st.button("En Uygun AI'ı Göster"):
    if query:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Analiz ediliyor... (Lütfen bekleyin)")
            progress_bar.progress(30)
            
            # Daha basit ve doğrudan bir prompt
            prompt = f"Kullanıcı ' {query} ' dedi. Bunu sadece şu kategorilerden biriyle eşleştir: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
            
            # API Çağrısı
            response = model.generate_content(prompt)
            progress_bar.progress(100)
            
            category_result = response.text.strip()
            
            # Eşleştirme Kontrolü
            matched_category = None
            for cat in AI_DIRECTORY.keys():
                if cat.lower() in category_result.lower():
                    matched_category = cat
                    break
            
            if matched_category:
                res = AI_DIRECTORY[matched_category]
                st.balloons()
                st.success(f"Analiz Başarılı! Önerilen: **{res['name']}**")
                st.write(res['desc'])
                st.link_button(f"{res['name']} Sayfasına Git 🚀", res['url'], use_container_width=True)
            else:
                st.warning(f"API '{category_result}' yanıtını verdi ama listede bulamadım. Lütfen tekrar deneyin.")
                
        except Exception as e:
            st.error(f"Bağlantı Hatası oluştu: {str(e)}")
            st.info("İpucu: İnternet bağlantınızı veya API anahtarınızın aktifliğini kontrol edin.")
        finally:
            status_text.empty()
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
