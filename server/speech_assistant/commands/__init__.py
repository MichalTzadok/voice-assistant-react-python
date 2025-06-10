import logging

logger = logging.getLogger(__name__)

# רשימה של פקודות רשומות. המפתח הוא ביטוי מפתח, והערך הוא פונקציית הטיפול.
# הפקודות ייטענו מתוך המודולים השונים.
registered_commands = {}


def register_command(keywords):
    """דקורטור לרישום פקודות."""

    def decorator(func):
        if isinstance(keywords, str):
            actual_keywords = [keywords]
        else:
            actual_keywords = keywords

        for keyword in actual_keywords:
            if keyword in registered_commands:
                logger.warning(f"הפקודה '{keyword}' כבר רשומה ותידרס.")
            registered_commands[keyword] = func
            logger.debug(f"נרשמה פקודה: '{keyword}' -> {func.__name__}")
        return func

    return decorator


# ייבוא כל קובצי הפקודות כדי לרשום אותן
import speech_assistant.commands.email_commands
import speech_assistant.commands.general_commands
import speech_assistant.commands.system_commands