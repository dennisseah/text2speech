# text2speech

## Prerequisites

1. Install uv [guide](https://docs.astral.sh/uv/getting-started/installation/)
2. Install taskfile [guide](https://taskfile.dev/#/installation)

## Setup

```bash
cd <this project folder>
uv sync
pre-commit install
cp .env.example .env
```

edit `.env` and fill in the required environment variables

## Azure Service

Install Azure AI Service and get the endpoint URL. Set the endpoint URL in the
`.env` file as `SPEECH_ENDPOINT`. The endpoint URL should be a custom domain
endpoint, e.g. `https://<resource-name>.cognitiveservices.azure.com/`

## Activate virtual environment

MacOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### vscode extensions

1. code . (open the project in vscode)
1. install the recommended extensions (cmd + shift + p ->
   `Extensions: Show Recommended Extensions`)

## Testing

## Unit Tests

```bash
task test:unit
```

## Linting

these are handled by pre-commit hooks

```sh
ruff format .
```

```sh
ruff check .
```

```sh
pyright .
```

## generate requirements.txt

these are handled by pre-commit hooks

```sh
uv lock
uv export --frozen --no-dev --output-file=requirements.txt
uv export --frozen --all-groups --output-file=requirements.dev.txt
```
