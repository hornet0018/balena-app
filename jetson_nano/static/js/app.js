const slider = document.getElementById('fanSlider');
const fanDisplay = document.getElementById('fan-display');

slider.addEventListener('input', function() {
    fanDisplay.textContent = this.value;
});

slider.addEventListener('change', function() {
    fetch(`/api/fan/${this.value}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStatus();
            }
        })
        .catch(error => console.error('Error:', error));
});

function updateStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').textContent = data.status;
            document.getElementById('uptime').textContent = data.uptime;
            document.getElementById('cpu-temp').textContent = data.cpu_temp;
            document.getElementById('cpu-clock').textContent = data.cpu_clock;
            document.getElementById('current-fan').textContent = data.fan_percent + '%';
            slider.value = data.fan_percent;
            fanDisplay.textContent = data.fan_percent;
            
            const now = new Date();
            document.getElementById('last-update').textContent = 
                `Last update: ${now.toLocaleTimeString()}`;
        })
        .catch(error => console.error('Error:', error));
}

// 初期状態を取得
updateStatus();

// 5秒ごとに更新
setInterval(updateStatus, 5000);
