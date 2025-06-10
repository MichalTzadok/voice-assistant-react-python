import os
import subprocess
import logging
from config import SEARCH_FOLDERS  # ייבוא מ-config

from speech_assistant.commands import register_command
from speech_assistant.exceptions import FileSystemError

logger = logging.getLogger(__name__)


@register_command("פתח תיקייה")
def open_folder_command(command: str, assistant) -> str:
    """פותח תיקייה במערכת הקבצים."""
    folder_name = command.replace("פתח תיקייה", "").strip()
    if not folder_name:
        assistant.speak("לא קיבלתי שם תיקייה לפתוח.")
        return "לא הוזן שם תיקייה."

    # מפות לתיקיות נפוצות
    common_folders = {
        "שולחן העבודה": os.path.expanduser("~/Desktop"),
        "המסמכים": os.path.expanduser("~/Documents"),
        "ההורדות": os.path.expanduser("~/Downloads"),
        "התמונות": os.path.expanduser("~/Pictures"),
        "המוזיקה": os.path.expanduser("~/Music"),
        "סרטונים": os.path.expanduser("~/Videos"),
    }

    path_to_open = None

    # נסה להתאים לתיקיות נפוצות
    for key, path in common_folders.items():
        if key in folder_name:
            path_to_open = path
            break

    # אם לא תואם תיקייה נפוצה, נסה נתיב ישיר או בתוך תיקיות החיפוש
    if not path_to_open:
        # בדיקה לנתיב מלא או יחסי
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            path_to_open = folder_name
        else:
            # חפש בתיקיות המוגדרות ב-SEARCH_FOLDERS
            for base_path in SEARCH_FOLDERS:
                full_path_candidate = os.path.join(base_path, folder_name)
                if os.path.exists(full_path_candidate) and os.path.isdir(full_path_candidate):
                    path_to_open = full_path_candidate
                    break

    if path_to_open:
        try:
            # פתיחת תיקייה תלויה במערכת ההפעלה
            if os.name == 'nt':  # Windows
                subprocess.Popen(f'explorer "{path_to_open}"')
            elif os.name == 'posix':  # macOS, Linux
                subprocess.Popen(['open', path_to_open])  # macOS
                # או subprocess.Popen(['xdg-open', path_to_open]) # Linux
            assistant.speak(f"פותחת את התיקייה {os.path.basename(path_to_open)}.")
            logger.info(f"נפתחה תיקייה: {path_to_open}")
            return "תיקייה נפתחה."
        except Exception as e:
            logger.error(f"שגיאה בפתיחת תיקייה {path_to_open}: {e}")
            assistant.speak(f"אירעה שגיאה בפתיחת התיקייה {folder_name}.")
            raise FileSystemError(f"שגיאה בפתיחת תיקייה: {e}")
    else:
        assistant.speak("לא מצאתי את התיקייה.")
        logger.warning(f"לא נמצאה תיקייה: {folder_name}")
        return "תיקייה לא נמצאה."


@register_command("פתח קובץ")
def open_file_command(command: str, assistant) -> str:
    """פותח קובץ במערכת הקבצים."""
    file_name = command.replace("פתח קובץ", "").strip()
    if not file_name:
        assistant.speak("לא קיבלתי שם קובץ לפתוח.")
        return "לא הוזן שם קובץ."

    path_to_open = None

    # חפש את הקובץ בתיקיות המוגדרות ב-SEARCH_FOLDERS
    for base_path in SEARCH_FOLDERS:
        expanded_base_path = os.path.expanduser(base_path)
        for root, _, files in os.walk(expanded_base_path):
            for file in files:
                if file_name.lower() in file.lower():  # חיפוש לא תלוי רישיות
                    path_to_open = os.path.join(root, file)
                    break
            if path_to_open:
                break
        if path_to_open:
            break

    if path_to_open and os.path.exists(path_to_open) and os.path.isfile(path_to_open):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path_to_open)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.Popen(['open', path_to_open])  # macOS
                # או subprocess.Popen(['xdg-open', path_to_open]) # Linux
            assistant.speak(f"פותחת את הקובץ {os.path.basename(path_to_open)}.")
            logger.info(f"נפתח קובץ: {path_to_open}")
            return "קובץ נפתח."
        except Exception as e:
            logger.error(f"שגיאה בפתיחת קובץ {path_to_open}: {e}")
            assistant.speak(f"אירעה שגיאה בפתיחת הקובץ {file_name}.")
            raise FileSystemError(f"שגיאה בפתיחת קובץ: {e}")
    else:
        assistant.speak("לא מצאתי את הקובץ.")
        logger.warning(f"לא נמצא קובץ: {file_name}")
        return "קובץ לא נמצא."


@register_command("צא מהתוכנית")
def exit_command(command: str, assistant) -> str:
    """מבקש מהשרת לצאת."""
    assistant.speak("להתראות.")
    logger.info("פקודת יציאה התקבלה.")
    # השרת לא נסגר אוטומטית כאן, אלא רק ה-assistant.
    # אם תרצי לכבות את השרת, תצטרכי לשלוח בקשה ל-endpoint ייעודי ב-Flask.
    return "exit_command"