import { useState } from 'react';
import { RingLoader } from 'react-spinners';
import './App.css';

interface ResumeResponse {
  summary: string;
  ats_score: number;
  ats_description: string;
  recomendations: string[];
  education: string[];
}

function App() {
  const [file, setFile] = useState<File | null>(null);  
  const [error, setError] = useState<string | null>(null); 
  const [data, setData] = useState<ResumeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [jobPrompt, setJobPrompt] = useState("");

  const endpoint = "https://res-pdf-parse.onrender.com";

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      setError("Please upload a PDF.");
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }

    const formData = new FormData();
    formData.append("job_prompt", jobPrompt);
    formData.append("resume_file", file);

    try {
      setLoading(true);
      setError(null);
      setData(null);

      const res = await fetch(`${endpoint}/resume/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Network response failed: ${res.status}`);
      }

      const json = await res.json() as ResumeResponse;

      if (typeof json.ats_score === "string") {
        json.ats_score = parseInt(json.ats_score);
      }

      setData(json);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
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
    return (
      <div className="results">
        <h1 className='report_title'>AI Resume Report</h1>
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
            </div>
            <p className="card_text ats_description">{data.ats_description}</p>
          </div>

          <div className="card improvements_card">
            <h2>Suggested Improvements</h2>
            <div className="card_text">
              {Array.isArray(data.recomendations) ? (
                <ul>
                  {data.recomendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              ) : (
                <p>{data.recomendations}</p>
              )}
            </div>
          </div>

          <div className="card education_card">
            <h2>Education</h2>
            <div className="card_text">
              {data.education && data.education.length > 0 ? (
                <ul>
                  {data.education.map((edu, index) => (
                    <li key={index}>{edu}</li>
                  ))}
                </ul>
              ) : (
                <p>No education information found in resume.</p>
              )}
            </div>
          </div>

        </div>

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
        <p>Preparing your AI report... Don't go anywhere!!!</p>
        <RingLoader color="#cec6d0" />
      </div>
    )
  }

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
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  setFile(e.target.files[0]);
                }
              }}
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