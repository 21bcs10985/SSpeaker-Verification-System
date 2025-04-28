from flask import Flask, render_template, request, jsonify
from main import sign_up, login
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/login/page1')
def login_page1():
    return render_template('login/page1.html')

@app.route('/login/page2')
def login_page2():
    return render_template('login/page2.html')

@app.route('/login/page3')
def login_page7():
    return render_template('login/page3.html')

@app.route('/register/page1')
def register_page1():
    return render_template('register/page1.html')

@app.route('/register/page2')
def register_page2():
    return render_template('register/page2.html')

@app.route('/register/page3')
def register_page3():
    return render_template('register/page3.html')

@app.route('/register/page4')
def register_page4():
    return render_template('register/page4.html')

@app.route('/register/page5')
def register_page5():
    return render_template('register/page5.html')

@app.route('/register/page6')
def register_page6():
    return render_template('register/page6.html')

@app.route('/register/page7')
def register_page7():
    return render_template('register/page7.html')


from flask import request, jsonify
import os
from pydub import AudioSegment

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    count = int(request.form['count'])
    audio = request.files['audio_data']

    user_dir = os.path.join("Data", username)
    os.makedirs(user_dir, exist_ok=True)

    # Save the original file as-is
    audio_path = os.path.join(user_dir, f"sample_{count}.webm")
    audio.save(audio_path)
    print(f"✅ Saved uploaded file at {audio_path}")

    # Check if 5 recordings exist
    if len([f for f in os.listdir(user_dir) if f.endswith('.webm')]) == 5:
        try:
            sign_up(username)
            return jsonify({"message": f"✅ All recordings uploaded and user '{username}' registered."})
        except Exception as e:
            return jsonify({"message": f"❌ Error during training: {str(e)}"})
    else:
        return jsonify({"message": f"✅ Recording {count}/5 saved for '{username}'."})


@app.route('/check-user', methods=['POST'])
def check_user():
    username = request.form['username']
    model_path = os.path.join("voiceauth", "model", f"{username}.gmm")
    exists = os.path.exists(model_path)
    return jsonify({'exists': exists})

# import traceback

import io
import sys
from flask import Response, stream_with_context

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    count = int(request.form['count'])
    audio = request.files['audio_data']

    user_dir = os.path.join("recordings", username)
    os.makedirs(user_dir, exist_ok=True)

    save_path = os.path.join(user_dir, f"{username}_recording.wav")
    audio.save(save_path)

    def generate_logs():
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # Redirect stdout
        try:
            login(username)                      # Call your login function
            sys.stdout = sys.__stdout__           # Reset redirect
            logs = captured_output.getvalue()
            yield logs
            yield "\n--- Process Completed Successfully ---"
        except Exception as e:
            sys.stdout = sys.__stdout__
            logs = captured_output.getvalue()
            yield logs
            yield f"\n--- Error Occurred: {str(e)} ---"

    return Response(stream_with_context(generate_logs()), mimetype='text/plain')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['audio']
    username = request.form['username']
    mode = request.form['mode']

    audio_path = os.path.join("uploads", f"{username}.wav")
    os.makedirs("uploads", exist_ok=True)
    file.save(audio_path)

    try:
        if mode == 'register':
            sign_up(username)
        else:
            login(username)
        return jsonify({'message': f"{mode.capitalize()} process completed for {username}."})
    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
