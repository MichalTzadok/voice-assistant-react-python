import os
import re
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

from speech_assistant.commands import register_command
from speech_assistant.exceptions import EmailError

load_dotenv()
logger = logging.getLogger(__name__)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def _get_user_confirmation(assistant, question: str) -> bool:
    """מבקש אישור מהמשתמש."""
    assistant.speak(question)
    try:
        confirmation = assistant.listen()
        if confirmation:
            return "כן" in confirmation.lower()
    except Exception as e:
        logger.warning(f"שגיאה בקבלת אישור מהמשתמש: {e}")
    return False

def _extract_email(text: str) -> str | None:
    """מחפש כתובת מייל בטקסט."""
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

@register_command("שלח מייל ל")
def send_email_command(command: str, assistant) -> str:
    """שולח מייל."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        assistant.speak("פרטי השולח אינם מוגדרים. לא ניתן לשלוח מייל.")
        logger.error("EMAIL_SENDER או EMAIL_PASSWORD אינם מוגדרים בקובץ .env")
        return "פרטי שולח המייל אינם מוגדרים."

    try:
        if "נושא" not in command or "תוכן" not in command:
            assistant.speak("אנא ציין נושא ותוכן למייל.")
            return "פקודה לא מלאה לשליחת מייל."

        # פיצול הפקודה בצורה חכמה יותר
        to_section = command.split("שלח מייל ל")[1].split("נושא")[0].strip()
        subject_section = command.split("נושא")[1].split("תוכן")[0].strip()
        body_section = command.split("תוכן")[1].strip()

        to_email = _extract_email(to_section)
        if not to_email:
            assistant.speak("לא הצלחתי לזהות כתובת מייל תקינה.")
            return "כתובת מייל לא תקינה."

        assistant.speak("רוצה לשלוח את המייל הבא:")
        assistant.speak(f"אל: {to_email}")
        assistant.speak(f"נושא: {subject_section}")
        assistant.speak(f"תוכן: {body_section}")

        if _get_user_confirmation(assistant, "האם לשלוח את המייל?"):
            email = EmailMessage()
            email["From"] = EMAIL_SENDER
            email["To"] = to_email
            email["Subject"] = subject_section
            email.set_content(body_section)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(email)
            assistant.speak("המייל נשלח בהצלחה.")
            logger.info(f"מייל נשלח בהצלחה ל-{to_email} עם נושא: {subject_section}")
            return "המייל נשלח בהצלחה."
        else:
            assistant.speak("שליחת המייל בוטלה.")
            logger.info("שליחת מייל בוטלה על ידי המשתמש.")
            return "השליחה בוטלה."

    except Exception as e:
        logger.error(f"שגיאה בשליחת מייל: {e}", exc_info=True)
        assistant.speak("אירעה שגיאה בשליחת המייל.")
        raise EmailError(f"אירעה שגיאה בשליחת המייל: {e}")