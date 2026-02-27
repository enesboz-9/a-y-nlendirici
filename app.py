import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .ai-card { padding: 25px; border-radius: 15px; background-color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eaeaea; margin-bottom: 20px; }
    .alt-card { padding: 12px; border-radius: 10px; background-color: #ffffff; margin-top: 10px; border: 2px solid #f1f3f5; border-left: 5px solid #FF4B4B; color: #1a1a1a !important; font-weight: 600; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR (KOTA DOSTU SIRALAMA) ---
@st.cache_resource
def initialize_ai():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Key Eksik!"
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # 1.5-Flash en yüksek kotaya (1500/gün) sahip olduğu için onu başa aldık
        model_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-lite']
        
        for m_name in model_list:
            try:
                test_model = genai.GenerativeModel(m_name)
                # Bağlantıyı sessizce kontrol et
                return test_model, m_name
            except: continue
        return None, "Tüm modellerin kotası dolmuş."
    except Exception as e: return None, str(e)

model, active_model_name = initialize_ai()

# --- 3. VERİ TABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻", "desc": "Kod yazımı ve teknik analizde dünya lideri.", "alternatives": ["Cursor AI", "GitHub Copilot"]},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨", "desc": "Profesyonel sanatsal görsel üretiminde rakipsiz.", "alternatives": ["DALL-E 3", "Leonardo AI"]},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍", "desc": "Güncel internet verisiyle kaynak gösteren arama motoru.", "alternatives": ["Grok-2", "SearchGPT"]},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️", "desc": "Yaratıcı yazarlık ve genel asistanlık için standart.", "alternatives": ["Google Gemini", "Mistral Large"]},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬", "desc": "Gerçekçi yapay zeka videoları üretir.", "alternatives": ["Runway Gen-3", "Kling AI"]},
    "Ses ve Müzik": {"name": "Suno AI", "url": "https://suno.com", "icon": "🎵", "desc": "Tam uzunlukta şarkılar besteler.", "alternatives": ["Udio", "ElevenLabs"]},
    "Sunum ve Doküman": {"name": "Gamma App", "url": "https://gamma.app", "icon": "📊", "desc": "Hızlıca profesyonel sunumlar hazırlar.", "alternatives": ["Canva Magic", "Tome"]},
    "Veri Analizi ve Excel": {"name": "Julius AI", "url": "https://julius.ai", "icon": "📈", "desc": "Veri tablolarını analiz eder.", "alternatives": ["ChatGPT Analysis", "Rows"]},
    "Akademik ve PDF": {"name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄", "desc": "PDF'leri okur ve özetler.", "alternatives": ["Humata AI", "Consensus"]},
    "SEO ve Pazarlama": {"name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀", "desc": "İçerik optimizasyonu yapar.", "alternatives": ["Copy.ai", "Writesonic"]}
}

# --- 4. UI ---
st.title("🎯 Akıllı AI Yönlendirici")
with st.sidebar:
    st.title("👨‍💻 Enes Boz Lab")
    if model: st.success(f"Aktif Motor: {active_model_name}")
    st.caption("Versiyon: 2.8.0")

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Python ile yılan oyunu yaz.")

if st.button("En Uygun AI'ı Bul"):
    if not model:
        st.error("Şu an tüm modeller kotalı. 1 dakika sonra tekrar deneyin.")
    elif query:
        with st.spinner('Zeka motorları çalışıyor...'):
            try:
                cats = list(AI_DIRECTORY.keys())
                # KISA PROMPT (Token tasarrufu için)
                prompt = f"Soru: {query}. Kategori listesi: {cats}. Sadece kategori adını yaz."
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                matched_cat = next((c for c in cats if c.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                st.balloons()
                st.markdown(f'<div class="ai-card"><h2 style="margin-top: 0;">{res["icon"]} <span style="color: #FF4B4B;">Önerilen: {res["name"]}</span></h2><p style="color: #1a1a1a;">{res["desc"]}</p></div>', unsafe_allow_html=True)
                st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                st.markdown("<br><b>🔁 Alternatifler:</b>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]: st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Kısa süreli kota dolumu. Lütfen 30 saniye bekleyip tekrar basın.")
    else: st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
