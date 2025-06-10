class AssistantError(Exception):
    """בסיס עבור חריגות הקשורות לעוזרת הקולית."""
    pass

class SpeechRecognitionError(AssistantError):
    """שגיאה בזיהוי דיבור."""
    pass

class CommandProcessingError(AssistantError):
    """שגיאה בעיבוד פקודה."""
    pass

class EmailError(CommandProcessingError):
    """שגיאה בשליחת מייל."""
    pass

class FileSystemError(CommandProcessingError):
    """שגיאה בפעולות קובץ/תיקייה."""
    pass

class GoogleSearchError(CommandProcessingError):
    """שגיאה בחיפוש בגוגל."""
    pass

class TimeoutError(SpeechRecognitionError):
    """שגיאת קלט קולי שפג תוקפו."""
    pass

class UnknownValueError(SpeechRecognitionError):
    """שגיאה כאשר הדיבור לא מובן."""
    pass

class RequestError(SpeechRecognitionError):
    """שגיאה בבקשה מ-Google Speech Recognition API."""
    pass