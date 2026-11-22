
import { useState } from "react";
import "./AIChat.css";

function AIChat({ userId, onBack }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ai-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          recommendations: data.recommendations || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Unable to connect to ScholarAI. Please try again.",
          recommendations: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-chat-container">
      <header className="ai-chat-header">
        <button onClick={onBack}>← Back</button>
        <h2>🤖 ScholarAI Assistant</h2>
        <p>Your AI scholarship guide</p>
      </header>

      <div className="ai-chat-messages">
        {messages.length === 0 && (
          <p>Hello! I'm ScholarAI. How can I help you today?</p>
        )}

        {messages.map((msg, index) => (
          <div className={`chat-message ${msg.role}`} key={index}>
            <strong>
              {msg.role === "user" ? "You" : "ScholarAI"}
            </strong>

            <p>{msg.content}</p>

            {msg.role === "assistant" &&
              msg.recommendations?.length > 0 && (
                <div className="recommendation-list">
                  {msg.recommendations.map((scheme, schemeIndex) => (
                    <div className="recommendation-card" key={schemeIndex}>
                      <h3>{scheme.scheme_name}</h3>

                      <span className="eligibility-status">
                        {scheme.status.replaceAll("_", " ")}
                      </span>

                      <p>
                        <strong>Benefits:</strong> {scheme.benefits}
                      </p>

                      <p>
                        <strong>Eligibility checks:</strong>{" "}
                        {Object.entries(scheme.checks || {})
                          .map(([key, value]) => `${key}: ${value}`)
                          .join(", ")}
                      </p>

                      {scheme.official_source_url && (
                        <a
                          href={scheme.official_source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Visit Official Source →
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
          </div>
        ))}

        {loading && <p>ScholarAI is thinking...</p>}
      </div>

      <div className="ai-chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about scholarships..."
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default AIChat;
