# text2speech

The text2speech package provides a simple interface to convert text to speech
using Azure AI Service. It uses the Azure Cognitive Services Speech SDK to
perform text-to-speech conversion. The package is designed to be easy to use and
can be integrated into any Python project. It also supports multiple voices and
languages, allowing you to customize the speech output to suit your needs.

usages:

```sh
python -m main -i input.txt -o output.wav -v gb-thomas
```

The generated `output.wav` file will contain the speech synthesized from the
text in `input.txt` using the `gb-thomas` voice. This `output.wav` file can then
be played using any media player that supports WAV files. It is located in the
`outputs` directory of the project.

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
