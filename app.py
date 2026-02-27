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
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 15px;
    }
    .ai-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
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

# --- 3. ARAYÜZ (Görsel Odaklı) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, senin için **en iyi yapay zekayı** bulalım.")
st.divider()

if model is None:
    st.error("Sistem şu an meşgul. Lütfen API anahtarınızı kontrol edin.")
    st.stop()

# Giriş Alanı
query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Modern bir logo tasarlatmak istiyorum.")

# Yan sütun (Sidebar) kısmına Enes Boz imzasını ve model bilgisini gizleyelim
with st.sidebar:
    st.title("Uygulama Bilgisi")
    st.info("Bu araç, ihtiyacınıza en uygun AI modelini seçmek için Gemini zekasını kullanır.")
    st.markdown("---")
    st.caption("Geliştirici: Enes Boz")
    st.caption("Versiyon: 2.0.0")

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
                
                # Şık Sonuç Kartı
                st.markdown(f"""
                <div class="ai-card">
                    <h2>{res['icon']} Önerilen: {res['name']}</h2>
                    <p style="color: #666; font-size: 1.1em;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.link_button(f"{res['name']} Web Sitesini Aç", res['url'], use_container_width=True)
                    
            except Exception as e:
                st.error("Küçük bir hata oluştu, lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

# Footer
st.markdown("<br><br><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
