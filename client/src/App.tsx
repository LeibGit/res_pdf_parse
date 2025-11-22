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
    console.log("🚀 Form submitted");
    
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const formData = new FormData();
      formData.append("job_prompt", jobPrompt);
      formData.append("resume_file", file);

      console.log("📤 Sending request to:", `${endpoint}/analyze`);

      const res = await fetch(`${endpoint}/analyze`, {
        method: 'POST',
        body: formData,
      });

      console.log("📥 Response status:", res.status);

      if (!res.ok) {
        const text = await res.text();
        console.log("❌ Backend error:", text);
        throw new Error(`Network response failed: ${res.status} ${text}`);
      }

      const json = await res.json();
      console.log("✅ Received data:", json);
      console.log("✅ Data type:", typeof json);
      console.log("✅ ATS Score:", json.ats_score);
      
      // Ensure ats_score is a number
      if (typeof json.ats_score === 'string') {
        json.ats_score = parseInt(json.ats_score);
      }
      
      setData(json);
      console.log("✅ Data state set successfully!");

    } catch (error) {
      console.error("❌ Error in handleSubmit:", error);
      setError(error.message); 
    } finally {
      console.log("🏁 Setting loading to false");
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
    console.log("🎨 Rendering results page with data:", data);
    const hasError = data.summary?.error || data.ats_score?.error;
    
    return (
      <div className="results">
        <h1 className='report_title'>AI Resume Report</h1>
        {hasError ? (
          <div>
            <p>Oops! There was an error generating your report:</p>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <div className="results_grid">
            <div className="card summary_card">
              <h2>Resume Summary</h2>
              <p className="card_text">{data.summary}</p>
            </div>

            <div className="card ats_card">
              <h2>ATS Score</h2>
              <div className="ats_bar_container">
                <div className="ats_bar" style={{ width: `${data.ats_score}%` }}></div>
                <span className="ats_number">{data.ats_score}</span>
                console.log(json.data.ats_score)
              </div>
              <p className="card_text ats_description">{data.ats_description}</p>
            </div>

            <div className="card improvements_card">
              <h2>Suggested Improvements</h2>
              <div className="card_text">
                {data.reccomendations}
              </div>
            </div>

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
    console.log("⏳ Showing loading screen");
    return (
      <div className='loader'>
        <p>Preparing your AI report... Don't go anywhere!!!</p>
        <RingLoader color="#cec6d0" />
      </div>
    )
  }

  console.log("📝 Showing form");
  return (
    <div>
      <h1 className="title">Rez Ai</h1>
      <p className="tagline">Score, analyze, and improve your resume instantly.</p>
      <form className="user_inputs" onSubmit={handleSubmit}>
        <div className="input_group">
          <label className='file_label'>
            Upload your resume:
            <input
              className="resume_file"
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </label>
        </div>
        <div className="input_group">
          <label className='prompt_label'>
            Job description:
            <textarea
              className="job_prompt"
              placeholder="Copy and paste the job description here..."
              value={jobPrompt}
              onChange={(e) => setJobPrompt(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit" className='submit'>Analyze Resume</button>
      </form>
    </div>
  );
}

export default App;