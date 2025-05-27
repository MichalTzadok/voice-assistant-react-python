import os
from config import SEARCH_FOLDERS

def open_folder_or_file(command, assistant):
    folders = {
        "שולחן העבודה": os.path.expanduser("~/Desktop"),
        "המסמכים": os.path.expanduser("~/Documents"),
        "ההורדות": os.path.expanduser("~/Downloads"),
        "התמונות": os.path.expanduser("~/Pictures"),
        "המוזיקה": os.path.expanduser("~/Music")
    }

    for name, path in folders.items():
        if name in command:
            assistant.speak(f"פותחת את {name}")
            os.startfile(path)
            return "folder_opened"

    file_name = command.replace("פתח", "").replace("את", "").strip()
    for base_path in SEARCH_FOLDERS:
        expanded = os.path.expanduser(base_path)
        for root, _, files in os.walk(expanded):
            for file in files:
                if file_name in file:
                    assistant.speak(f"פותחת את הקובץ {file}")
                    os.startfile(os.path.join(root, file))
                    return "file_opened"

    assistant.speak("לא הצלחתי למצוא את הקובץ או התיקיה")
    return "not_found"
