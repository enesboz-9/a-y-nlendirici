import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Küratörü | Enes Bozo", page_icon="🤖", layout="wide")

# 1. Veri Tabanı: 2026 AI Ekosistemi (Güncel Linklerle)
AI_REHBERI = {
    "Görsel": {
        "sampiyon": "Nano Banana 2.0",
        "link": "https://banana.ai",
        "acıklama": "Metin yazma yeteneği en yüksek, fotogerçekçi görsel motoru.",
        "alternatifler": [
            {"ad": "Midjourney v7", "url": "https://www.midjourney.com"},
            {"ad": "Flux.1 Pro", "url": "https://blackforestlabs.ai"}
        ]
    },
    "Video": {
        "sampiyon": "Google Veo 3",
        "link": "https://deepmind.google/technologies/veo/",
        "acıklama": "Sinematik kalitede 1 dakikalık tutarlı video üretimi.",
        "alternatifler": [
            {"ad": "Luma Dream Machine", "url": "https://lumalabs.ai/"},
            {"ad": "Kling AI", "url": "https://klingai.com"}
        ]
    },
    "Kod": {
        "sampiyon": "Claude 4.6 Sonnet",
        "link": "https://www.anthropic.com/claude",
        "acıklama": "Hatasız mimari kurma ve karmaşık debug işlemlerinde lider.",
        "alternatifler": [
            {"ad": "Cursor", "url": "https://cursor.sh"},
            {"ad": "GitHub Copilot", "url": "https://github.com/features/copilot"}
        ]
    },
    "Ses": {
        "sampiyon": "Suno v5",
        "link": "https://suno.com",
        "acıklama": "Radyo kalitesinde vokal ve tam aranjeli müzik üretimi.",
        "alternatifler": [
            {"ad": "Udio 2", "url": "https://www.udio.com"},
            {"ad": "ElevenLabs", "url": "https://elevenlabs.io"}
        ]
    },
    "Metin": {
        "sampiyon": "Gemini 3.1 Pro",
        "link": "https://gemini.google.com",
        "acıklama": "2 milyon token bağlam penceresi ile devasa veri analizi.",
        "alternatifler": [
            {"ad": "Perplexity", "url": "https://www.perplexity.ai"},
            {"ad": "ChatGPT (GPT-5)", "url": "https://chat.openai.com"}
        ]
    }
}

# 2. Groq Bağlantısı
api_key = st.secrets.get("GROQ_API_KEY")
if api_key:
    client = Groq(api_key=api_key)
else:
    st.error("🔑 API Anahtarı bulunamadı! Lütfen Secrets kısmına 'GROQ_API_KEY' ekleyin.")
    st.stop()

# 3. Arayüz Tasarımı
st.title("🚀 AI Küratörü: Akıllı Çözüm Rehberi")
st.markdown(f"**Geliştirici:** `Enes Bozo` | 2026 AI Ekosistemi")
st.markdown("---")

user_query = st.text_input("Ne üretmek istiyorsun?", placeholder="Örn: Yeni markam için bir logo ve kısa bir tanıtım videosu lazım...")

if user_query:
    with st.spinner("Niyetiniz analiz ediliyor..."):
        try:
            # Groq üzerinden Niyet Analizi
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen bir AI uzmanısın. Kullanıcı talebini analiz et ve sadece şu kategorilerden uygun olanları virgülle ayırarak yaz: Görsel, Kod, Video, Ses, Metin. Başka hiçbir şey yazma."
                    },
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            tespit_edilen = chat_completion.choices[0].message.content
            
            st.subheader("🎯 Tespit Edilen Çözüm Paketi")
            
            found_any = False
            # Tespit edilen kategorileri dön
            for cat_name, info in AI_REHBERI.items():
                if cat_name.lower() in tespit_edilen.lower():
                    found_any = True
                    with st.container():
                        st.success(f"### {cat_name} İhtiyacı")
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**🏆 Şampiyon Önerisi:** {info['sampiyon']}")
                            st.write(info['acıklama'])
                            st.markdown("**Alternatifler:** " + ", ".join([alt['ad'] for alt in info['alternatifler']]))
                        
                        with col2:
                            # Ana butonu göster
                            st.link_button(f"🚀 {info['sampiyon']}'a Git", info['link'], use_container_width=True)
                            
                            # Alternatifleri küçük linkler olarak göster
                            with st.expander("Diğer Seçenekler"):
                                for alt in info['alternatifler']:
                                    st.markdown(f"🔗 [{alt['ad']}]({alt['url']})")
                        st.divider()
            
            if not found_any:
                st.warning("Niyet tam anlaşılamadı, lütfen daha açık bir talep yazın.")

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

# Alt Bilgi
st.sidebar.markdown("---")
st.sidebar.write(f"© 2026 **Enes Boz**")
st.sidebar.caption("Bu uygulama Groq Llama 3.3 altyapısını kullanarak saniyeler içinde karar verir.")
