import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from speech_assistant.assistant import SpeechAssistant
from speech_assistant.exceptions import AssistantError, SpeechRecognitionError, TimeoutError, UnknownValueError, RequestError
from config import LOG_LEVEL, LOG_FILE # ייבוא הגדרות לוגינג

# הגדרת לוגינג בסיסית עבור כל האפליקציה
logging.basicConfig(level=getattr(logging, LOG_LEVEL),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

assistant = SpeechAssistant()

@app.route('/')
def index():
    logger.info("גישה לדף הבית של השרת.")
    return "שרת עוזרת קולית פועל."

@app.route('/listen', methods=['GET'])
def listen_and_process_command():
    command = None
    result = "לא נכנס לפעולה."
    status = "error"
    message = "שגיאה לא ידועה."

    try:
        command = assistant.listen()
        if command is None:
            message = "לא זוהה דיבור ברור."
            result = "לא זוהה דיבור ברור."
            status = "fail"
        else:
            result = assistant.process_command(command)
            status = "success"
            message = "הפקודה טופלה בהצלחה."
            if result == "exit_command":
                message = "השרת ממשיך לפעול, העוזרת סיימה פעולה."

    except TimeoutError:
        message = "לא התקבל קול בזמן."
        result = "timeout_error"
        status = "timeout"
        logger.warning(message)
    except UnknownValueError:
        message = "לא הצלחתי להבין את הדיבור."
        result = "unknown_value_error"
        status = "unknown_speech"
        logger.warning(message)
    except RequestError as e:
        message = f"שגיאה בבקשה ל-Google Speech Recognition API: {e}"
        result = "request_error"
        status = "api_error"
        logger.error(message)
    except AssistantError as e:
        message = f"שגיאת עוזרת קולית: {e}"
        result = "assistant_error"
        status = "assistant_fail"
        logger.error(message, exc_info=True)
    except Exception as e:
        message = f"שגיאה בלתי צפויה: {e}"
        result = "unexpected_error"
        status = "unexpected_fail"
        logger.critical(message, exc_info=True)

    response_data = {
        "status": status,
        "command": command,
        "result": result,
        "message": message
    }
    logger.info(f"תגובה ללקוח: {response_data}")
    return jsonify(response_data)

@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    logger.info("בקשת כיבוי שרת התקבלה.")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        logger.error("לא פועל עם Werkzeug Server, לא ניתן לכבות.")
        return jsonify({"status": "error", "message": "לא ניתן לכבות את השרת בדרך זו."}), 500
    try:
        assistant.stop() # עצירת העוזרת לפני כיבוי השרת
        func()
        logger.info("השרת כובה בהצלחה.")
        return jsonify({"status": "success", "message": "השרת כובה בהצלחה."})
    except Exception as e:
        logger.critical(f"שגיאה במהלך כיבוי השרת: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"שגיאה במהלך כיבוי השרת: {e}"}), 500


if __name__ == '__main__':
    logger.info("מפעיל את שרת Flask...")
    # שימוש ב-threaded=True מאפשר לטפל בבקשות במקביל
    app.run(debug=True, threaded=True)