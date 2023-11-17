import './App.css'

function App() {

  return (
    <div className="wrapper">
      <div className="card">
        <h2 className="title">Camera Streaming</h2>
        <img id="camera-stream" src="http://192.168.1.140:8000/stream/camera"></img>
      </div>
      
      <div className="card">
        <h2 className="title">Video Streaming</h2>
        <video controls width="640" height="480">
          <source src="http://192.168.1.140:8000/stream/video" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  )
}

export default App
