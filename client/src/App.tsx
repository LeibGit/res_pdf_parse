import { useState } from 'react'
import { RingLoader } from 'react-spinners';
import './App.css'

interface ResumeData {
  summary: string;
  ats_score: number;
  ats_description: string;
  recomendations: string[];
}

function App() {
  const [data, setData] = useState<ResumeResponse | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [jobPrompt, setJobPrompt] = useState("");


  const endpoint = "http://127.0.0.1:8000/resume";

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const files = e.target.files;
      if (!files || files.length === 0) return;
      const file = files[0];


      if (file.type !== 'application/pdf') {
        setError('Only PDF files are allowed.');
        return;
      }

      const formData = new FormData();
      formData.append("job_prompt", jobPrompt);
      formData.append("resume_file", file);

      const res = await fetch(`${endpoint}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Network response failed: ${res.status} ${text}`);
      }

      const json = await res.json();

      // Normalize ats_score
      if (typeof json.ats_score === "string") {
        json.ats_score = parseInt(json.ats_score);
      }

      setData(json);

    } catch (error: unknown) {
      if (error instanceof Error) {
        console.log(error.message);
      }
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

  // -------------------------- RESULTS PAGE --------------------------
  if (data) {
    const hasError = (data as any)?.summary?.error || (data as any)?.ats_score?.error;

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
              </div>
              <p className="card_text ats_description">{data.ats_description}</p>
            </div>

            <div className="card improvements_card">
              <h2>Suggested Improvements</h2>
              <div className="card_text">
                {data.recomendations}
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

  // -------------------------- LOADING PAGE --------------------------
  if (loading) {
    return (
      <div className='loader'>
        <p>Preparing your AI report... Don't go anywhere!!!</p>
        <RingLoader color="#cec6d0" />
      </div>
    )
  }

  // -------------------------- FORM --------------------------
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