import speech_recognition as sr
import pyttsx3
import threading
import queue
from config import LANGUAGE
from .commands import process_command  # הסר את הנקודה אם אתה לא בתוך חבילה

class SpeechAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        self.speak_queue = queue.Queue()
        self.speak_thread = threading.Thread(target=self._speak_loop, daemon=True)
        self.speak_thread.start()

    def _speak_loop(self):
        while True:
            text = self.speak_queue.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.runAndWait()
            self.speak_queue.task_done()

    def speak(self, text):
        """ מוסיף טקסט לתור הדיבור """
        self.speak_queue.put(text)

    def listen(self):
        """ מאזין לקלט קולי ומחזיר את הטקסט או שגיאה """
        with sr.Microphone() as source:
            print("ממתינה להוראה...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
            except sr.WaitTimeoutError:
                print("לא התקבל קול בזמן.")
                return "timeout_error"

        try:
            command = self.recognizer.recognize_google(audio, language=LANGUAGE)
            print("זיהוי:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("לא הצלחתי להבין את הדיבור.")
            return None
        except sr.RequestError:
            print("שגיאת בקשה מ-Google.")
            return "request_error"

    def handle_command(self, command):
        """ מעביר פקודה לעיבוד מלא """
        return process_command(command, self)
