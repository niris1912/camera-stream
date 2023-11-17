import './App.css'
import {useState} from 'react'
import axios from 'axios'

function App() {

  const endpoint = 'http://localhost:8000'
  const captureApi = `${endpoint}/stream/capture/`;

  const [capturing, setCapturing] = useState(false);

  const startRecord = () => {

    if (!capturing) {

      axios.post(captureApi, {
        action: 'start'
      }).then((data) => {
        
        if (data.status) 
          setCapturing(true);
        else {
          console.log('error');
          alert("Can't start capture! You should stop current capturing first!");        
        }
        
      })

    } else {
      alert("Can't start capture! You should stop current capturing first!");
    }    

  }

  const stopRecord = () => {

    if (capturing) {

      axios.post(captureApi, {
        action: 'stop'
      }).then((data) => {
        if (data.status) 
          setCapturing(false);
        else {
          console.log('error');
          alert("Can't stop capture! You should stop current capturing first!");        
        }

      })

    } else {
      alert("Can't start capture! You should stop current capturing first!");
    }

  }

  const restartRecord = () => {
    if (capturing) {

      axios.post(captureApi, {
        action: 'restart'
      }).then((data) => {
        
        if (data.status) 
          setCapturing(true);
        else {
          console.log('error');
          alert("Can't start capture! You should stop current capturing first!");        
        }
        
      })

    } else {
      alert("Can't start capture! You should stop current capturing first!");
    }
  }

  return (
    <div className="wrapper">
      <div className="card">
        <h2 className="title">Camera Streaming</h2>
        <div className="buttons">
          <button 
            className={`camera-button ${capturing ? 'disabled' : ''}`}
            onClick={startRecord}>
            Start
          </button>

          <button 
            className={`camera-button ${capturing ? '' : 'disabled'}`}
            onClick={stopRecord}>
            Stop
          </button>
          
          <button 
            className={`camera-button ${capturing ? '' : 'disabled'}`}
            onClick={restartRecord}>
            Restart
          </button>
          
        </div>
        <img id="camera-stream" src={`${endpoint}/stream/camera`}></img>
      </div>
      
      <div className="card">
        <h2 className="title">Video Streaming</h2>
        <video controls width="640" height="480">
          <source src={`${endpoint}/stream/video`} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  )
}

export default App
