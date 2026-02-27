import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="AI Küratörü 2026", page_icon="🤖")

# 1. API Bağlantısını Önbelleğe Al (Cache)
@st.cache_resource
def setup_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        # 2026'da Türkiye ve Streamlit üzerinde en stabil model:
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        st.error(f"Kurulum Hatası: {e}")
        return None

# Secrets'tan anahtarı çek
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Secrets kısmına API anahtarını ekle.")
    api_key = None

model = setup_gemini(api_key)

# 2. Uygulama Arayüzü
st.title("🚀 AI Küratörü: Akıllı Yönlendirme")
user_input = st.text_input("Ne yapmak istiyorsun?", placeholder="Örn: Yeni şirketim için bir logo ve tanıtım müziği lazım")

if user_input and model:
    with st.spinner("Niyetiniz analiz ediliyor..."):
        try:
            # Niyet Okuma Promptu
            prompt = f"""Sen bir AI uzmanısın. Kullanıcının şu talebini analiz et: '{user_input}'
            Sadece şu kategorilerden uygun olanları virgülle ayırarak yaz: 
            Görsel, Kod, Video, Metin, Ses."""
            
            response = model.generate_content(prompt)
            kategoriler = response.text
            
            st.subheader("🎯 Tespit Edilen İhtiyaçlar")
            st.info(kategoriler)
            
            # Burada senin veri tabanın devreye girecek
            # (Şimdilik örnek bir gösterim yapalım)
            if "Görsel" in kategoriler:
                st.success("**Görsel Tasarım:** Nano Banana 2.0 (Şampiyon)")
            if "Ses" in kategoriler:
                st.success("**Müzik/Ses:** Suno v5 (Şampiyon)")

        except Exception as e:
            st.error(f"İşlem sırasında hata oluştu: {e}")
