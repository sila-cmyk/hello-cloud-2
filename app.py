from flask import Flask, request, render_template_string
import os
import psycopg2

app = Flask(__name__)

def connect_db():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# HTML Tasarımı (Basit bir form ve liste)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ziyaretçi Defteri</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 50px auto; line-height: 1.6; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; }
        button { background: #007bff; color: white; border: none; padding: 10px; cursor: pointer; }
        .mesaj-kutusu { border-bottom: 1px solid #ccc; padding: 10px 0; }
    </style>
</head>
<body>
    <h2>Ziyaretçi Defteri</h2>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adınız" required>
        <textarea name="mesaj" placeholder="Mesajınız" required></textarea>
        <button type="submit">Gönder</button>
    </form>
    <hr>
    <h3>Gelen Mesajlar</h3>
    {% for isim, mesaj in mesajlar %}
        <div class="mesaj-kutusu">
            <strong>{{ isim }}:</strong> {{ mesaj }}
        </div>
    {% endfor %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connect_db()
    cur = conn.cursor()
    
    # Tabloyu her ihtimale karşı hazır tut
    cur.execute("CREATE TABLE IF NOT EXISTS mesajlar (id SERIAL PRIMARY KEY, isim TEXT, mesaj TEXT);")
    
    if request.method == 'POST':
        isim = request.form.get('isim')
        mesaj = request.form.get('mesaj')
        cur.execute("INSERT INTO mesajlar (isim, mesaj) VALUES (%s, %s)", (isim, mesaj))
        conn.commit()

    # Tüm mesajları çek
    cur.execute("SELECT isim, mesaj FROM mesajlar ORDER BY id DESC;")
    tum_mesajlar = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, mesajlar=tum_mesajlar)

if __name__ == '__main__':
    app.run(debug=True)
