<div align="center">
  <img src="files/logo.svg" alt="Bot Logo" width="120"
  height="120" style="border-radius: 24px;">

  <h1 style="margin-top: 24px;">🎥 Telegram Video Bot</h1>

  <p style="font-size: 18px; color: #666; margin-bottom: 24px;">
    <strong>Transform regular videos into perfect circular video notes</strong>
  </p>

  <p>
    <a href="https://github.com/bohd4nx/Telegram-Video-Bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/bohd4nx/Telegram-Video-Bot/issues">Request Feature</a>
    ·
    <a href="https://t.me/bohd4nx">Try Demo</a>
  </p>

</div>

## ✨ Features

- 🎯 **Circle Videos** - Creates perfect circular videos with the same overlay as in Telegram for Android
- ⚡ **Fast Processing** - Uses optimized ffmpeg pipeline for maximum speed
- 🎵 **Audio Encoding** - Encodes audio to AAC 96k for optimal quality and size
- 📐 **Smart Cropping** - Automatic centering and scaling
- 🎬 **Video Segmentation** - Automatically splits long videos into 60-second segments
- 🔧 **Simple Usage** - Only /start and /help commands

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/bohd4nx/Telegram-Video-Bot.git
cd Telegram-Video-Bot
pip install -r requirements.txt
```

### 2. Install FFmpeg

```bash
# macOS (Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg
```

### 3. Configuration

Create `.env` file in project root:

```env
# Get token from @BotFather
BOT_TOKEN=your_bot_token_here
```

### 4. Run

```bash
python main.py
```

## 📱 Usage

### Bot Commands

- `/start` - Welcome message and instructions
- `/help` - Detailed usage guide

### Video Processing Flow

1. Send video to bot
2. Wait for processing (⏳ Processing...)
3. Receive circular video with white background (like original Telegram format)
4. Forward as regular video note

## 📋 Video Requirements

### Input Parameters

- **Format**: MP4, AVI, MOV and others
- **Size**: Up to 20MB
- **Duration**: Recommended up to 60 seconds
- **Resolution**: Any (automatically processed)

### Output Specifications

- **Format**: Circular video (video note)
- **Resolution**: Up to 640×640 (optimized for Telegram)
- **Codec**: H.264 + AAC
- **Background**: White outside circle
- **Audio**: Preserved from original

## ⚙️ Technical Implementation

### Processing Algorithm

1. **Download** - Get video from user
2. **Analysis** - Determine dimensions and parameters
3. **Cropping** - Extract square from frame center
4. **Mask** - Apply circular mask with white background
5. **Scaling** - Resize to optimal dimensions
6. **Audio** - Merge with original audio via FFmpeg
7. **Upload** - Send as video note to Telegram

### Optimization

- Maximum resolution 640×640 for Telegram compliance
- Even dimensions for codec compatibility
- Fast FFmpeg presets for speed
- Automatic temporary file cleanup

## 🐛 Error Handling

| Error                   | Cause                     | Solution           |
| ----------------------- | ------------------------- | ------------------ |
| File too large          | File > 20MB               | Compress video     |
| Voice messages disabled | Voice messages turned off | Enable in settings |
| Processing error        | Processing failure        | Check video format |

## 🛠️ Deployment

### Docker (Optional)

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Environment Variables

```env
BOT_TOKEN=your_telegram_bot_token
```

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
