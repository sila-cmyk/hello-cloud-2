import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# Render üzerindeki veritabanı bağlantı adresini alır
DATABASE_URL = os.environ.get('DATABASE_URL')

def connect_db():
    # 'sslmode=require' ekleyerek bağlantı hatasını çözüyoruz
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        # 1. Tabloyu oluşturma komutu
        cur.execute('''
            CREATE TABLE IF NOT EXISTS mesajlar (
                id SERIAL PRIMARY KEY,
                isim VARCHAR(100),
                mesaj TEXT
            );
        ''')
        
        # 2. Örnek bir veri ekleyelim (Test için)
        cur.execute("INSERT INTO mesajlar (isim, mesaj) VALUES (%s, %s)", ("Gemini", "Selam, veritabanı harika çalışıyor!"))
        
        # 3. Eklediğimiz veriyi geri çekelim
        cur.execute("SELECT isim, mesaj FROM mesajlar;")
        sonuc = cur.fetchall()
        
        conn.commit() # Değişiklikleri kaydetmek için şart!
        cur.close()
        conn.close()
        
        return f"Tablo oluşturuldu ve veri eklendi! Veritabanındaki mesajlar: {sonuc}"
    
    except Exception as e:
        return f"Hata: {str(e)}"

# Render için gerekli port ve host ayarları
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
