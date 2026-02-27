import streamlit as st
import google.generativeai as genai
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .ai-card { padding: 25px; border-radius: 15px; background-color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eaeaea; }
    .alt-card { padding: 10px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #FF4B4B; color: #1a1a1a !important; font-weight: 600; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR (MİNİMUM İSTEK MODU) ---
@st.cache_resource
def get_ai_model():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # En geniş kotalı ve en stabil model
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return str(e)

model_engine = get_ai_model()

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

# --- 4. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("Görevi yaz, en uygun AI'ı bulalım.")

with st.sidebar:
    st.title("👨‍💻 Enes Boz Lab")
    st.info("Sistem: Gemini 1.5 Flash (Stabil)")
    st.caption("Versiyon: 2.9.0")

query = st.text_input("Bugün ne yapmak istiyorsun?", key="user_input")

if st.button("AI Modelini Belirle"):
    if not isinstance(model_engine, genai.GenerativeModel):
        st.error(f"Sistem başlatılamadı: {model_engine}")
    elif query:
        with st.spinner('Lütfen bekleyin, analiz ediliyor...'):
            try:
                cats = list(AI_DIRECTORY.keys())
                prompt = f"Soru: {query}. Kategoriler: {cats}. Sadece kategori adını döndür."
                
                response = model_engine.generate_content(prompt)
                res_text = response.text.strip()
                
                matched_cat = next((c for c in cats if c.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                st.markdown(f'''
                <div class="ai-card">
                    <h2 style="margin-top: 0;">{res["icon"]} <span style="color: #FF4B4B;">Önerilen: {res["name"]}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em;">{res["desc"]}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                
                st.markdown("<br><b>🔁 Alternatifler:</b>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                if "429" in str(e):
                    st.warning("⏱️ Çok hızlı gidiyoruz! Google bizi 15 saniye beklemeye aldı. Lütfen biraz bekleyip tekrar deneyin.")
                else:
                    st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

st.markdown("<br><hr><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
