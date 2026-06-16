export default function ChatMessage({
  message,
  role,
}) {
  return (
    <div
      className={`message-row ${
        role === "user"
          ? "message-user"
          : "message-ai"
      }`}
    >
      <div className="message-bubble">
        {message}
      </div>
    </div>
  );
}