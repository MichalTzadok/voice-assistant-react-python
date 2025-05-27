import React, { useState } from "react";
import { listenToCommand } from "../api/assistantApi";
import { FaMicrophone as RawFaMicrophone, FaStop as RawFaStop } from "react-icons/fa";

// פתרון לבעיה שבה TypeScript לא מזהה את האייקונים כקומפוננטות תקינות
const FaMicrophone = RawFaMicrophone as unknown as React.FC;
const FaStop = RawFaStop as unknown as React.FC;

const HomePage: React.FC = () => {
  const [command, setCommand] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [autoListen, setAutoListen] = useState(true);

  const handleListen = async () => {
    setLoading(true);
    try {
      const data = await listenToCommand();
      const cmd = data.command || "לא זוהתה פקודה";
      const res = data.result || "אין תוצאה";
      setCommand(cmd);
      setResult(res);
      setHistory((prev) => [`🔊 ${cmd} => ${res}`, ...prev]);

      if (autoListen && res !== "סיים") {
        setTimeout(() => handleListen(), 1000);
      }
    } catch (e) {
      setCommand("");
      setResult("שגיאה בקבלת תגובה מהשרת");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 flex flex-col items-center justify-center gap-6 p-6">
      <h1 className="text-4xl font-bold text-blue-900">🎙️ העוזרת הקולית</h1>
      <div className="flex items-center gap-4">
        <button
          onClick={handleListen}
          disabled={loading}
          className="flex items-center gap-2 bg-blue-600 text-white py-2 px-4 rounded shadow-md hover:bg-blue-700 transition"
        >
          <FaMicrophone />
          {loading ? "מקשיבה..." : "התחל האזנה"}
        </button>
        <button
          onClick={() => setAutoListen(false)}
          className="flex items-center gap-2 bg-red-600 text-white py-2 px-4 rounded shadow-md hover:bg-red-700 transition"
        >
          <FaStop /> עצור
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6 max-w-lg w-full text-right">
        <p className="font-semibold text-lg">📢 פקודה שזוהתה:</p>
        <p className="text-blue-800">{command}</p>
        <p className="font-semibold text-lg mt-4">✅ תוצאה:</p>
        <p className="text-green-700">{result}</p>
      </div>

      {history.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-4 max-w-lg w-full text-right mt-6">
          <h2 className="font-semibold text-xl mb-2">🕘 היסטוריית פקודות:</h2>
          <ul className="list-disc pr-4 text-sm text-gray-700 space-y-1">
            {history.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default HomePage;
