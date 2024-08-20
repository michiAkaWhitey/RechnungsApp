feather.replace();

const controls = document.querySelector('.controls');
const cameraOptions = document.querySelector('.video-options>select');
const video = document.querySelector('video');
const canvas = document.querySelector('canvas');
const screenshotImage = document.querySelector('img');
const buttons = [...controls.querySelectorAll('button')];
let streamStarted = false;
const [play, pause, screenshot] = buttons;
let currentStream = null;

const constraints = {
    video: {
        width: {
            min: 1280,
            ideal: 1920,
            max: 2560,
        },
        height: {
            min: 720,
            ideal: 1080,
            max: 1440
        },
        deviceId: null
    }
}

const getCameraSelection = () => {
    navigator.mediaDevices.enumerateDevices().then((devices) => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        const options = videoDevices.map(videoDevice => {
            return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
        });
        cameraOptions.innerHTML = options.join('');
    });
}

const startStream = (constraints, changeMode = false) => {
    try {
        if (currentStream) {
            currentStream.getTracks().forEach(track => {
                track.stop();
            });
        }
        navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
            if (!changeMode) getCameraSelection();
            video.srcObject = stream;
            play.classList.add('d-none');
            pause.classList.remove('d-none');
            screenshot.classList.remove('d-none');
            streamStarted = true;
        });
    } catch (e) {
        console.error(e);
    }
}

play.onclick = () => {
    if (streamStarted) {
        video.play();
        play.classList.add('d-none');
        pause.classList.remove('d-none');
        return;
    }
    if ('mediaDevices' in navigator) {
        startStream(constraints);
    }
}

cameraOptions.onchange = () => {
    constraints.video.deviceId = {
        exact: cameraOptions.value
    };
    startStream(constraints, true);
}

pause.onclick = () => {
    video.pause();
    play.classList.remove('d-none');
    pause.classList.add('d-none');
}

screenshot.onclick = () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    screenshotImage.src = canvas.toDataURL('image/webp');
    screenshotImage.classList.remove('d-none');
}