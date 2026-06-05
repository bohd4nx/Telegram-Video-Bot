<div align="center">

# video-bot

Telegram bot that converts any video — or a TikTok / Instagram / YouTube Shorts link — into a **round video note** (video circle).
Supports iOS and Android overlay styles, automatic segmentation of long videos, and PostgreSQL-backed download history.

**[Try Demo](https://t.me/RoundMsgBot)** · **[Report Bug](https://github.com/bohd4nx/Telegram-Video-Bot/issues)** · **[Request Feature](https://github.com/bohd4nx/Telegram-Video-Bot/issues)**

</div>

---

## Features

- **Circle conversion** — crops, masks, and scales any video to a perfect 640×640 round note
- **Overlay styles** — iOS (white border) or Android (transparent) — user chooses per video
- **URL downloads** — paste a TikTok, Instagram Reel, or YouTube Shorts link and get a circle
- **Auto-segmentation** — videos longer than 60 s are split and sent as sequential notes
- **i18n** — Russian and English, auto-detected from Telegram locale
- **PostgreSQL** — stores users and download history

---

## Quick Start

### Docker (recommended)

```bash
git clone https://github.com/bohd4nx/Telegram-Video-Bot.git
cd Telegram-Video-Bot
cp .env.example .env   # fill in BOT_TOKEN, POSTGRES_*
docker compose up -d
```

### Local

```bash
git clone https://github.com/bohd4nx/Telegram-Video-Bot.git
cd Telegram-Video-Bot

# requires Python 3.10+ and ffmpeg installed
pip install .

cp .env.example .env   # fill in BOT_TOKEN, POSTGRES_*
python main.py
```

**Install ffmpeg:**

```bash
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Ubuntu/Debian
choco install ffmpeg         # Windows
```

---

## Configuration

Copy `.env.example` to `.env` and fill in the values:

| Variable            | Required | Default | Description                                     |
| ------------------- | -------- | ------- | ----------------------------------------------- |
| `BOT_TOKEN`         | ✅       | —       | Token from [@BotFather](https://t.me/BotFather) |
| `POSTGRES_USER`     | ✅       | —       | PostgreSQL username                             |
| `POSTGRES_PASSWORD` | ✅       | —       | PostgreSQL password                             |
| `POSTGRES_DB`       | ✅       | —       | PostgreSQL database name                        |
| `POSTGRES_HOST`     | —        | `db`    | PostgreSQL host (Docker service name)           |
| `POSTGRES_PORT`     | —        | `5432`  | PostgreSQL port                                 |
| `ADMIN_IDS`         | —        | —       | Comma-separated admin Telegram IDs              |
| `SUPPORT_URL`       | —        | —       | Support link shown in /help                     |

---

## Usage

### Commands

| Command  | Description     |
| -------- | --------------- |
| `/start` | Welcome message |
| `/help`  | Usage guide     |

### Sending a video

1. Send any video file → bot asks for overlay style (iOS / Android)
2. Choose overlay → bot processes and sends back round video note(s)

### Sending a URL

1. Paste a TikTok, Instagram Reel, or YouTube Shorts link
2. Bot downloads and processes it the same way

---

<div align="center">

Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx) · [Contributing](CONTRIBUTING.md)

**Star ⭐ if you found it useful**

</div>
