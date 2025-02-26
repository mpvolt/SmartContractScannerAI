import { useState } from "react";
import axios from "axios";
import "./SolidityScanner.css"; // ✅ Import CSS file

export default function SolidityScanner() {
  const [solidityCode, setSolidityCode] = useState("");
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
    setError("");
  };

  // Handle text input change
  const handleCodeChange = (event) => {
    setSolidityCode(event.target.value);
    setError("");
  };

  // Submit Solidity code or file to backend using axios
  const handleSubmit = async () => {
    setLoading(true);
    setAnalysisResult("");
    setError("");

    const formData = new FormData();

    if (file) {
      console.log("📂 File selected:", file);
      formData.append("file", file, file.name);
    } else if (solidityCode.trim()) {
      console.log("📝 Solidity code submitted.");
      formData.append("code", solidityCode);
    } else {
      setError("❌ Please upload a file or enter Solidity code.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5001/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Accept": "application/json",
        },
      });

      console.log("✅ Server Response:", response.data);
      setAnalysisResult(response.data.analysis);
    } catch (err) {
      console.error("❌ Axios Error:", err);
      setError(err.response?.data?.error || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>🔍 Solidity Security Scanner</h2>

      {/* File Upload Input */}
      <label htmlFor="fileUpload">📂 Upload Solidity File</label>
      <input
        id="fileUpload"
        type="file"
        accept=".sol"
        onChange={handleFileChange}
      />

      <label htmlFor="solidityCode">✍️ Or Paste Solidity Code</label>
      <textarea
        id="solidityCode"
        placeholder="Paste your Solidity code here..."
        value={solidityCode}
        onChange={handleCodeChange}
      ></textarea>

      {/* Submit Button */}
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Contract"}
      </button>

      {/* Error Message */}
      {error && <div className="error"><strong>⚠️ Error:</strong> {error}</div>}

      {/* Display Analysis Result */}
      {analysisResult && (
        <div className="result">
          <h3>🧠 AI Analysis:</h3>
          <pre>{analysisResult}</pre>
        </div>
      )}
    </div>
  );
}
