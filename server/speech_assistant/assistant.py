import speech_recognition as sr
import pyttsx3
import threading
import queue
import logging
from config import LANGUAGE
from speech_assistant.exceptions import SpeechRecognitionError, TimeoutError, UnknownValueError, RequestError

# הגדרת לוגינג
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpeechAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9) # הגדרת ווליום ברירת מחדל

        self._speak_queue = queue.Queue()
        self._running = True # דגל לשליטה על לולאת הדיבור
        self._speak_thread = threading.Thread(target=self._speak_loop, daemon=True)
        self._speak_thread.start()

    def _speak_loop(self):
        """לולאה ייעודית לטיפול בפלט קולי למניעת חסימה."""
        while self._running:
            text = self._speak_queue.get()
            if text is None: # סימן לסיום
                self._speak_queue.task_done()
                break
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"שגיאה בהפעלת דיבור: {e}")
            finally:
                self._speak_queue.task_done()
        logger.info("לולאת הדיבור נסגרה.")

    def speak(self, text: str):
        """מוסיף טקסט לתור הדיבור."""
        if not text:
            return
        logger.info(f"מדברת: {text}")
        self._speak_queue.put(text)
        self._speak_queue.join() # ממתין שהדיבור יסתיים לפני שממשיך (אופציונלי, תלוי UX)

    def listen(self) -> str | None:
        """מאזין לקלט קולי ומחזיר את הטקסט או זורק שגיאה."""
        with sr.Microphone() as source:
            logger.info("ממתינה להוראה...")
            self.recognizer.adjust_for_ambient_noise(source) # התאמה לרעשי סביבה
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
            except sr.WaitTimeoutError:
                logger.warning("לא התקבל קול בזמן.")
                raise TimeoutError("לא התקבל קול בזמן.")
            except Exception as e:
                logger.error(f"שגיאה כללית בזמן האזנה: {e}")
                raise SpeechRecognitionError(f"שגיאה כללית בזמן האזנה: {e}")

        try:
            command = self.recognizer.recognize_google(audio, language=LANGUAGE)
            logger.info(f"זיהוי: {command}")
            return command.lower()
        except sr.UnknownValueError:
            logger.warning("לא הצלחתי להבין את הדיבור.")
            raise UnknownValueError("לא הצלחתי להבין את הדיבור.")
        except sr.RequestError as e:
            logger.error(f"שגיאת בקשה מ-Google Speech Recognition API: {e}")
            raise RequestError(f"שגיאת בקשה מ-Google Speech Recognition API: {e}")
        except Exception as e:
            logger.error(f"שגיאה כללית בזיהוי דיבור: {e}")
            raise SpeechRecognitionError(f"שגיאה כללית בזיהוי דיבור: {e}")

    def process_command(self, command: str) -> str:
        """מפעיל את הפקודה באמצעות מנגנון הרישום."""
        from speech_assistant.commands import registered_commands # ייבוא בתוך הפונקציה למניעת ייבוא ציקלי
        for cmd_name, cmd_func in registered_commands.items():
            if cmd_name in command:
                try:
                    return cmd_func(command, self)
                except Exception as e:
                    logger.error(f"שגיאה בהפעלת פקודה '{cmd_name}': {e}")
                    raise
        # אם לא נמצאה פקודה מתאימה
        self.speak("לא הבנתי את הפקודה.")
        return "לא הבנתי את הפקודה."

    def stop(self):
        """מנקה משאבים ומפסיק את לולאת הדיבור."""
        logger.info("מכבה את העוזרת הקולית...")
        self._running = False
        self._speak_queue.put(None) # שחרור ה-queue.get()
        self._speak_thread.join(timeout=2) # ממתין שהתהליך יסיים (עם טיימאאוט)
        if self._speak_thread.is_alive():
            logger.warning("תהליך הדיבור לא הסתיים בזמן.")
        try:
            self.engine.stop() # עצירת מנוע הדיבור
        except Exception as e:
            logger.error(f"שגיאה בעצירת מנוע pyttsx3: {e}")
        logger.info("העוזרת הקולית כובתה בהצלחה.")