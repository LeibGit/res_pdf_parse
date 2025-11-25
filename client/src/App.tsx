import { useState } from 'react'
import { RingLoader } from 'react-spinners';
import './App.css'

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null); 
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [jobPrompt, setJobPrompt] = useState("");

  const endpoint = "https://res-pdf-parse.onrender.com"

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

      const res = await fetch(`${endpoint}/resume/analyze`, {
        method: 'POST',
        body: formData,
      });


      if (!res.ok) {
        throw new Error(`Network response failed: ${res.status}`);
      }

      const json = await res.json();

      if (typeof json.ats_score === 'string') {
        json.ats_score = parseInt(json.ats_score);
      }
      
      setData(json);


    } catch (error) {
      console.error(error);
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
              placeholder="Enter any Linkedin job description..."
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