import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (!question.trim()) return;

    onSend(question);
    setQuestion("");
  };

  return (
    <div className="chat-input-container">
      <input
        className="chat-input"
        type="text"
        placeholder="Ask anything about your PDF..."
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
      />

      <button
        className="send-btn"
        onClick={handleSend}
      >
        Send
      </button>
    </div>
  );
}