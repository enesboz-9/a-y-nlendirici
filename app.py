import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA VE GÜVENLİK ---
try:
    # Streamlit Secrets'tan anahtarı al
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # HATA ÇÖZÜMÜ: 'models/' ön eki ve '-latest' takısı 404 hatalarını çözer
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Sistem başlatılamadı: {e}")
    st.stop()

# --- 2. AI ARAÇLARI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", 
        "url": "https://claude.ai", 
        "desc": "Karmaşık yazılım projeleri ve mantık yürütme için en iyisi."
    },
    "Görsel Tasarım": {
        "name": "Midjourney", 
        "url": "https://www.midjourney.com", 
        "desc": "Logo, UI/UX tasarımı ve sanatsal görseller için profesyonel araç."
    },
    "Araştırma ve Bilgi": {
        "name": "Perplexity AI", 
        "url": "https://www.perplexity.ai", 
        "desc": "İnterneti tarayarak kaynak gösteren akıllı arama motoru."
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", 
        "url": "https://lumalabs.ai/dream-machine", 
        "desc": "Gerçekçi ve yüksek çözünürlüklü AI videoları oluşturur."
    },
    "Metin ve Yazarlık": {
        "name": "ChatGPT", 
        "url": "https://chatgpt.com", 
        "desc": "Blog yazıları, özetleme ve genel asistanlık işlerinde lider."
    }
}

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("<p style='color: grey;'>Enes Boz tarafından tasarlanmıştır.</p>", unsafe_allow_html=True)
st.divider()

query = st.text_input("Bugün ne yapmak istiyorsun?", placeholder="Örn: Bir web sitesi için logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if query:
        with st.spinner('Analiz ediliyor, lütfen bekleyin...'):
            try:
                # Modeli daha doğrudan bir yöntemle çağırıyoruz
                prompt = f"Aşağıdaki isteği şu kategorilerden biriyle eşleştir: {list(AI_DIRECTORY.keys())}. İsteği oku ve SADECE kategori ismini yaz: '{query}'"
                
                response = model.generate_content(prompt)
                
                # Yanıtın boş gelme ihtimaline karşı kontrol
                if response and response.text:
                    ai_decision = response.text.strip()
                    
                    matched_cat = None
                    for cat in AI_DIRECTORY.keys():
                        if cat.lower() in ai_decision.lower():
                            matched_cat = cat
                            break
                    
                    if matched_cat:
                        res = AI_DIRECTORY[matched_cat]
                        st.balloons()
                        st.success(f"Analiz Tamamlandı! Senin için en iyisi: **{res['name']}**")
                        
                        with st.container(border=True):
                            st.subheader(f"🚀 {res['name']}")
                            st.write(res['desc'])
                            st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
                    else:
                        st.warning("Eşleşme sağlanamadı, lütfen daha detaylı bir cümle yazın.")
                else:
                    st.error("API'den boş yanıt döndü. Lütfen tekrar deneyin.")
            
            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")

# Alt Bilgi
st.markdown("<br><br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
