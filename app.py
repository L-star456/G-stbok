from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

FILE_PATH = 'Gästbok.txt'

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
    return render_template('index.html', posts=posts)

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
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
