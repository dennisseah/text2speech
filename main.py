import argparse

from text2speech.main import convert
from text2speech.voices import Voice

VOICE_CHOICES = {
    "gb-thomas": Voice.EN_GB_THOMAS,
    "sg-wayne": Voice.EN_SG_WAYNE,
    "us-monica": Voice.EN_US_MONICA,
    "us-eric": Voice.EN_US_ERIC,
    "in-neerja": Voice.EN_IN_NEERJA,
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

    convert(text, output_file=args.output, voice=VOICE_CHOICES[args.voice])


if __name__ == "__main__":
    main()
