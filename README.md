# Jetson Nano Web Control Panel

Jetson Nano用のWebベース制御パネルアプリケーションです。ファン制御、CPU温度・クロック監視機能を提供します。

## 機能

- 🌀 **ファン制御**: リアルタイムでファン速度を0-100%で調整可能
- 🌡️ **CPU温度監視**: Jetson NanoのCPU温度をリアルタイム表示
- ⚡ **CPUクロック監視**: 現在のCPU周波数を表示
- ⏱️ **稼働時間表示**: システムのアップタイムを表示
- 📊 **自動更新**: 5秒ごとにステータスを自動更新
- 🎨 **モダンUI**: レスポンシブデザインでモバイル対応

## 技術スタック

- **Backend**: Python 3.6 + Flask 2.0.3
- **Frontend**: Vanilla JavaScript + CSS3
- **コンテナ**: Docker (Balena対応)
- **ベースイメージ**: balenalib/jetson-nano-ubuntu:bionic-run-20221215

## デプロイ方法

### Balena CLIを使用

1. Balena CLIをインストール
2. デバイスを検出:
```bash
balena device detect
```

3. ローカルプッシュ:
```bash
balena push <device-ip>.local
```

例:
```bash
balena push 39c639e.local
```

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|------------|------|
| `FAN_PERCENT` | 50 | 起動時のファン速度 (0-100%) |

## 使い方

1. デプロイ後、ブラウザで `http://<device-ip>:8080` にアクセス
2. リアルタイムでシステムステータスを確認
3. スライダーでファン速度を調整

## ファイル構成

```
jetson_nano/
├── Dockerfile              # コンテナ定義
├── app.py                  # Flaskアプリケーション
├── requirements.txt        # Python依存関係
├── static/
│   ├── css/
│   │   └── style.css      # スタイルシート
│   └── js/
│       └── app.js         # フロントエンドロジック
└── templates/
    └── index.html         # HTMLテンプレート
```

## API エンドポイント

### `GET /api/status`
システムステータスを取得

**レスポンス例:**
```json
{
  "status": "Running",
  "uptime": "2h 15m",
  "cpu_temp": "45.2°C",
  "cpu_clock": "1479 MHz",
  "fan_percent": 50
}
```

### `GET /api/fan/<percent>`
ファン速度を設定 (0-100%)

**レスポンス例:**
```json
{
  "success": true,
  "percent": 75
}
```

## 開発

ローカルで開発する場合:

```bash
cd jetson_nano
pip3 install -r requirements.txt
python3 app.py
```

ブラウザで `http://localhost:8080` にアクセス

## ライセンス

MIT License
