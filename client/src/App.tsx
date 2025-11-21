import { useState } from 'react'
import './App.css'

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [jobPrompt, setJobPrompt] = useState("");

  const endpoint = "http://127.0.0.1:8000/resume"

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {

      const formData = new FormData();
      formData.append("job_prompt", jobPrompt);
      formData.append("resume_file", file);

      const res = await fetch(`${endpoint}/analyze`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        throw new Error("Netork response failed.");
      }

      const data = await res.json();
      console.log("Response from backend:", data);

    } catch (error) {
      throw new Error("An unkown error occured");
    }
  }

  return ( 
    <>
    <h1>Rez Ai</h1>
    <form className='user_inputs' onSubmit={handleSubmit}>  
      <label>Upload your resume: 
        <input className='resume_file' type='file' onChange={(e) => setFile(e.target.files[0])} />
      </label>
      <label>Upload your user inputs:
        <input className='job_prompt' type='text' placeholder='Copy and paste the job description here...' value={jobPrompt} onChange={(e) => setJobPrompt(e.target.value)} />
      </label>
      <button type='submit'>Submit</button>
    </form>
    </>
  )
}

export default App
