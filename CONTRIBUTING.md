# Contributing

Thank you for considering contributing to **video-bot**!

## Getting Started

1. Fork the repository and clone it locally:

```bash
git clone https://github.com/bohd4nx/Telegram-Video-Bot.git
cd Telegram-Video-Bot
```

2. Install dependencies:

```bash
pip install ".[dev]"
```

3. Copy the example env and fill in your values:

```bash
cp .env.example .env
```

## Development Workflow

- Create a branch for your change: `git checkout -b feat/my-feature`
- Make your changes, then run the linter and type checker:

```bash
ruff check . --fix && ruff format . && mypy . --explicit-package-bases
```

- Commit using [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `refactor:`, etc.
- Open a Pull Request against `master`

## Code Style

- **Formatter / linter:** [ruff](https://github.com/astral-sh/ruff) (line length 120)
- **Type checker:** [mypy](https://mypy-lang.org)
- **Python:** 3.10+

## Reporting Issues

Please open an issue with:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behaviour
- Python version and OS

## Questions

Reach out on Telegram: [@bohd4nx](https://t.me/bohd4nx)
