import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

# CSS - Yazı Rengi ve Kontrast Düzenlemesi
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; font-weight: bold; border: none; }
    .ai-card { padding: 25px; border-radius: 15px; background-color: white; box-shadow: 0 10px 15px rgba(0,0,0,0.05); border: 1px solid #eaeaea; }
    .alt-card { 
        padding: 12px; border-radius: 10px; background-color: #ffffff; 
        margin-top: 10px; border: 2px solid #f1f3f5; border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; font-weight: 600; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_ai():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Ücretsiz katmanın kralı: gemini-1.5-flash
        # Hem zekidir hem de günlük 1500 sorgu hakkı verir.
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except:
        return None

model = initialize_ai()

# --- 2. VERİTABANI (Kategorileri 10'a Çıkardık) ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻", "desc": "Kod yazımı ve teknik analiz için dünya lideri.", "alternatives": ["Cursor AI", "GitHub Copilot"]},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨", "desc": "Profesyonel sanatsal görsel üretim aracı.", "alternatives": ["DALL-E 3", "Leonardo AI"]},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍", "desc": "İnterneti tarayıp kaynak gösteren akıllı arama motoru.", "alternatives": ["Grok-2", "SearchGPT"]},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️", "desc": "Yaratıcı yazarlık ve genel asistanlık için standart.", "alternatives": ["Google Gemini", "Mistral Large"]},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬", "desc": "Gerçekçi ve yüksek çözünürlüklü yapay zeka videoları.", "alternatives": ["Runway Gen-3", "Kling AI"]},
    "Ses ve Müzik": {"name": "Suno AI", "url": "https://suno.com", "icon": "🎵", "desc": "Tam uzunlukta şarkılar ve besteler üretir.", "alternatives": ["Udio", "ElevenLabs"]},
    "Sunum ve Doküman": {"name": "Gamma App", "url": "https://gamma.app", "icon": "📊", "desc": "Saniyeler içinde profesyonel sunumlar hazırlar.", "alternatives": ["Canva Magic", "Tome"]},
    "Veri Analizi ve Excel": {"name": "Julius AI", "url": "https://julius.ai", "icon": "📈", "desc": "Karmaşık veri tablolarını analiz eder.", "alternatives": ["ChatGPT Analysis", "Rows"]},
    "Akademik ve PDF": {"name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄", "desc": "PDF dökümanlarını okur ve özetler.", "alternatives": ["Humata AI", "Consensus"]},
    "SEO ve Pazarlama": {"name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀", "desc": "İçerik optimizasyonu ve SEO analizi yapar.", "alternatives": ["Copy.ai", "Writesonic"]}
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, en iyisini ve alternatiflerini bulalım.")

with st.sidebar:
    st.title("Bilgi")
    st.info("Sistem: Gemini 1.5 Flash (Kota Dostu)")
    st.caption("Geliştirici: Enes Boz")
    st.caption("Versiyon: 3.2.0")

query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Modern bir logo ve tanıtım müziği istiyorum.")

if st.button("En Uygun AI'ı Bul"):
    if not model:
        st.error("API Anahtarı doğrulanamadı. Lütfen Secrets ayarlarını kontrol edin.")
        st.stop()

    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                cats = list(AI_DIRECTORY.keys())
                prompt = f"Kullanıcı isteği: {query}. Kategoriler: {cats}. Sadece bir kategori adını yaz."
                
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                
                matched_cat = next((cat for cat in cats if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                st.markdown(f"""
                <div class="ai-card">
                    <h2 style='margin-top: 0;'>{res['icon']} <span style='color: #FF4B4B;'>Önerilen: {res['name']}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em; font-weight: 400;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                
                st.markdown("<br><b>🔁 Popüler Alternatifler</b>", unsafe_allow_html=True)
                cols = st.columns(len(res['alternatives']))
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f'<div class="alt-card">{alt}</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                if "429" in str(e):
                    st.warning("⏱️ Çok hızlı gidiyorsun! 15 saniye bekleyip tekrar dene.")
                else:
                    st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

st.markdown("<br><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
