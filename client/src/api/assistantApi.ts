const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

export const listenToCommand = async () => {
  const response = await fetch(`${API_BASE_URL}/listen`);
  if (!response.ok) {
    // זורק שגיאה אם הסטטוס אינו OK (למשל, 404, 500)
    const errorData = await response.json();
    throw new Error(errorData.message || "שגיאה בשרת.");
  }
  const data = await response.json();
  return data;
};

export const shutdownServer = async () => {
  const response = await fetch(`${API_BASE_URL}/shutdown`, {
    method: "POST",
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "שגיאה בכיבוי השרת.");
  }
  const data = await response.json();
  return data;
};