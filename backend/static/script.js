const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const videoFeed = document.getElementById('video-feed');

startBtn.addEventListener('click', async () => {
    // Tell server to start streaming
    await fetch('/start_stream', { method: 'POST' });

    // Replace video feed with streaming img tag
    videoFeed.innerHTML = '<img src="/video_feed" style="width:100%; height:auto; border-radius:8px;" />';
});

stopBtn.addEventListener('click', async () => {
    // Tell server to stop streaming
    await fetch('/stop_stream', { method: 'POST' });

    // Remove the img tag, show placeholder text again
    videoFeed.innerHTML = '<p>Video feed will be displayed here...</p>';
});
