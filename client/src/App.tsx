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
  const [showRating, setShowRating] = useState(false);
  const [activePanel, setActivePanel] = useState<'summary' | 'ats' | 'improvements' | 'education'>('summary');

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

  // -------------------------- ERROR PAGE --------------------------
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

  // -------------------------- RATING PAGE --------------------------
  if (showRating) {
    return (
      <div className="rating_page">
        <h1>Rate Your AI Resume Report</h1>

        <form 
          action="https://formspree.io/f/xgvgyekd" 
          method="POST" 
          className="rating_form"
        >
          <label>
            Your Email:
            <input type="email" name="email" required />
          </label>

          <label>
            Your Rating:
            <select name="rating" required>
              <option value="">Select a rating</option>
              <option value="5">⭐⭐⭐⭐⭐ — Excellent</option>
              <option value="4">⭐⭐⭐⭐ — Good</option>
              <option value="3">⭐⭐⭐ — Okay</option>
              <option value="2">⭐⭐ — Poor</option>
              <option value="1">⭐ — Terrible</option>
            </select>
          </label>

          <label>
            Additional Comments:
            <textarea name="comments" rows={4}></textarea>
          </label>

          <button type="submit" className="submit_rating">
            Submit Rating
          </button>
        </form>

        <button
          className="analyze_another"
          onClick={() => setShowRating(false)}
        >
          Back to Report
        </button>
      </div>
    );
  }

  // -------------------------- RESULTS PAGE --------------------------
  if (data) {
    return (
      <div className="results">
        <h1 className='report_title'>AI Resume Report</h1>
        
        <div className="results_grid">
          <button
            type="button"
            className={`card summary_card ${activePanel === 'summary' ? 'card_active' : ''}`}
            onClick={() => setActivePanel('summary')}
          >
            <h2>Resume Summary</h2>
            <p className="card_text">
              {data.summary.length > 180
                ? data.summary.slice(0, 180) + '...'
                : data.summary}
            </p>
          </button>

          <button
            type="button"
            className={`card ats_card ${activePanel === 'ats' ? 'card_active' : ''}`}
            onClick={() => setActivePanel('ats')}
          >
            <h2>ATS Score</h2>
            <div className="ats_bar_container">
              <div className="ats_bar" style={{ width: `${data.ats_score}%` }}></div>
              <span className="ats_number">{data.ats_score}</span>
            </div>
            <p className="card_text ats_description">
              {data.ats_description.length > 140
                ? data.ats_description.slice(0, 140) + '...'
                : data.ats_description}
            </p>
          </button>

          <button
            type="button"
            className={`card improvements_card ${activePanel === 'improvements' ? 'card_active' : ''}`}
            onClick={() => setActivePanel('improvements')}
          >
            <h2>Suggested Improvements</h2>
            <div className="card_text">
              {Array.isArray(data.recomendations) ? (
                <ul>
                  {data.recomendations.slice(0, 3).map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                  {data.recomendations.length > 3 && (
                    <li>+ {data.recomendations.length - 3} more suggestions</li>
                  )}
                </ul>
              ) : (
                <p>{data.recomendations}</p>
              )}
            </div>
          </button>

          <button
            type="button"
            className={`card education_card ${activePanel === 'education' ? 'card_active' : ''}`}
            onClick={() => setActivePanel('education')}
          >
            <h2>Education</h2>
            <div className="card_text">
              {data.education && data.education.length > 0 ? (
                <ul>
                  {data.education.slice(0, 3).map((edu, index) => (
                    <li key={index}>{edu}</li>
                  ))}
                  {data.education.length > 3 && (
                    <li>+ {data.education.length - 3} more entries</li>
                  )}
                </ul>
              ) : (
                <p>No education information found in resume.</p>
              )}
            </div>
          </button>
        </div>

        <div className="details_panel">
          {activePanel === 'summary' && (
            <>
              <h2>Full Resume Summary</h2>
              <p className="card_text">{data.summary}</p>
            </>
          )}

          {activePanel === 'ats' && (
            <>
              <h2>ATS Score Details</h2>
              <div className="ats_bar_container">
                <div className="ats_bar" style={{ width: `${data.ats_score}%` }}></div>
                <span className="ats_number">{data.ats_score}</span>
              </div>
              <p className="card_text ats_description">{data.ats_description}</p>
            </>
          )}

          {activePanel === 'improvements' && (
            <>
              <h2>All Suggested Improvements</h2>
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
            </>
          )}

          {activePanel === 'education' && (
            <>
              <h2>Education Details</h2>
              <div className="card_text">
                {data.education && data.education.length > 0 ? (
                  <ul style={{ listStyle: 'none', padding: 0 }}>
                    {data.education.map((edu, index) => (
                      <li key={index} style={{ marginBottom: '0.5rem' }}>
                        {edu}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No education information found in resume.</p>
                )}
              </div>
            </>
          )}
        </div>

        <button
          className="submit_rating"
          onClick={() => setShowRating(true)}
        >
          Rate Your Experience
        </button>

        <button className='analyze_another' onClick={() => {
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
        <p className='loader_text'>Preparing your AI report... Don't go anywhere!!!</p>
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