import React, { useState, useEffect, useRef } from "react";
import { listenToCommand, shutdownServer } from "../api/assistantApi";
import { FaMicrophone as RawFaMicrophone, FaStop as RawFaStop, FaPowerOff as RawFaPowerOff } from "react-icons/fa";

interface IconProps extends React.SVGProps<SVGSVGElement> {}

const FaMicrophone: React.FC<IconProps> = RawFaMicrophone as unknown as React.FC<IconProps>;
const FaStop: React.FC<IconProps> = RawFaStop as unknown as React.FC<IconProps>;
const FaPowerOff: React.FC<IconProps> = RawFaPowerOff as unknown as React.FC<IconProps>;


const HomePage: React.FC = () => {
    const [command, setCommand] = useState<string>("");
    const [result, setResult] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [history, setHistory] = useState<string[]>([]);
    const [autoListen, setAutoListen] = useState<boolean>(false);
    const autoListenTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    const handleListen = async () => {
        if (loading) return;

        setLoading(true);
        setCommand("מקשיבה...");
        setResult("");

        try {
            const data = await listenToCommand();
            const cmd = data.command || "לא זוהתה פקודה";
            const res = data.message || data.result || "אין תוצאה";

            setCommand(cmd);
            setResult(res);
            setHistory((prev) => [`🔊 ${cmd} => ${res}`, ...prev]);

            if (autoListen && data.result !== "exit_command") {
                autoListenTimeoutRef.current = setTimeout(() => handleListen(), 1000);
            }
        } catch (e: any) {
            setCommand("");
            setResult(`שגיאה: ${e.message || "בקבלת תגובה מהשרת"}`);
            setHistory((prev) => [`❌ שגיאה: ${e.message || "בקבלת תגובה מהשרת"}`, ...prev]);
            console.error("שגיאה בקריאה לשרת:", e);
            setAutoListen(false);
        } finally {
            setLoading(false);
        }
    };

    const handleShutdown = async () => {
        if (!window.confirm("האם אתה בטוח שברצונך לכבות את שרת הפייתון?")) {
            return;
        }
        setLoading(true);
        try {
            const data = await shutdownServer();
            setResult(data.message);
            setHistory((prev) => [`🔴 ${data.message}`, ...prev]);
        } catch (e: any) {
            setResult(`שגיאה בכיבוי שרת: ${e.message}`);
            setHistory((prev) => [`❌ שגיאה בכיבוי שרת: ${e.message}`, ...prev]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        return () => {
            if (autoListenTimeoutRef.current) {
                clearTimeout(autoListenTimeoutRef.current);
            }
        };
    }, [autoListen]);

    return (
        <div className="min-h-screen flex flex-col items-center justify-center gap-10 p-8 relative overflow-hidden">
            {/* אפקטים ויזואליים - נקודות / רשת עתידנית */}
            <div className="absolute inset-0 z-0 opacity-10">
                <div className="absolute inset-0 bg-[size:50px_50px] [background-image:radial-gradient(ellipse_at_center,_rgba(255,255,255,0.1)_0%,_transparent_50%)]"></div>
            </div>

            <h1 className="text-6xl font-bold text-white text-center leading-tight z-10 drop-shadow-lg">
                <span className="text-yellow-400">🎙️</span>  העוזרת הקולית שלך<br className="sm:hidden"/> 
            </h1>

            <div className="flex flex-wrap justify-center items-center gap-6 z-10">
                <button
                    onClick={() => { setAutoListen(true); handleListen(); }}
                    disabled={loading && autoListen}
                    className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold text-lg rounded-full shadow-2xl
                               hover:from-purple-700 hover:to-blue-700 transition duration-300 ease-in-out transform hover:scale-105
                               disabled:opacity-50 disabled:cursor-not-allowed border border-blue-400"
                >
                    <FaMicrophone className="text-2xl" />
                    {loading && autoListen ? "מקשיבה אוטומטית..." : "התחל האזנה"}
                </button>

                <button
                    onClick={() => { setAutoListen(false); if (autoListenTimeoutRef.current) clearTimeout(autoListenTimeoutRef.current); setLoading(false); }}
                    disabled={!autoListen && !loading}
                    className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-pink-600 to-red-600 text-white font-bold text-lg rounded-full shadow-2xl
                               hover:from-pink-700 hover:to-red-700 transition duration-300 ease-in-out transform hover:scale-105
                               disabled:opacity-50 disabled:cursor-not-allowed border border-red-400"
                >
                    <FaStop className="text-2xl" /> עצור האזנה
                </button>

                <button
                    onClick={handleShutdown}
                    disabled={loading}
                    className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-gray-700 to-gray-900 text-white font-bold text-lg rounded-full shadow-2xl
                               hover:from-gray-600 hover:to-gray-800 transition duration-300 ease-in-out transform hover:scale-105
                               disabled:opacity-50 disabled:cursor-not-allowed border border-gray-500"
                    title="כבה את שרת הפייתון"
                >
                    <FaPowerOff className="text-2xl" /> כבה שרת
                </button>
            </div>

            <div className="glass-card p-10 max-w-2xl w-full text-right z-10 border border-purple-500/50">
                <p className="font-bold text-2xl text-yellow-300 mb-4">📢 פקודה שזוהתה:</p>
                <p className="text-blue-300 text-xl break-words min-h-[1.5em]">{command || "ממתינה לפקודה..."}</p>

                <p className="font-bold text-2xl text-yellow-300 mt-8 mb-4">✅ תוצאה:</p>
                <p className="text-green-400 text-xl break-words min-h-[1.5em]">{result || "הפקודה תבוצע ותוצאה תופיע כאן..."}</p>
            </div>

            {history.length > 0 && (
                <div className="glass-card p-8 max-w-2xl w-full text-right z-10 border border-pink-500/50">
                    <h2 className="font-bold text-2xl text-yellow-300 mb-6">🕘 היסטוריית פקודות:</h2>
                    <ul className="list-disc pr-8 text-lg text-gray-200 space-y-3 max-h-72 overflow-y-auto custom-scrollbar">
                        {history.map((item, index) => (
                            <li key={index} className="leading-relaxed">{item}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default HomePage;