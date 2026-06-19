import argparse
from pathlib import Path

from azure_translation.text2speech.main import TextToSpeech
from azure_translation.text2speech.voices import Voice

VOICE_CHOICES = {
    voice.name.removeprefix("EN_").lower().replace("_", "-"): voice for voice in Voice
}


def main():
    parser = argparse.ArgumentParser(description="Convert text from a file to speech.")
    parser.add_argument("-i", "--input", help="Path to the input text file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.wav",
        help="Path to the output audio file (default: output.wav).",
    )
    parser.add_argument(
        "-c",
        "--voice",
        default="gb-thomas",
        choices=list(VOICE_CHOICES),
        help="Voice to use for speech synthesis (default: gb-thomas).",
    )

    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    text_to_speech = TextToSpeech()
    text_to_speech(
        text,
        output_file=str(output_dir / args.output),
        voice=VOICE_CHOICES[args.voice],
    )


if __name__ == "__main__":
    main()
