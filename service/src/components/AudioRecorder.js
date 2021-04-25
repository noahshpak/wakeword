import React from "react";

class Recorder extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            time: {},
            seconds: 0,
            recording: false,
            audio: [],
            audioBlob: null
        };
        this.timer = 0;
        this.startTimer = this.startTimer.bind(this);
        this.countDown = this.countDown.bind(this);
    }

    startTimer() {
        this.timer = setInterval(this.countDown, 1000);
    }

    countDown() {
        let seconds = this.state.seconds + 1;
        this.setState({
            time: this.secondsToTime(seconds),
            seconds: seconds
        });
    }

    secondsToTime(secs) {
        let hours = Math.floor(secs / (60 * 60));
    
        let divisor_for_minutes = secs % (60 * 60);
        let minutes = Math.floor(divisor_for_minutes / 60);
    
        let divisor_for_seconds = divisor_for_minutes % 60;
        let seconds = Math.ceil(divisor_for_seconds);
    
        let obj = {
          h: hours,
          m: minutes,
          s: seconds
        };
        return obj;
    }

    async componentDidMount() {
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        if (navigator.mediaDevices) {
            const stream = await navigator.mediaDevices.getUserMedia({audio: true});
            this.
        }
    }
}