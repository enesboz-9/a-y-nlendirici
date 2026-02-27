import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Küratörü | Enes Boz", page_icon="💎", layout="wide")

# 1. Veri Tabanı: 2026 AI Ekosistemi (Hibrit Model)
AI_REHBERI = {
    "Görsel": {
        "profesyonel": {"ad": "Nano Banana 2.0", "url": "https://banana.ai", "ozellik": "Dünyanın en gelişmiş görsel motoru."},
        "ucretsiz": {"ad": "Flux.1 Schnell", "url": "https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell", "ozellik": "Açık kaynak ve tamamen ücretsiz."},
    },
    "Video": {
        "profesyonel": {"ad": "Google Veo 3", "url": "https://deepmind.google/technologies/veo/", "ozellik": "Sinematik 4K video üretimi."},
        "ucretsiz": {"ad": "Pika Art", "url": "https://pika.art", "ozellik": "Günlük ücretsiz deneme kredisi sunar."},
    },
    "Kod": {
        "profesyonel": {"ad": "Claude 4.6 Sonnet", "url": "https://www.anthropic.com/claude", "ozellik": "Karmaşık mimariler için en zeki model."},
        "ucretsiz": {"ad": "Codeium", "url": "https://codeium.com", "ozellik": "Bireysel kullanım için sınırsız ve ücretsiz."},
    },
    "Ses": {
        "profesyonel": {"ad": "Suno v5", "url": "https://suno.com", "ozellik": "Profesyonel müzik ve vokal üretimi."},
        "ucretsiz": {"ad": "Udio Free", "url": "https://www.udio.com", "ozellik": "Kısıtlı ama yüksek kaliteli ücretsiz sürüm."},
    },
    "Metin": {
        "profesyonel": {"ad": "Gemini 3.1 Pro", "url": "https://gemini.google.com", "ozellik": "Deasa veri setleri için 2M bağlam."},
        "ucretsiz": {"ad": "HuggingChat", "url": "https://huggingface.co/chat/", "ozellik": "Llama 3.3 tabanlı, tamamen açık ve ücretsiz."},
    }
}

# 2. API Bağlantısı (Groq - Hız ve Limit Avantajı)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🔑 Hata: GROQ_API_KEY bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
    st.stop()

# 3. Sol Menü (Sidebar) ve Mod Seçimi
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Kontrol Merkezi")
    st.markdown("---")
    
    # --- MOD SEÇİCİ ---
    ucretsiz_mod = st.toggle("✨ Sadece Ücretsiz Modu Aç", value=False)
    
    if ucretsiz_mod:
        st.info("Şu an 'Ekonomik Mod' aktif. Sadece ücretsiz araçlar listeleniyor.")
    else:
        st.success("Şu an 'Profesyonel Mod' aktif. En güçlü araçlar listeleniyor.")
    
    st.markdown("---")
    st.write(f"👨‍💻 Geliştirici: **Enes Boz**")
    st.caption("Versiyon 3.5 | 2026")

# 4. Ana Ekran Tasarımı
st.markdown("<h1 style='text-align: center;'>🚀 AI Küratörü</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555;'>Akıllı Yapay Zeka Yönlendirme Sistemi - <b>Enes Boz</b></p>", unsafe_allow_html=True)
st.markdown("---")

user_input = st.text_input("Hangi konuda yardıma ihtiyacın var?", placeholder="Örn: Şirketim için bir logo tasarlatmak ve kod yazdırmak istiyorum.")



if user_input:
    with st.spinner("Enes Boz'un yapay zekası niyetinizi analiz ediyor..."):
        try:
            # Niyet Analizi (Groq Llama 3.3)
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Kullanıcının talebini şu kategorilere ayır (virgülle yaz): Görsel, Kod, Video, Ses, Metin. Sadece isimleri döndür."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
            )
            tespit_edilen = chat.choices[0].message.content
            
            st.subheader("💡 Önerilen Çözümler")
            
            # Kategorileri Ekrana Basma
            for kat, veri in AI_REHBERI.items():
                if kat.lower() in tespit_edilen.lower():
                    with st.container(border=True):
                        c1, c2 = st.columns([3, 1])
                        
                        if ucretsiz_mod:
                            # ÜCRETSİZ MOD GÖRÜNÜMÜ
                            with c1:
                                st.markdown(f"### 🆓 {kat}: {veri['ucretsiz']['ad']}")
                                st.write(f"*{veri['ucretsiz']['ozellik']}*")
                                st.caption("Bu araç ücretsiz/açık kaynaklıdır.")
                            with c2:
                                st.link_button("🌐 Ücretsiz Kullan", veri['ucretsiz']['url'], use_container_width=True)
                        else:
                            # TÜMÜ / PROFESYONEL MOD GÖRÜNÜMÜ
                            with c1:
                                st.markdown(f"### 🏆 {kat}: {veri['profesyonel']['ad']}")
                                st.write(f"*{veri['profesyonel']['ozellik']}*")
                                st.write(f"**Alternatif:** {veri['ucretsiz']['ad']} (Ücretsiz)")
                            with c2:
                                st.link_button("🚀 Siteyi Aç", veri['profesyonel']['url'], use_container_width=True)
                                
        except Exception as e:
            st.error(f"Bir analiz hatası oluştu: {e}")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center;'>© 2026 <b>Enes Boz</b> tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
