import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Küratörü v2.0", page_icon="🚀", layout="wide")

# 1. Veri Tabanı: 2026'nın Gizli ve Güçlü Araçları
AI_REHBERI = {
    "Görsel": {
        "sampiyon": "Nano Banana 2.0",
        "link": "https://banana.ai",
        "acıklama": "Metin yazma yeteneği en yüksek, fotogerçekçi görsel motoru.",
        "alternatifler": ["Midjourney v7", "Flux.1 Pro"]
    },
    "Video": {
        "sampiyon": "Google Veo 3",
        "link": "https://deepmind.google/veo",
        "acıklama": "Sinematik kalitede 1 dakikalık tutarlı video üretimi.",
        "alternatifler": ["Luma Dream Machine", "Kling AI"]
    },
    "Kod": {
        "sampiyon": "Claude 4.6 Sonnet",
        "link": "https://anthropic.com",
        "acıklama": "Hatasız mimari kurma ve karmaşık debug işlemlerinde lider.",
        "alternatifler": ["Cursor", "GitHub Copilot Next"]
    },
    "Ses": {
        "sampiyon": "Suno v5",
        "link": "https://suno.com",
        "acıklama": "Radyo kalitesinde vokal ve tam aranjeli müzik üretimi.",
        "alternatifler": ["Udio 2", "ElevenLabs Voice"]
    },
    "Metin": {
        "sampiyon": "Gemini 3.1 Pro",
        "link": "https://gemini.google.com",
        "acıklama": "2 milyon token bağlam penceresi ile devasa veri analizi.",
        "alternatifler": ["GPT-5 (Early Access)", "Perplexity"]
    }
}

# 2. Groq Bağlantısı
# Key'i Streamlit Secrets'tan al: st.secrets["GROQ_API_KEY"]
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets'a 'GROQ_API_KEY' ekleyin!")
    st.stop()

# 3. Arayüz
st.title("🤖 AI Küratörü: Akıllı Çözüm Rehberi")
st.markdown("---")

user_query = st.text_input("Ne üretmek istiyorsun?", placeholder="Örn: Yeni markam için bir logo ve kısa bir tanıtım videosu lazım...")

if user_query:
    with st.spinner("Niyetiniz analiz ediliyor..."):
        # Niyet Okuma (Intent Analysis)
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen bir AI Küratörüsün. Kullanıcı talebini analiz et ve sadece şu kategorilerden (virgülle ayırarak) hangilerine ihtiyaç duyulduğunu yaz: Görsel, Kod, Video, Ses, Metin. Ekstra açıklama yapma."
                    },
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            tespit_edilen = chat_completion.choices[0].message.content
            
            # Sonuçları Kartlar Halinde Göster
            st.subheader("🎯 Size Özel AI Çözüm Paketi")
            cols = st.columns(len(AI_REHBERI))
            
            found_any = False
            for cat_name, info in AI_REHBERI.items():
                if cat_name.lower() in tespit_edilen.lower():
                    found_any = True
                    with st.expander(f"✅ {cat_name} İhtiyacı Tespit Edildi", expanded=True):
                        st.markdown(f"### 🏆 Şampiyon: [{info['sampiyon']}]({info['link']})")
                        st.write(info['acıklama'])
                        st.divider()
                        st.write("**Alternatif Planlar:**")
                        for alt in info['alternatifler']:
                            st.caption(f"• {alt}")
            
            if not found_any:
                st.warning("Niyet tam anlaşılamadı, lütfen daha detaylı yazın.")

        except Exception as e:
            st.error(f"Groq API Hatası: {e}")

st.sidebar.info("Bu uygulama 2026 AI ekosistemine göre Groq & Llama 3.3 altyapısıyla güncellenmiştir.")
