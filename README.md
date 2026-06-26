# test-speeder

CLI internet speed tester — measures your download speed via 10 sequential HTTP requests.

## Quick start

### Option A — Docker (recommended, no local Python required)

```bash
# 1. Clone the repository
git clone https://github.com/Primero1800/test-speeder.git
cd test-speeder

# 2. (Optional) Set your own test URL
cp .env.example .env
# edit .env → TARGET_URL=https://...

# 3. Build and run
docker compose run --rm service

# Clean up everything when done
docker compose down --rmi all
```

### Option B — Poetry (local venv)

```bash
# 1. Clone the repository
git clone https://github.com/Primero1800/test-speeder.git
cd test-speeder

# 2. Install Poetry (if not installed)
pip install poetry

# 3. Install dependencies
poetry install

# 4. (Optional) Set your own test URL
cp .env.example .env

# 5. Run
poetry run python main.py
```

## Usage

```bash
# Interactive (will ask for URL at startup)
docker compose run --rm service

# Pass URL directly
docker compose run --rm service --url https://example.com/large-file.jpg

# With Poetry
poetry run python main.py --url https://example.com/large-file.jpg
```

## Configuration

Copy `.env.example` to `.env` and edit as needed:

| Variable | Default | Description |
|---|---|---|
| `TARGET_URL` | _(empty)_ | URL of a large file. If empty, you will be prompted at startup. |
| `REQUEST_COUNT` | `10` | Number of sequential requests |
| `REQUEST_TIMEOUT` | `30` | Timeout per request in seconds |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
