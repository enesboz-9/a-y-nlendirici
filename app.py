import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

# CSS - Yazı Rengi ve Kontrast Düzenlemesi
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .ai-card { padding: 25px; border-radius: 15px; background-color: white; box-shadow: 0 10px 15px rgba(0,0,0,0.05); border: 1px solid #eaeaea; }
    
    /* Alternatif Kutucukları ve Yazı Fontu */
    .alt-card { 
        padding: 12px; 
        border-radius: 10px; 
        background-color: #ffffff; 
        margin-top: 10px; 
        border: 2px solid #f1f3f5;
        border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; /* Koyu siyah/füme yazı rengi */
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_ai():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        for m_name in ['gemini-3-flash-preview', 'gemini-1.5-flash', 'gemini-1.0-pro']:
            try:
                test_model = genai.GenerativeModel(m_name)
                test_model.generate_content("ping")
                return test_model
            except: continue
        return None
    except: return None

model = initialize_ai()

# --- 2. VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻",
        "desc": "Kod yazımı ve teknik dökümantasyon için lider.",
        "alternatives": ["Cursor AI", "GitHub Copilot"]
    },
    "Görsel ve Tasarım": {
        "name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨",
        "desc": "Profesyonel sanatsal görsel üretim aracı.",
        "alternatives": ["DALL-E 3", "Leonardo AI"]
    },
    "Hızlı Bilgi ve Araştırma": {
        "name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍",
        "desc": "Canlı internet verisiyle akademik araştırma asistanı.",
        "alternatives": ["Grok-2", "SearchGPT"]
    },
    "Metin ve Yazışma": {
        "name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️",
        "desc": "Yaratıcı yazarlık ve genel asistanlık için ideal.",
        "alternatives": ["Google Gemini", "Mistral Large"]
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬",
        "desc": "Yüksek çözünürlüklü yapay zeka videoları.",
        "alternatives": ["Runway Gen-3", "Kling AI"]
    }
}

# --- 3. ARAYÜZ ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, en iyisini ve alternatiflerini bulalım.")

with st.sidebar:
    st.title("Bilgi")
    st.caption("Geliştirici: Enes Boz")
    st.caption("Versiyon: 2.3.0")

query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Python ile veri analizi yapmak istiyorum.")

if st.button("En Uygun AI'ı Bul"):
    if query:
        with st.spinner('Analiz ediliyor...'):
            try:
                prompt = f"Soru: {query}. Kategoriler: {list(AI_DIRECTORY.keys())}. Sadece bir kategori adını yaz."
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                matched_cat = next((cat for cat in AI_DIRECTORY.keys() if cat.lower() in res_text.lower()), "Metin ve Yazışma")
                
                res = AI_DIRECTORY[matched_cat]
                st.balloons()
                
                # ANA SONUÇ KARTI
                st.markdown(f"""
                <div class="ai-card">
                    <h2 style='margin-top: 0;'>{res['icon']} <span style='color: #FF4B4B;'>Önerilen: {res['name']}</span></h2>
                    <p style="color: #1a1a1a; font-size: 1.1em; font-weight: 400;">{res['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"{res['name']} Sitesine Git", res['url'], use_container_width=True)
                
                # ALTERNATİFLER BÖLÜMÜ
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🔁 Popüler Alternatifler")
                cols = st.columns(len(res['alternatives']))
                
                for i, alt in enumerate(res['alternatives']):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="alt-card">
                            {alt}
                        </div>
                        """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

st.markdown("<br><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
