from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

FILE_PATH = 'Gästbok.txt'

HTML = '''
<!doctype html>
<html lang="sv">
<head>
    <meta charset="utf-8">
    <title>Gästbok</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background-color: #fafafa; }
        h1 { color: #333; }
        form { margin-bottom: 30px; }
        input, textarea { 
            margin: 5px 0; 
            padding: 8px; 
            width: 400px; 
            box-sizing: border-box; 
            font-family: Arial, sans-serif;
        }
        textarea { 
            height: 80px; 
            resize: none;  /* Förhindrar att användaren drar rutan */
        }
        .post { background: white; border: 1px solid #ccc; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .time { color: gray; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Lukas Gästbok</h1>
    <p>Skriv ett inlägg nedan. Ditt namn, e-post, telefon, meddelande och tid sparas.</p>

    <form method="post" action="/add">
        <label for="name">Namn:</label><br>
        <input type="text" id="name" name="name" required><br>

        <label for="email">E-post:</label><br>
        <input type="email" id="email" name="email"><br>

        <label for="phone">Telefon:</label><br>
        <input type="text" id="phone" name="phone"><br>

        <label for="message">Meddelande:</label><br>
        <textarea id="message" name="message" required></textarea><br>

        <input type="submit" value="Lägg till">
    </form>

    <h2>Inlägg</h2>
    {% if posts %}
        {% for post in posts %}
            <div class="post">
                <strong>{{ post['name'] }}</strong> <span class="time">({{ post['time'] }})</span><br>
                {{ post['message'] }}<br>
                <em>E-post:</em> {{ post['email'] }}<br>
                <em>Telefon:</em> {{ post['phone'] }}
            </div>
        {% endfor %}
    {% else %}
        <p>Inga inlägg ännu.</p>
    {% endif %}
</body>
</html>
'''

def read_posts():
    posts = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    posts.append({
                        'name': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'message': parts[3],
                        'time': parts[4]
                    })
    return list(reversed(posts))

@app.route('/', methods=['GET'])
def index():
    posts = read_posts()
    return render_template_string(HTML, posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if name and message:
        with open(FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(f"{name}|{email}|{phone}|{message}|{time_now}\n")

    posts = read_posts()
    return render_template_string(HTML, posts=posts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
