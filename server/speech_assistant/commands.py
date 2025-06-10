import os
import subprocess
import re
import ssl
import smtplib
import requests
import webbrowser
from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def speak_and_return(text, assistant):
    assistant.speak(text)
    return text

def get_user_confirmation(assistant, question):
    assistant.speak(question)
    confirmation = assistant.listen()
    if confirmation:
        confirmation = confirmation.lower()
        return "כן" in confirmation
    return False

def send_email(subject, body, receiver, assistant):
    email = EmailMessage()
    email["From"] = EMAIL_SENDER
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(email)
        return speak_and_return("המייל נשלח בהצלחה", assistant)
    except Exception as e:
        print(e)
        return speak_and_return("שליחת המייל נכשלה", assistant)

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

def search_google(query):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select("a"):
            href = link.get("href")
            if href and "/url?q=" in href:
                url = href.split("/url?q=")[1].split("&")[0]
                if "google" not in url:
                    return url
    except Exception as e:
        print(f"Search error: {e}")
    return None

def process_command(command, assistant):
    if not command:
        return speak_and_return("לא קיבלתי פקודה. אנא נסה שוב.", assistant)

    command = command.lower()

    if "שלח מייל ל" in command and "נושא" in command and "תוכן" in command:
        try:
            to_section = command.split("שלח מייל ל")[1].split("נושא")[0].strip()
            subject_section = command.split("נושא")[1].split("תוכן")[0].strip()
            body_section = command.split("תוכן")[1].strip()

            to = extract_email(to_section)
            if not to:
                return speak_and_return("לא הצלחתי לזהות כתובת מייל תקינה", assistant)

            assistant.speak("רוצה לשלוח את המייל הבא:")
            assistant.speak(f"אל: {to}")
            assistant.speak(f"נושא: {subject_section}")
            assistant.speak(f"תוכן: {body_section}")
            if get_user_confirmation(assistant, "האם לשלוח את המייל?"):
                return send_email(subject_section, body_section, to, assistant)
            else:
                return speak_and_return("השליחה בוטלה", assistant)

        except Exception as e:
            print(e)
            return speak_and_return("הייתה בעיה בעיבוד הפקודה", assistant)

    elif "חפש בגוגל" in command:
        query = command.split("חפש בגוגל")[-1].strip()
        if not query:
            return speak_and_return("לא קיבלתי מה לחפש", assistant)
        assistant.speak(f"מחפשת בגוגל: {query}")
        url = search_google(query)
        if url:
            webbrowser.open(url)
            return speak_and_return("פתחתי את התוצאה הראשונה שמצאתי", assistant)
        else:
            return speak_and_return("לא מצאתי תוצאה", assistant)

    elif "פתח גוגל" in command:
        webbrowser.open("https://www.google.com")
        return speak_and_return("פותחת את גוגל", assistant)

    elif "פתח יוטיוב" in command:
        webbrowser.open("https://www.youtube.com")
        return speak_and_return("פותחת את יוטיוב", assistant)

    elif "מה השעה" in command:
        now = datetime.now().strftime("%H:%M")
        return speak_and_return(f"השעה עכשיו {now}", assistant)

    elif "פתח תיקייה" in command:
        folder_name = command.split("פתח תיקייה")[-1].strip()
        path = os.path.expanduser(f"~/{folder_name}")
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')
            return speak_and_return(f"פותחת את התיקייה {folder_name}", assistant)
        else:
            return speak_and_return("לא מצאתי את התיקייה", assistant)

    elif "פתח קובץ" in command:
        file_name = command.split("פתח קובץ")[-1].strip()
        path = os.path.expanduser(f"~/{file_name}")
        if os.path.exists(path):
            os.startfile(path)
            return speak_and_return(f"פותחת את הקובץ {file_name}", assistant)
        else:
            return speak_and_return("לא מצאתי את הקובץ", assistant)

    elif "צאי מהתוכנית" in command:
        speak_and_return("להתראות", assistant)
        os._exit(0)

    else:
        return speak_and_return("לא הבנתי את הפקודה", assistant)
