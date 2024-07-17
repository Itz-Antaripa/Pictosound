import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [audioSrc, setAudioSrc] = useState(null);
  const [lyrics, setLyrics] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:3001/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data.analysis);
      setAudioSrc(`http://localhost:3001/${response.data.musicPath}`);
      setLyrics(response.data.lyrics);
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing the image.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Synesthetic Soundscape</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Analyze Image and Generate Music'}
        </button>
      </form>
      {result && (
        <div>
          <h2>Analysis Result:</h2>
          <pre>{result}</pre>
        </div>
      )}
      {lyrics && (
        <div>
          <h2>Generated Lyrics:</h2>
          <pre>{lyrics}</pre>
        </div>
      )}
      {audioSrc && (
        <div>
          <h2>Generated Music:</h2>
          <audio controls src={audioSrc}>
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
}

export default App;
