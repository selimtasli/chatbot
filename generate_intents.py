import pandas as pd
import random
import string

try:
    df = pd.read_excel("data/tek_market.xlsx")
    
    urun_listesi = df.iloc[:, 0].dropna().astype(str).unique().tolist() # İlk sütun Urun_Adi
    marka_listesi = df.iloc[:, 1].dropna().astype(str).unique().tolist() # İkinci sütun Marka
    
    print(f"✅ Excel Okundu: {len(urun_listesi)} Ürün, {len(marka_listesi)} Marka bulundu.")

except Exception as e:
    print(f"⚠️ Excel Hatası: {e}")
    urun_listesi = ["iPhone 15", "Samsung S24", "MacBook Air", "Dyson V15"]
    marka_listesi = ["Apple", "Samsung", "Dyson", "Sony"]

def lowercase_randomly(text):
    if random.random() < 0.5: return text.lower()
    return text

def add_filler_words(text):
    prefixes = ["Hocam", "Reis", "Acaba", "Şey", "Bi baksana", "Selam", "Pardon", "Usta", "Kral", "Bakar mısın"]
    if random.random() < 0.30: 
        text = f"{random.choice(prefixes)} {text}"
    return text

def add_typo(text):
    if random.random() > 0.3: return text
    
    char_list = list(text)
    if len(char_list) < 4: return text
    
    idx = random.randint(1, len(char_list) - 1)
    
    if random.random() > 0.5: 
        char_list[idx] = random.choice(string.ascii_lowercase)
    else: 
        if char_list[idx] != ' ':
            del char_list[idx]
            
    return "".join(char_list)

templates = {

    "greeting": [
        "Merhaba", "Selam", "Günaydın", "İyi günler", "Selamlar bot", 
        "Tünaydın", "Selamun aleyküm", "Merhabalar", "Slm",
        "İyi akşamlar", "Kolay gelsin", "Naber", "Hey", "Orada mısın?", 
        "Dükkan açık mı?", "Selam millet"
    ],

    "goodbye": [ 
        "Görüşürüz", "Hoşçakal", "Bay bay", "Kib", "Bye", "Kaçtım ben",
        "İyi çalışmalar", "Allah'a emanet",
        "Güle güle", "Sonra görüşürüz", "Çıkış yapıyorum", "Kapatıyorum", 
        "Müsadenle", "Sohbeti bitir", "Ben kaçtım"
    ],

    "ask_price": [
        "{urun} ne kadar",
        "{urun} fiyat",
        "{urun} için fiyat alabilir miyim",
        "{urun} kaça geliyor",
        "{urun} pahalı mı",
        "{urun} alınır mı",
        "{urun} fiyatı uçmuş mu",
        "{urun} var mı fiyatı ne",
        "selam {urun} fiyatı",
        "{marka} {urun} fiyat bilgisi",
        "{urun} bütçeme uyar mı",
        "{urun} hakkında fiyat bilgisi"
    ],

    "ask_stock": [
        "{urun} var mı",
        "{urun} kaldı mı",
        "{urun} bulunuyor mu",
        "{urun} mağazada var mı",
        "{urun} bugün alabilir miyim",
        "{urun} hemen teslim mi",
        "{urun} var mı fiyatı ne",
        "selam {urun} var mı",
        "{marka} ürünleri mevcut mu",
        "{urun} ne zaman gelir",
        "{urun} stoklar bitmiş mi",
        "{urun} var diyordular doğru mu"
    ],

    "tech_support": [
        "Telefon suya düştü ne yapmalıyım?", "Cihaza su kaçtı", "Üzerine kahve döküldü",
        "Telefona çay döküldü çalışır mı?", "Cihaz sıvı teması aldı", "Yağmurda ıslandı",
        "Suya düşen telefon garantiye girer mi?", "Pirinç işe yarar mı?",
        
        "Garanti süresi ne kadar?", "İade koşulları neler?", "Ürünü geri verebilir miyim?",
        "Değişim yapıyor musunuz?", "Kutuyu açtım iade olur mu?", "Faturam kayıp ne yapabilirim?",
        "Garanti belgesi yok", "Kaç gün içinde iade hakkım var?", "Ayıplı mal değişimi",
        
        "Telefon şarj olmuyor", "Şarj soketi bozuk", "Batarya çok çabuk bitiyor",
        "Pil sağlığı düştü", "Batarya şişti ne yapayım?", "Orijinal şarj aleti kullanmasam ne olur?",
        "Telefonu gece şarjda bırakmak zararlı mı?", "Şarj kablosu temassızlık yapıyor",
        
        "Ekran kırıldı garanti karşılar mı?", "Ekranda ölü piksel var", "Camı çatladı",
        "Dokunmatik çalışmıyor", "Ekran karardı gelmiyor", "Görüntü gidip geliyor",
        "Kasa yamuldu", "Telefon yere düştü açılmıyor", "Tuşlar basmıyor",
        
        "Cihaz çok ısınıyor", "Telefon ateş gibi oldu", "Oyun oynarken ısınıyor",
        "Telefon donuyor", "Sürekli kapanıp açılıyor", "Reset atıyor kendi kendine",
        "Mavi ekran verdi", "Wi-Fi bağlanmıyor", "Şebeke çekmiyor",
        
        "Bozuk ürün", "Tamir yapıyor musunuz?", "Teknik servis nerede?",
        "Cihaz arızalandı", "Servise nasıl gönderirim?", "Yardım lazım cihaz bozuldu",
        "Çalışmıyor", "Bozuldu", "Arıza var"
    ]
}

dataset = []

print("🔄 Veri seti üretiliyor... (Arkadaşının tekniğiyle)")

for intent, sentences in templates.items():
    count = 800 if intent in ["ask_price", "ask_stock"] else 200
    
    for _ in range(count):
        text = random.choice(sentences)
        
        if "{urun}" in text: 
            text = text.replace("{urun}", random.choice(urun_listesi))
        if "{marka}" in text: 
            text = text.replace("{marka}", random.choice(marka_listesi))
            
        text = lowercase_randomly(text) 
        text = add_filler_words(text)    
        text = add_typo(text)            
        
        dataset.append({"text": text, "label": intent})

df_output = pd.DataFrame(dataset)
df_output = df_output.sample(frac=1).reset_index(drop=True)

output_path = "data/intents.xlsx"
df_output.to_excel(output_path, index=False)

print(f"🎉 SÜPER! Toplam {len(df_output)} satırlık gelişmiş veri '{output_path}' konumuna kaydedildi.")
print("-" * 30)
print(df_output.head(10))