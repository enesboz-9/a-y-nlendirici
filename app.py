import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="AI Router | Enes Boz", 
    page_icon="🎯", 
    layout="centered"
)

# Modern CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 20px; height: 3.5em; 
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .ai-card { 
        padding: 25px; border-radius: 15px; background-color: white; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eaeaea;
        margin-bottom: 20px;
    }
    .alt-card { 
        padding: 12px; border-radius: 10px; background-color: #ffffff; 
        margin-top: 10px; border: 2px solid #f1f3f5; border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; font-weight: 600; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTORU ÇALIŞTIR (INITIALIZE AI) ---
@st.cache_resource
def initialize_ai():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Key bulunamadı (Secrets kontrol et)"
            
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Ekran görüntündeki modele öncelik verdik
        model_list = ['gemini-2.0-flash-lite', 'gemini-1.5-flash']
        
        for m_name in model_list:
            try:
                test_model = genai.GenerativeModel(m_name)
                # Bağlantıyı sessizce doğrula (kota harcamadan)
                return test_model, m_name
            except:
                continue
        return None, "Uygun model bulunamadı."
    except Exception as e:
        return None, str(e)

model, active_model_name = initialize_ai()

# --- 3. GENİŞ VERİ TABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻",
        "desc": "Kod yazımı ve teknik analizde dünya lideri.",
        "alternatives": ["Cursor AI", "GitHub Copilot", "DeepSeek-V3"]
    },
    "Görsel ve Tasarım": {
        "name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨",
        "desc": "Profesyonel sanatsal görsel üretiminde rakipsiz.",
        "alternatives": ["DALL-E 3", "Leonardo AI", "Recraft V3"]
    },
    "Hızlı Bilgi ve Araştırma": {
        "name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍",
        "desc": "Güncel internet verisiyle kaynak gösteren arama motoru.",
        "alternatives": ["Grok-2", "SearchGPT", "Phind"]
    },
    "Metin ve Yazışma": {
        "name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️",
        "desc": "Yaratıcı yazarlık ve genel asistanlık için standart.",
        "alternatives": ["Google Gemini", "Mistral Large", "Jasper"]
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬",
        "desc": "Gerçekçi yapay zeka videoları üretir.",
        "alternatives": ["Runway Gen-3", "Kling AI", "Sora"]
    },
    "Ses ve Müzik": {
        "name": "Suno AI", "url": "https://suno.com", "icon": "🎵",
        "desc": "Tam uzunlukta şarkılar besteler.",
        "alternatives": ["Udio", "ElevenLabs", "Adobe Podcast"]
    },
    "Sunum ve Doküman": {
        "name": "Gamma App", "url": "https://gamma.app", "icon": "📊",
        "desc": "Hızlıca profesyonel sunumlar hazırlar.",
        "alternatives": ["Canva Magic", "Tome", "Beautiful.ai"]
    },
    "Veri Analizi ve Excel": {
        "name": "Julius AI", "url": "https://julius.ai", "icon": "📈",
        "desc": "Veri tablolarını analiz eder ve grafikler oluşturur.",
        "alternatives": ["ChatGPT Analysis", "Rows", "Akkio"]
    },
    "Akademik ve PDF Analizi": {
        "name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄",
        "desc": "PDF'leri okur ve özetler.",
        "alternatives": ["Humata AI", "Consensus", "Elicit"]
    },
    "SEO ve Pazarlama": {
        "name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀",
        "desc": "İçerik optimizasyonu ve SEO analizi yapar.",
        "alternatives": ["Copy.ai", "Writesonic", "Semrush"]
    }
}

# --- 4. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, senin için **en iyi AI ekosistemini** kuralım.")

with st.sidebar:
    st.title("👨‍💻 Enes Boz AI Lab")
    if model:
        st.success(f"Bağlantı Aktif: {active_model_name}")
    else:
        st.error("Bağlantı Hatası!")
    st.markdown("---")
    st.caption("Versiyon: 2.7.0")

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Modern bir logo ve tanıtım müziği istiyorum.")

if st.button("En Uygun AI'ı Bul"):
    if not model:
        st.error(f"Hata: {active_model_name}")
        st.stop()

    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                categories = list(AI_DIRECTORY.keys())
                prompt = f"Kullanıcı isteği: {query}. Bu isteğe en uygun kategoriyi şunlardan seç: {categories}. Sadece kategori adını yaz."
                
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                
                matched_cat = next((cat for cat in categories if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                
                # ANA SONUÇ
                st.markdown(f"""
                <div class="ai-card">
                    <h2 style='margin-top: 0;'>{res['icon']} <span style='color: #FF4B4B;'>Önerilen: {res['name']}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em; line-height: 1.6;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.link_button(f"{res['name']} Web Sitesini Aç", res['url'], use_container_width=True)
                
                # ALTERNATİFLER
                st.markdown("<br><h4 style='color: #444;'>🔁 Popüler Alternatifler</h4>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Bir pürüz çıktı: {e}")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

st.markdown("<br><br><center style='opacity: 0.3; font-size: 0.8em;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
