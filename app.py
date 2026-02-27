import streamlit as st
import google.generativeai as genai

# --- 1. GÜVENLİK VE YAPILANDIRMA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # API yapılandırmasını yaparken versiyon çakışmasını önlemek için doğrudan configure ediyoruz
    genai.configure(api_key=api_key)
    
    # Hata aldığın model ismini 'gemini-1.5-flash' olarak sadeleştiriyoruz 
    # veya 'models/gemini-1.5-flash-latest' deneyebilirsin.
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Başlatma Hatası: {e}")
    st.stop()

# --- 2. AI ARAÇLARI VERİTABANI ---
AI_DIRECTORY = {
    "Yazılım ve Kodlama": {
        "name": "Claude 3.5 Sonnet", 
        "url": "https://claude.ai", 
        "desc": "Karmaşık yazılım projeleri ve teknik analizler için en iyisi."
    },
    "Görsel Tasarım": {
        "name": "Midjourney", 
        "url": "https://www.midjourney.com", 
        "desc": "Logo ve UI/UX tasarımı için profesyonel çözümler."
    },
    "Araştırma ve Bilgi": {
        "name": "Perplexity AI", 
        "url": "https://www.perplexity.ai", 
        "desc": "İnterneti tarayarak kaynak gösteren akıllı arama motoru."
    },
    "Video Üretimi": {
        "name": "Luma Dream Machine", 
        "url": "https://lumalabs.ai/dream-machine", 
        "desc": "Gerçekçi AI videoları oluşturur."
    },
    "Metin ve Yazarlık": {
        "name": "ChatGPT", 
        "url": "https://chatgpt.com", 
        "desc": "Blog yazıları ve genel asistanlık işlerinde lider."
    }
}

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Router | Enes Boz", page_icon="🎯")

st.title("🎯 Akıllı AI Yönlendirici")
st.markdown("<p style='color: #666;'>Enes Boz tarafından tasarlanmıştır.</p>", unsafe_allow_html=True)
st.divider()

user_query = st.text_input("Ne yapmak istiyorsun?", placeholder="Örn: Logo tasarlatmak istiyorum...")

if st.button("En Uygun AI'ı Göster", type="primary"):
    if user_query:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Promptu çok daha basit tutuyoruz
                prompt = f"Aşağıdaki isteği sadece kategori adıyla eşleştir: '{user_query}'. Kategoriler: {list(AI_DIRECTORY.keys())}. Sadece kategori adını yaz."
                
                # API çağrısını yapıyoruz
                response = model.generate_content(user_query) # Direkt sorguyu gönderip test edelim
                
                # Eğer response.text hata verirse alternatif metot:
                ai_decision = response.candidates[0].content.parts[0].text.strip()
                
                matched_cat = None
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in ai_decision.lower():
                        matched_cat = cat
                        break
                
                if matched_cat:
                    res = AI_DIRECTORY[matched_cat]
                    st.balloons()
                    st.success(f"Analiz Tamamlandı! En uygun araç: **{res['name']}**")
                    with st.container(border=True):
                        st.subheader(f"🚀 {res['name']}")
                        st.write(res['desc'])
                        st.link_button(f"{res['name']} Sayfasına Git", res['url'], use_container_width=True)
                else:
                    st.warning("Eşleşme sağlanamadı. Lütfen daha net bir ifade deneyin.")
            
            except Exception as e:
                # Hatayı daha detaylı yakalamak için
                st.error(f"Teknik bir sorun oluştu. Lütfen tekrar deneyin. Detay: {e}")
    else:
        st.warning("Lütfen bir cümle yazın.")

st.markdown("<br><br><center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
