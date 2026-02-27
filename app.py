import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env dosyasından anahtarı çek
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Yapılandırma
genai.configure(api_key=api_key)
# Hız için flash modelini ve düşük güvenlik filtrelerini kullanıyoruz (takılmaması için)
model = genai.GenerativeModel('gemini-1.5-flash')

AI_DIRECTORY = {
    "Yazılım ve Kodlama": {"name": "Claude 4.5", "url": "https://claude.ai", "desc": "Karmaşık kodlama ve teknik analizler için en iyi tercih."},
    "Görsel Oluşturma": {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "Yüksek kaliteli sanatsal görseller ve tasarımlar için."},
    "Araştırma ve Bilgi": {"name": "Perplexity", "url": "https://www.perplexity.ai", "desc": "Güncel internet verileriyle kaynak göstererek cevap verir."},
    "Video Üretimi": {"name": "Sora / Veo", "url": "https://openai.com/sora", "desc": "Gerçekçi ve yüksek çözünürlüklü yapay zeka videoları için."},
    "Metin ve Yazarlık": {"name": "ChatGPT (GPT-5)", "url": "https://chatgpt.com", "desc": "Yaratıcı yazarlık, özetleme ve günlük asistanlık için."}
}

def analyze_intent(user_input):
    # Promptu daha netleştirip cevabı tek kelimeye zorladık ki takılmasın
    prompt = f"""Kullanıcı isteği: "{user_input}"
    Bu isteği şu kategorilerden sadece birine ata: {list(AI_DIRECTORY.keys())}.
    Cevap olarak SADECE kategori ismini yaz. Bilmiyorum deme, en yakın olanı seç."""
    
    try:
        # 10 saniye içinde cevap gelmezse hata vermesi için timeout simülasyonu (opsiyonel)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None

# --- Arayüz Tasarımı ---
st.set_page_config(page_title="Akıllı AI Yönlendirici", page_icon="🎯")

# Başlık ve Tasarımcı Bilgisi
st.title("🎯 Akıllı AI Yönlendirici")
st.caption("Enes Boz tarafından tasarlanmıştır.")

st.markdown("---")

query = st.text_input("Ne yapmak istiyorsunuz?", placeholder="Örn: Bir web sitesi için logo tasarlatmak istiyorum.")

if st.button("En Uygun AI'ı Göster"):
    if query:
        with st.spinner('Sizin için en iyi araç belirleniyor...'):
            category_result = analyze_intent(query)
            
            # API'den gelen cevabı kontrol et
            matched_category = None
            if category_result:
                for cat in AI_DIRECTORY.keys():
                    if cat.lower() in category_result.lower():
                        matched_category = cat
                        break
            
            if matched_category:
                res = AI_DIRECTORY[matched_category]
                st.balloons() # Başarı görseli
                st.success(f"Bulundu! Sizin için en uygun kategori: **{matched_category}**")
                
                # Bilgi Kartı
                with st.container():
                    st.subheader(f"Önerilen Araç: {res['name']}")
                    st.write(res['desc'])
                    st.link_button(f"{res['name']} Sayfasına Git 🚀", res['url'], use_container_width=True)
            else:
                st.error("Şu an analiz yapılamıyor. Lütfen internetinizi kontrol edin veya tekrar deneyin.")
    else:
        st.warning("Lütfen bir isteğinizi belirtin.")

# Alt Bilgi
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='opacity: 0.5;'>© 2026 | Enes Boz</center>", unsafe_allow_html=True)
