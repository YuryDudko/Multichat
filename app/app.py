from flask import Flask, render_template, request, redirect, url_for,jsonify,make_response
from datetime import datetime
import time

app = Flask(__name__)
users = set()  # Хранение имен пользователей в оперативной памяти (множество)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')

    if username:
        if username not in users:
            users.add(username)
            resp = (redirect('/page2'))
            resp.set_cookie('userID',username)
            return resp
        else:
            return "Пользователь с таким именем уже существует."
    else:
        return "Заполните имя пользователя."

@app.route('/page2')
def page2():
    return render_template('page2.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = request.cookies.get('userID')
    #username = data.get('username')
    message = data.get('message')
    time_val = data.get('time')

    if username and message:
        new_message = {'username': username, 'message': message , 'time': time_val}
        messages.append(new_message)
        return jsonify({'success': True, 'message': new_message})
    else:
        return jsonify({'success': False, 'error': 'Invalid data'})

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
