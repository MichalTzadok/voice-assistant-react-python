from flask import Flask, jsonify
from speech_assistant.assistant import SpeechAssistant

from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

assistant = SpeechAssistant()

@app.route('/')
def index():
    return "שרת עוזרת קולית פועל."

@app.route('/listen', methods=['GET'])
def listen_command():
    command = assistant.listen()
    result = assistant.handle_command(command)

    # במקרה של פקודת יציאה, מחזירים הודעה אבל לא סוגרים את השרת
    if result == "exit_command":
        return jsonify({
            "status": "success",
            "command": command,
            "result": result,
            "message": "השרת ממשיך לפעול."
        })

    return jsonify({
        "status": "success",
        "command": command,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True)
