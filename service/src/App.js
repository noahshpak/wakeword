import React from 'react';
import { Recorder } from 'react-voice-recorder';
import 'react-voice-recorder/dist/index.css';

import './App.css';

class AudioRecorder extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      audioDetails: {
        url: null,
        blob: null,
        chunks: null,
        duration: {
          h: 0,
          m: 0,
          s: 0
        }
      }
    }
  }
  handleAudioPause(e) {
    e.preventDefault();
    clearInterval(this.timer);
    this.mediaRecorder.pause();
    this.setState({ pauseRecord: true });
  }
  handleAudioStop(data){
    console.log(data)
    this.setState({ audioDetails: data });
  }
  handleAudioUpload(file) {
    console.log(file);
  }
  handleReset() {
    const reset = {
      url: null,
      blob: null,
      chunks: null,
      duration: {
        h: 0,
        m: 0,
        s: 0
      }
    };
    this.setState({ audioDetails: reset });
  }
  render() {
    return <Recorder
      record={true}
      title={"New recording"}
      audioURL={this.state.audioDetails.url}
      showUIAudio
      handleAudioStop={data => this.handleAudioStop(data)}
      handleAudioUpload={data => this.handleAudioUpload(data)}
      handleAudioPause={e => this.handleAudioPause(e)}
      handleReset={() => this.handleReset()}
    />
  }
}

function App() {
  return (
    <div className="App">
      <div>
        <AudioRecorder />
      </div>
    </div>
  );
}

export default App;
