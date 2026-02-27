import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE MODEL BAĞLANTISI (ARKA PLANDA) ---
st.set_page_config(
    page_title="AI Router | Enes Boz", 
    page_icon="🎯", 
    layout="centered"
)

# Custom CSS ile Arayüzü Güzelleştirelim
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    /* Buton Tasarımı */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B; /* Ana Kırmızı Renk */
        color: white;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e04343; /* Hover Rengi */
    }
    /* Giriş Kutusu Tasarımı */
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 1px solid #ced4da;
    }
    /* Sonuç Kartı Tasarımı */
    .ai-card {
        padding: 25px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #eaeaea;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_ai():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # Arka planda en iyi modeli bulalım
        for m_name in ['gemini-3-flash-preview', 'gemini-1.5-flash', 'gemini-1.0-pro']:
            try:
                test_model = genai.GenerativeModel(m_name)
                test_model.generate_content("ping")
                return test_model
            except: continue
        return None
    except: return None

model = initialize_ai()

# --- 2. AI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "desc": "Kod yazımı, hata ayıklama ve teknik dökümantasyon için lider.", "icon": "💻"},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Dünyanın en gelişmiş yapay zeka görsel üretim aracı.", "icon": "🎨"},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "Canlı internet verisiyle akademik seviyede araştırma asistanı.", "icon": "🔍"},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "desc": "Yaratıcı yazarlık, çeviri ve genel asistanlık için ideal.", "icon": "✍️"},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "desc": "Gerçekçi ve yüksek çözünürlüklü yapay zeka videoları.", "icon": "🎬"}
}

# --- 3. ARAYÜZ (UI) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, senin için **en iyi yapay zekayı** bulalım.")
st.divider()

if model is None:
    st.error("Sistem şu an meşgul. Lütfen API anahtarınızı kontrol edin.")
    st.stop()

# Yan sütun (Sidebar)
with st.sidebar:
    st.title("Uygulama Bilgisi")
    st.info("Bu araç, ihtiyacınıza en uygun AI modelini seçmek için Gemini zekasını kullanır.")
    st.markdown("---")
    st.caption("Geliştirici: Enes Boz")
    st.caption("Versiyon: 2.1.0")

# Giriş Alanı
query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Modern bir logo tasarlatmak istiyorum.")

# İşlem ve Sonuç
if st.button("En Uygun AI'ı Bul"):
    if query:
        with st.spinner('Yapay zeka modelleri taranıyor...'):
            try:
                prompt = f"Kullanıcı sorusu: {query}. Kategoriler: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                
                res_text = response.text.strip()
                matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                
                # --- Şık ve Okunaklı Sonuç Kartı ---
                # 'Önerilen: Program İsmi' kısmı artık Kırmızı renkte ve net!
                st.markdown(f"""
                <div class="ai-card">
                    <h2 style='margin-top: 0;'>{res['icon']} <span style='color: #FF4B4B;'>Önerilen: {res['name']}</span></h2>
                    <p style="color: #444; font-size: 1.1em; line-height: 1.6;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Git Butonu (Kırmızı)
                st.link_button(f"{res['name']} Web Sitesini Aç", res['url'], use_container_width=True)
                    
            except Exception as e:
                st.error("Küçük bir hata oluştu, lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

# Footer
st.markdown("<br><br><br><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
