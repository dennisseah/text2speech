import argparse
from pathlib import Path

from azure_translation.speech2text.main import SpeechToText


def main():
    parser = argparse.ArgumentParser(description="Convert text from a file to speech.")
    parser.add_argument("-i", "--input", help="Path to the input audio file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.txt",
        help="Path to the output text file (default: output.txt).",
    )

    args = parser.parse_args()

    path = Path(args.input)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    speech_to_text = SpeechToText()
    txt = speech_to_text(str(path))

    with open(output_dir / args.output, "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    main()
