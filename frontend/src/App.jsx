import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    try {
      setError("");
      const res = await axios.post("http://localhost:5000/analyze", { code });
      console.log(res.data);  // Log the response data
      setResult(res.data);
    } catch (err) {
      setResult(null);
      setError(err.response?.data?.error || "Error analyzing code");
    }
  };

  return (
    <div className="min-h-screen p-8 flex flex-col items-center bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-6">🧠 Code Analyzer</h1>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your Python code here..."
        className="w-full max-w-3xl p-4 rounded bg-gray-800 text-white h-60 resize-none shadow-lg"
      />
      <button
        onClick={handleSubmit}
        className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white font-semibold"
      >
        Analyze
      </button>

      {result && (
        <div className="mt-6 bg-gray-800 p-4 rounded shadow-md w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-2">🔍 Analysis Result</h2>
          <p><strong>Execution Time:</strong> {result.time_taken.toFixed(6)} sec</p>
          <p><strong>Peak Memory:</strong> {result.peak_memory} bytes</p>
          <p><strong>Output:</strong> {result.output}</p>
          <p><strong>Time Complexity:</strong> {result.time_complexity}</p>
          <p><strong>Space Complexity:</strong> {result.space_complexity}</p>
        </div>
      )}

      {error && (
        <div className="mt-6 bg-red-800 p-4 rounded shadow-md w-full max-w-2xl">
          <p><strong>Error:</strong> {error}</p>
        </div>
      )}
    </div>
  );
};

export default App;
