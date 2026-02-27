import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TASARIM AYARLARI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    /* Buton Tasarımı */
    .stButton>button { 
        width: 100%; border-radius: 20px; height: 3.5em; 
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
    }
    /* Ana Sonuç Kartı */
    .ai-card { 
        padding: 25px; border-radius: 15px; background-color: white; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eaeaea; 
        margin-bottom: 20px;
    }
    /* Alternatif Kutucukları - Okunabilir Siyah Yazı */
    .alt-card { 
        padding: 12px; border-radius: 10px; background-color: #ffffff; 
        margin-top: 10px; border: 2px solid #f1f3f5; border-left: 5px solid #FF4B4B;
        color: #1a1a1a !important; font-weight: bold; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR (KOTA DOSTU & 404 HATASIZ) ---
@st.cache_resource
def initialize_ai():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı (Secrets) bulunamadı!"
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 404 hatasını önlemek için en yalın isim: 'gemini-1.5-flash'
        # Bu model ücretsiz katmanda günlük 1500 sorguya izin verir.
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model, "Gemini 1.5 Flash"
    except Exception as e:
        return None, str(e)

model_engine, active_model_name = initialize_ai()

# --- 3. VERİTABANI (10 KATEGORİ) ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 3.5 Sonnet", "url": "https://claude.ai", "icon": "💻", "desc": "Kod yazımı ve teknik analizde dünya lideri.", "alternatives": ["Cursor AI", "GitHub Copilot"]},
    "Görsel ve Tasarım": {"name": "Midjourney", "url": "https://www.midjourney.com", "icon": "🎨", "desc": "Profesyonel sanatsal görsel üretiminde rakipsiz.", "alternatives": ["DALL-E 3", "Leonardo AI"]},
    "Hızlı Bilgi ve Araştırma": {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "icon": "🔍", "desc": "Güncel internet verisiyle kaynak gösteren arama motoru.", "alternatives": ["Grok-2", "SearchGPT"]},
    "Metin ve Yazışma": {"name": "ChatGPT (GPT-4o)", "url": "https://chatgpt.com", "icon": "✍️", "desc": "Yaratıcı yazarlık ve genel asistanlık için standart.", "alternatives": ["Google Gemini", "Mistral Large"]},
    "Video Üretimi": {"name": "Luma Dream Machine", "url": "https://lumalabs.ai", "icon": "🎬", "desc": "Gerçekçi yapay zeka videoları üretir.", "alternatives": ["Runway Gen-3", "Kling AI"]},
    "Ses ve Müzik": {"name": "Suno AI", "url": "https://suno.com", "icon": "🎵", "desc": "Tam uzunlukta şarkılar ve besteler üretir.", "alternatives": ["Udio", "ElevenLabs"]},
    "Sunum ve Doküman": {"name": "Gamma App", "url": "https://gamma.app", "icon": "📊", "desc": "Hızlıca profesyonel sunumlar hazırlar.", "alternatives": ["Canva Magic", "Tome"]},
    "Veri Analizi ve Excel": {"name": "Julius AI", "url": "https://julius.ai", "icon": "📈", "desc": "Karmaşık veri tablolarını analiz eder.", "alternatives": ["ChatGPT Analysis", "Rows"]},
    "Akademik ve PDF": {"name": "ChatPDF", "url": "https://www.chatpdf.com", "icon": "📄", "desc": "PDF dökümanlarını okur ve özetler.", "alternatives": ["Humata AI", "Consensus"]},
    "SEO ve Pazarlama": {"name": "Surfer SEO", "url": "https://surferseo.com", "icon": "🚀", "desc": "SEO ve içerik optimizasyonu yapar.", "alternatives": ["Copy.ai", "Writesonic"]}
}

# --- 4. ARAYÜZ (UI) ---
st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("İhtiyacın olan görevi yaz, en uygun AI ekosistemini bulalım.")

with st.sidebar:
    st.title("👨‍💻 Enes Boz Lab")
    if model_engine:
        st.success(f"Sistem Aktif: {active_model_name}")
    else:
        st.error("Bağlantı Kurulamadı!")
    st.caption("Versiyon: 3.5.0")

query = st.text_input("Bugün ne oluşturmak istiyorsun?", placeholder="Örn: Modern bir logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Belirle"):
    if not model_engine:
        st.error(f"Hata: {active_model_name}")
    elif query:
        with st.spinner('Analiz ediliyor...'):
            try:
                cats = list(AI_DIRECTORY.keys())
                prompt = f"Soru: {query}. Bu soruyu şu kategorilerden hangisi en iyi çözer? {cats}. Sadece kategori adını yaz."
                
                response = model_engine.generate_content(prompt)
                res_text = response.text.strip()
                
                matched_cat = next((c for c in cats if c.lower() in res_text.lower()), "Metin ve Yazışma")
                res = AI_DIRECTORY[matched_cat]
                
                st.balloons()
                
                # ANA SONUÇ KARTI
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
                    st.warning("⏱️ Çok hızlı gidiyorsun! Google 15 saniye bekletiyor. Lütfen birazdan tekrar dene.")
                else:
                    st.error(f"Bir pürüz çıktı: {e}")
    else:
        st.warning("Lütfen bir görev tanımlayın.")

st.markdown("<br><hr><center style='opacity: 0.3;'>© 2026 | Enes Boz AI Lab</center>", unsafe_allow_html=True)
