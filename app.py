import streamlit as st
import google.generativeai as genai

# Streamlit Secrets üzerinden anahtarı çek (En güvenli ve doğru yol budur)
api_key = st.secrets["GOOGLE_API_KEY"]

# Arayüz Ayarları ve İmza
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")
st.markdown("---")

# API Yapılandırma
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Yapılandırılamadı: {e}")

# Veritabanı
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 4.5", "url": "https://claude.ai", "desc": "Kod yazımı ve teknik işler."},
    "Görsel Oluşturma": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Logo ve görsel tasarım."},
    "Araştırma ve Bilgi": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Hızlı ve kaynaklı bilgi."},
    "Video Üretimi": {"name": "Sora / Veo", "url": "https://openai.com/sora", "desc": "Yapay zeka videoları."},
    "Metin ve Yazarlık": {"name": "ChatGPT", "url": "https://chatgpt.com", "desc": "Genel metin işleri."}
}

query = st.text_input("Ne yapmak istiyorsunuz?", placeholder="Örn: Bir logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Göster"):
    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                prompt = f"Kullanıcı isteği: '{query}'. Bunu sadece şu kategorilerden biriyle eşleştir: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                category_result = response.text.strip()
                
                matched_category = None
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in category_result.lower():
                        matched_category = cat
                        break
                
                if matched_category:
                    res = AI_DIRECTORY[matched_category]
                    st.balloons()
                    st.success(f"Önerilen Araç: **{res['name']}**")
                    st.info(res['desc'])
                    st.link_button(f"{res['name']} Sayfasına Git 🚀", res['url'], use_container_width=True)
                else:
                    st.warning("Eşleşme sağlanamadı, lütfen başka bir cümle deneyin.")
            except Exception as e:
                st.error("Bir hata oluştu. Lütfen Secrets kısmındaki API anahtarını kontrol edin.")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
