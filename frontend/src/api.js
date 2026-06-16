const API_BASE = "http://127.0.0.1:8000";

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload-pdf`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload PDF");
  }

  return response.json();
}

export async function askQuestion(question) {
  const response = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get answer");
  }

  return response.json();
}