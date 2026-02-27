import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="AI Router | Enes Boz", 
    page_icon="🎯", 
    layout="centered"
)

# Görsel Düzenleme: Okunabilir Yazılar ve Modern Kartlar
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; border-radius: 20px; height: 3.5em; 
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
    }
    .ai-card { 
        padding: 20px; border-radius: 15px; background-color: white; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #eee;
        margin-bottom: 20px;
    }
    .alt-card { 
        padding: 12px; border-radius: 10px; background-color: #ffffff; 
        margin-top: 10px; border: 2px solid #f0f0f0; border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; font-weight: 600; text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR (HATA DİRENÇLİ BAĞLANTI) ---
@st.cache_resource
def get_ai_model():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "Secrets: GOOGLE_API_KEY bulunamadı!"
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 404 ve 429 hatalarını minimize etmek için en stabil model ismi
        # 'models/' ön eki olmadan en yalın haliyle tanımlıyoruz
        model_name = 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)
        return model, model_name
    except Exception as e:
        return None, str(e)

model_engine, active_model = get_ai_model()

# --- 3. GENİŞ VERİ TABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻", "desc": "Kod yazımı ve teknik analizde dünya lideri.", "alternatives": ["Cursor AI", "GitHub Copilot"]},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨", "desc": "Profesyonel sanatsal görsel üretiminde rakipsiz.", "alternatives": ["DALL-E 3", "Leonardo AI"]},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍", "desc": "Güncel internet verisiyle kaynak gösteren arama motoru.", "alternatives": ["Grok-2", "SearchGPT"]},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️", "desc": "Yaratıcı yazarlık ve genel asistanlık için standart.", "alternatives": ["Google Gemini", "Mistral Large"]},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬", "desc": "Gerçekçi yapay zeka videoları üretir.", "alternatives": ["Runway Gen-3", "Kling AI"]},
    "Ses ve Müzik": {"name": "Suno AI", "url": "https://suno.com", "icon": "🎵", "desc": "Tam uzunlukta şarkılar besteler.", "alternatives": ["Udio", "ElevenLabs"]},
    "Sunum ve Doküman": {"name": "Gamma App", "url": "https://gamma.app", "icon": "📊", "desc": "Hızlıca profesyonel sunumlar hazırlar.", "alternatives": ["Canva Magic", "Tome"]},
    "Veri Analizi ve Excel": {"name": "Julius AI", "url": "https://julius.ai", "icon": "📈", "desc": "Karmaşık veri tablolarını analiz eder.", "alternatives": ["ChatGPT Analysis", "Rows"]},
    "Akademik ve PDF": {"name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄", "desc": "PDF'leri okur, özetler ve soruları yanıtlar.", "alternatives": ["Humata AI", "Consensus"]},
    "SEO ve Pazarlama": {"name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀", "desc": "Google'da üst sıralara çıkmak için içerik optimizasyonu yapar.", "alternatives": ["Copy.ai", "Writesonic"]}
}

# --- 4. ARAYÜZ (UI) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("Hangi görev için hangi yapay zekayı kullanman gerektiğini bulalım.")

with st.sidebar:
    st.title("👨‍💻 Enes Boz Lab")
    if model_engine:
        st.success(f"Bağlantı: {active_model}")
    else:
        st.error("Bağlantı Hatası!")
    st.caption("Versiyon: 3.0.0")

query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Modern bir logo ve marka müziği...")

if st.button("En Uygun AI'ı Belirle"):
    if not model_engine:
        st.error(f"Sistem başlatılamadı: {active_model}")
    elif query:
        with st.spinner('AI motorları analiz ediyor...'):
            try:
                cats = list(AI_DIRECTORY.keys())
                prompt = f"Soru: {query}. Bu soruyu şu kategorilerden hangisi en iyi çözer? {cats}. Sadece kategori adını yaz."
                
                response = model_engine.generate_content(prompt)
                res_text = response.text.strip()
                
                # Eşleşen kategoriyi bul
                matched_cat = next((c for c in cats if c.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                
                # SONUÇ KARTI
                st.markdown(f'''
                <div class="ai-card">
                    <h2 style="margin-top: 0;">{res["icon"]} <span style="color: #FF4B4B;">Önerilen: {res["name"]}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em; line-height: 1.5;">{res["desc"]}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                st.link_button(f"{res['name']} Web Sitesini Aç", res['url'], use_container_width=True)
                
                # ALTERNATİFLER
                st.markdown("<br><b>🔁 Popüler Alternatifler:</b>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                if "429" in str(e):
                    st.warning("⏱️ Çok fazla istek gönderildi. Lütfen 20 saniye bekleyip tekrar deneyin.")
                elif "404" in str(e):
                    st.error("Model ismi hatası. Lütfen API Key'inizin geçerli olduğunu kontrol edin.")
                else:
                    st.error(f"Bir pürüz çıktı: {e}")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

st.markdown("<br><hr><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
