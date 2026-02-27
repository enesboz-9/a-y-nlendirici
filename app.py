import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env dosyasından anahtarı çek
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini Yapılandırması
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# AI Araçları Listesi
AI_DIRECTORY = {
    "Yazılım/Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Karmaşık kod yapılarında en iyisi."},
    "Görsel Tasarım": {"name": "Midjourney / Leonardo", "url": "https://leonardo.ai", "desc": "Profesyonel çizim ve logo için."},
    "Akademik Araştırma": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Kaynak göstererek hızlı bilgi bulur."},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai/dream-machine", "desc": "Yüksek kaliteli AI videoları için."},
    "Metin/Yaratıcı Yazım": {"name": "ChatGPT", "url": "https://chat.com", "desc": "Genel asistanlık ve blog yazıları için."}
}

def analyze_intent(user_input):
    prompt = f"""
    Sen bir AI rehberisin. Kullanıcının şu isteğini analiz et: "{user_input}"
    Bu istek şu kategorilerden hangisine giriyor: {list(AI_DIRECTORY.keys())}?
    Sadece kategori ismini yaz, başka bir açıklama yapma.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit Arayüzü ---
st.set_page_config(page_title="Ücretsiz AI Router", page_icon="🚀")

st.title("🤖 Ücretsiz AI Yönlendirici")
st.info("Bu uygulama Gemini API kullanarak tamamen ücretsiz çalışır.")

user_query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Modern bir web sitesi tasarımı istiyorum...")

if st.button("En Uygun AI'ı Göster"):
    if user_query:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Gemini'ye soruyoruz
                category = analyze_intent(user_query)
                
                # Eşleşen kategoriyi bul
                matched_category = None
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in category.lower():
                        matched_category = cat
                        break
                
                if matched_category:
                    res = AI_DIRECTORY[matched_category]
                    st.success(f"Analiz Tamamlandı: **{matched_category}**")
                    
                    st.subheader(f"Öneri: {res['name']}")
                    st.write(res['desc'])
                    st.link_button(f"{res['name']} Sitesine Git 🚀", res['url'])
                else:
                    st.warning("İsteğine uygun bir AI bulamadım, lütfen daha açık yaz.")
            except Exception as e:
                st.error(f"API hatası: {e}")
    else:
        st.warning("Lütfen bir cümle yazın.")
