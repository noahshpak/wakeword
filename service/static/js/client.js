function sendMessage(socket, event, data) {
    socket.emit(event, {
        data: data
    })
}

function getAudio(socket, duration) {

  const handleSuccess = async function(stream) {
    let recorder = RecordRTC(stream, {
      type: 'audio',
      mimeType: 'audio/wav',
      recorderType: StereoAudioRecorder,
      sampleRate: 44100,
      // used by StereoAudioRecorder
      numberOfAudioChannels: 1
    });
    
    recorder.startRecording();
    const sleep = m => new Promise(r => setTimeout(r, m));
    await sleep(duration);
    recorder.stopRecording(function() {
        var files = {
            audio: {
                type: recorder.getBlob().type || 'audio/wav',
                data: recorder.getBlob()
            }
          }
        // submit the audio file to the server  
        sendMessage(socket, 'my event', files);
    })   
  };
  navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(handleSuccess);    
}

function record() {
  console.log("record");
  var socket = io();
  socket.on('connect', function () {
    socket.on('prediction', function (msg) {
      alert(msg);
    });
    console.log("Connected");
    getAudio(socket, 2000);
    console.log("Message Sent");
  });
}

const recorder = document.getElementById('recorder');
recorder.onclick = record

