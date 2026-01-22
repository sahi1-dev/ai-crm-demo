import { useState } from "react";
import "./index.css";

function App() {
  const [interaction, setInteraction] = useState("");
  const [aiResponse, setAiResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!interaction) return alert("Please enter interaction");
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/log-interaction", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: interaction }),
    });

    const data = await res.json();
    setAiResponse(data);
    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="main-card">
        
        {/* LEFT FORM */}
        <div className="form-section">
          <h2>Log HCP Interaction</h2>
          <p className="subtitle">Enter interaction details for AI processing</p>

          <textarea
            placeholder="E.g. Met Dr. Sharma, discussed Product X and follow-up planned"
            value={interaction}
            onChange={(e) => setInteraction(e.target.value)}
          />

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Processing..." : "Submit Interaction"}
          </button>
        </div>

        {/* RIGHT AI PANEL */}
        <div className="ai-section">
          <h3>AI Assistant</h3>

          {aiResponse ? (
            <div className="ai-card fade-in">
              <p><b>Doctor:</b> {aiResponse.doctor}</p>
              <p><b>Topic:</b> {aiResponse.topic}</p>
              <p><b>Sentiment:</b> {aiResponse.sentiment}</p>
              <p><b>Follow-up:</b> {aiResponse.follow_up}</p>
            </div>
          ) : (
            <div className="ai-placeholder">
              AI output will appear here after submission
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
