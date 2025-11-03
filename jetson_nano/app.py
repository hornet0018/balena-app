#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

def get_uptime():
    """システムのアップタイムを取得"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
    except:
        return "Unknown"

def get_cpu_temp():
    """CPU温度を取得"""
    try:
        # Jetson Nanoの温度センサーを読み取る
        temp_files = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/sys/class/thermal/thermal_zone1/temp',
            '/sys/devices/virtual/thermal/thermal_zone0/temp',
        ]
        
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    temp = float(f.read().strip()) / 1000.0
                    return f"{temp:.1f}°C"
        
        return "N/A"
    except:
        return "N/A"

def get_cpu_clock():
    """CPUクロック周波数を取得"""
    try:
        # Jetson NanoのCPU周波数を読み取る
        clock_files = [
            '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq',
            '/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq',
        ]
        
        for clock_file in clock_files:
            if os.path.exists(clock_file):
                with open(clock_file, 'r') as f:
                    freq_khz = int(f.read().strip())
                    freq_mhz = freq_khz / 1000.0
                    if freq_mhz >= 1000:
                        return f"{freq_mhz/1000:.2f} GHz"
                    else:
                        return f"{freq_mhz:.0f} MHz"
        
        return "N/A"
    except:
        return "N/A"

def get_fan_speed():
    """ファン速度を取得 (0-255)"""
    try:
        with open('/sys/devices/pwm-fan/target_pwm', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def set_fan_speed(pwm_value):
    """ファン速度を設定 (0-255)"""
    try:
        with open('/sys/devices/pwm-fan/target_pwm', 'w') as f:
            f.write(str(pwm_value))
        return True
    except Exception as e:
        print(f"Error setting fan speed: {e}")
        return False

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """システムステータスを返す"""
    fan_pwm = get_fan_speed()
    fan_percent = int((fan_pwm / 255.0) * 100)
    
    return jsonify({
        'status': 'Running',
        'uptime': get_uptime(),
        'cpu_temp': get_cpu_temp(),
        'cpu_clock': get_cpu_clock(),
        'fan_percent': fan_percent
    })

@app.route('/api/fan/<int:percent>')
def set_fan(percent):
    """ファン速度を設定 (パーセンテージ)"""
    if 0 <= percent <= 100:
        pwm_value = int((percent / 100.0) * 255)
        success = set_fan_speed(pwm_value)
        return jsonify({'success': success, 'percent': percent})
    else:
        return jsonify({'success': False, 'error': 'Invalid percentage'}), 400

if __name__ == '__main__':
    print("Starting Flask server on 0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
