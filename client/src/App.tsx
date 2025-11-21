import { useState } from 'react'
import { RingLoader } from 'react-spinners';
import './App.css'

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null); 
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [jobPrompt, setJobPrompt] = useState("");

  const endpoint = "http://127.0.0.1:8000/resume"

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null); // Clear previous errors
    setData(null);  // Clear previous data

    try {
      const formData = new FormData();
      formData.append("job_prompt", jobPrompt);
      formData.append("resume_file", file);

      const res = await fetch(`${endpoint}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        console.log("Backend error:", text);
        throw new Error(`Network response failed: ${res.status} ${text}`);
      }

      const json = await res.json();
      console.log("Received data:", json);
      setData(json);

    } catch (error) {
      console.error("Error in handleSubmit:", error);
      setError(error.message); 
    } finally {
      setLoading(false);
    }
  };

  
  if (error) {
    return (
      <div className="error">
        <h1>Error</h1>
        <p>{error}</p>
        <button onClick={() => {
          setError(null);
          setData(null);
        }}>Try Again</button>
      </div>
    );
  }

  if (data) {
    const hasError = data.summary?.error || data.ats_score?.error;
    return (
      <div className="results">
        <h1>AI Resume Report</h1>
        {hasError ? (
          <div>
            <p>Oops! There was an error generating your report:</p>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <div>
            <p><strong>Summary:</strong> {data.summary}</p>
            <p><strong>ATS Score:</strong> {data.ats_score}</p>
            <p><strong>Description:</strong> {data.ats_description}</p>
            <p><strong>Recommendations:</strong> {data.reccomendations}</p>
          </div>
        )}
        <button onClick={() => {
          setData(null);
          setFile(null);
          setJobPrompt("");
        }}>Analyze Another Resume</button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className='loader'>
        <p>Preparing your AI report... This loader should keep you entertained!!!</p>
        <RingLoader />
      </div>
    )
  }

  return (
    <div>
      <h1>Rez Ai</h1>
      <form className="user_inputs" onSubmit={handleSubmit}>
        <label>
          Upload your resume:
          <input
            className="resume_file"
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </label>

        <label>
          Job description:
          <textarea
            className="job_prompt"
            placeholder="Copy and paste the job description here..."
            value={jobPrompt}
            onChange={(e) => setJobPrompt(e.target.value)}
            required
          />
        </label>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;