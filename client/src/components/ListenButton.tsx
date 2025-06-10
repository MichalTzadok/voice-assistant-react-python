import React from "react";

interface Props {
  onClick: () => void;
  loading: boolean;
}

const ListenButton: React.FC<Props> = ({ onClick, loading }) => {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
    >
      {loading ? "מקשיב..." : "האזן לפקודה"}
    </button>
  );
};

export default ListenButton;