import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from speech_assistant.commands import register_command
from speech_assistant.exceptions import GoogleSearchError

logger = logging.getLogger(__name__)

@register_command("חפש בגוגל")
def search_google_command(command: str, assistant) -> str:
    """מבצע חיפוש בגוגל ופותח את דף תוצאות החיפוש."""
    query = command.replace("חפש בגוגל", "").strip()
    if not query:
        assistant.speak("לא קיבלתי מה לחפש בגוגל.")
        return "לא קיבלתי שאילתה."

    assistant.speak(f"מחפשת בגוגל: {query}")
    try:
        # יצירת ה-URL לחיפוש גוגל ישירות
        Google_Search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(Google_Search_url)
        assistant.speak("פתחתי את תוצאות החיפוש בגוגל.")
        logger.info(f"נפתח חיפוש גוגל עבור: {query}")
        return "נפתח חיפוש בגוגל."
    except Exception as e:
        logger.error(f"שגיאה בפתיחת חיפוש גוגל: {e}")
        assistant.speak(f"אירעה שגיאה בפתיחת חיפוש גוגל: {e}")
        return f"שגיאה בפתיחת חיפוש: {e}"

@register_command("פתח גוגל")
def open_google_command(command: str, assistant) -> str:
    """פותח את דף הבית של גוגל."""
    webbrowser.open("https://www.google.com")
    assistant.speak("פותחת את גוגל.")
    logger.info("נפתח Google.")
    return "נפתח Google."

@register_command("פתח יוטיוב")
def open_youtube_command(command: str, assistant) -> str:
    """פותח את יוטיוב."""
    webbrowser.open("https://www.youtube.com")
    assistant.speak("פותחת את יוטיוב.")
    logger.info("נפתח YouTube.")
    return "נפתח YouTube."

@register_command("מה השעה")
def get_time_command(command: str, assistant) -> str:
    """מחזיר את השעה הנוכחית."""
    now = datetime.now().strftime("%H:%M")
    assistant.speak(f"השעה עכשיו {now}.")
    logger.info(f"השעה נמסרה: {now}")
    return f"השעה: {now}."