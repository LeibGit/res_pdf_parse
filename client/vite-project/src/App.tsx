import './App.css'

function App() {
  return (
    <>
      <div className='file_upload_div'>
          <input placeholder='Drop your resume here' type='file' />
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
            rows={6}
            placeholder="Paste your job description or resume here..."
          />
      </div>
      <div className='submission'>
        <button className='submit-button'>Submit</button>
      </div>
    </>
  )
}

export default App
