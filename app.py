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
        
        # Burası örnek bir sorgudur, kendi tablo ismine göre değiştirebilirsin
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return f"Veritabanına başarıyla bağlandım! DB Versiyonu: {db_version}"
    
    except Exception as e:
        return f"Bağlantı hatası oluştu: {str(e)}"

# Render için gerekli port ve host ayarları
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
