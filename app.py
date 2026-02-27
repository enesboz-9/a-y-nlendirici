import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="AI Router | Enes Boz", 
    page_icon="🎯", 
    layout="centered"
)

# Gelişmiş CSS: Okunabilirlik ve Modern Kartlar
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 20px; height: 3.5em; 
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stTextInput>div>div>input { border-radius: 15px; }
    
    /* Ana Öneri Kartı */
    .ai-card { 
        padding: 25px; border-radius: 15px; background-color: white; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eaeaea;
        margin-bottom: 20px;
    }
    
    /* Alternatif Kutucukları - %100 Okunabilir */
    .alt-card { 
        padding: 12px; border-radius: 10px; background-color: #ffffff; 
        margin-top: 10px; border: 2px solid #f1f3f5; border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; font-weight: 600; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_ai():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # Mevcut en iyi modelleri sırayla dene
        for m_name in ['gemini-3-flash-preview', 'gemini-1.5-flash', 'gemini-1.0-pro']:
            try:
                test_model = genai.GenerativeModel(m_name)
                test_model.generate_content("ping")
                return test_model
            except: continue
        return None
    except: return None

model = initialize_ai()

# --- 2. GENİŞLETİLMİŞ VERİ TABANI (10 KATEGORİ) ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻",
        "desc": "Kod yazımı, hata ayıklama ve teknik analizde şu an dünyanın en iyisi.",
        "alternatives": ["Cursor AI", "GitHub Copilot", "DeepSeek-V3"]
    },
    "Görsel ve Tasarım": {
        "name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨",
        "desc": "Profesyonel sanatsal görsel üretiminde rakipsiz.",
        "alternatives": ["DALL-E 3", "Leonardo AI", "Recraft V3"]
    },
    "Hızlı Bilgi ve Araştırma": {
        "name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍",
        "desc": "İnterneti tarayıp kaynak göstererek cevap veren akıllı arama motoru.",
        "alternatives": ["Grok-2", "SearchGPT", "Phind"]
    },
    "Metin ve Yazışma": {
        "name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️",
        "desc": "Genel asistanlık, yaratıcı yazarlık ve sohbet için standart.",
        "alternatives": ["Google Gemini", "Mistral Large", "Jasper"]
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬",
        "desc": "Gerçekçi ve yüksek çözünürlüklü video klipler üretir.",
        "alternatives": ["Runway Gen-3", "Kling AI", "Sora"]
    },
    "Ses ve Müzik": {
        "name": "Suno AI", "url": "https://suno.com", "icon": "🎵",
        "desc": "Sözlü veya enstrümantal tam uzunlukta şarkılar besteler.",
        "alternatives": ["Udio", "ElevenLabs", "Adobe Podcast"]
    },
    "Sunum ve Doküman": {
        "name": "Gamma App", "url": "https://gamma.app", "icon": "📊",
        "desc": "Saniyeler içinde profesyonel sunumlar ve web sayfaları hazırlar.",
        "alternatives": ["Canva Magic", "Tome", "Beautiful.ai"]
    },
    "Veri Analizi ve Excel": {
        "name": "Julius AI", "url": "https://julius.ai", "icon": "📈",
        "desc": "Karmaşık veri tablolarını analiz eder ve grafikler oluşturur.",
        "alternatives": ["ChatGPT Analysis", "Rows", "Akkio"]
    },
    "Akademik ve PDF Analizi": {
        "name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄",
        "desc": "Uzun PDF dökümanlarını okur, özetler ve soruları yanıtlar.",
        "alternatives": ["Humata AI", "Consensus", "Elicit"]
    },
    "SEO ve Pazarlama": {
        "name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀",
        "desc": "Google'da üst sıralara çıkmak için içerik optimizasyonu yapar.",
        "alternatives": ["Copy.ai", "Writesonic", "Semrush"]
    }
}

# --- 3. ARAYÜZ (UI) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, senin için **en iyi AI ekosistemini** kuralım.")

with st.sidebar:
    st.title("👨‍💻 Enes Boz AI Lab")
    st.info("Bu sistem, Gemini altyapısını kullanarak ihtiyacınıza en uygun aracı saniyeler içinde belirler.")
    st.markdown("---")
    st.caption("Versiyon: 2.5.0")
    st.caption("Bölge: Türkiye (Global Support)")

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Şirketim için modern bir logo ve tanıtım müziği istiyorum.")

if st.button("En Uygun AI'ı Bul"):
    if query:
        with st.spinner('Yapay Zeka Uzmanları Tartışıyor...'):
            try:
                # Dinamik Kategori Eşleşmesi
                categories = list(AI_DIRECTORY.keys())
                prompt = f"Kullanıcı isteği: {query}. Bu isteğe en uygun tek bir kategoriyi seç: {categories}. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                
                res_text = response.text.strip()
                matched_cat = next((cat for cat in categories if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                
                res = AI_DIRECTORY[matched_cat]
                st.balloons()
                
                # ANA SONUÇ EKRANI
                st.markdown(f"""
                <div class="ai-card">
                    <h2 style='margin-top: 0;'>{res['icon']} <span style='color: #FF4B4B;'>Önerilen: {res['name']}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em; line-height: 1.6;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.link_button(f"{res['name']} Web Sitesini Aç", res['url'], use_container_width=True)
                
                # ALTERNATİFLER BÖLÜMÜ
                st.markdown("<br><h4 style='color: #444;'>🔁 Popüler Alternatifler</h4>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error("Küçük bir teknik pürüz oluştu. Lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen bir görev veya hayal ettiğiniz projeyi yazın.")

# Footer
st.markdown("<br><br><center style='opacity: 0.3; font-size: 0.8em;'>© 2026 | Enes Boz AI Lab | Tüm AI Hakları Saklıdır</center>", unsafe_allow_html=True)
