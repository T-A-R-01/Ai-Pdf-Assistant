import { useState, useEffect, useRef } from "react";

import Sidebar from "./components/Sidebar";
import UploadSection from "./components/UploadSection";
import ChatInput from "./components/ChatInput";
import ChatMessage from "./components/ChatMessage";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const [pdfs, setPdfs] = useState([]);

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "Upload a PDF and start asking questions.",
    },
  ]);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handlePdfUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/upload-pdf",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setPdfs((prev) => [
        ...prev,
        selectedFile.name,
      ]);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            data.message ||
            `${selectedFile.name} uploaded successfully.`,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Failed to upload PDF.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (question) => {
    if (!question.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: question,
      },
    ]);

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            data.answer ||
            "No answer returned.",
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            "Error connecting to backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar pdfs={pdfs} />

      <div className="main-content">
        <div className="hero-section">
          <h1>PDF Research Assistant</h1>

          <p>
            Upload PDFs and ask questions
            using Retrieval-Augmented
            Generation (RAG)
          </p>
        </div>

        <UploadSection
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
        />

        <button
          className="add-pdf-btn"
          onClick={handlePdfUpload}
        >
          Upload Document
        </button>

        <div className="chat-container">
          {messages.map((msg, index) => (
            <ChatMessage
              key={index}
              role={msg.role}
              message={msg.text}
            />
          ))}

          {loading && (
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}

          <div ref={chatEndRef}></div>
        </div>

        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}