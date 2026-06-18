import threading

import azure.cognitiveservices.speech as speech_sdk  # type: ignore[import-untyped]
from azure.identity import DefaultAzureCredential
from pydantic_settings import BaseSettings, SettingsConfigDict


class SpeechToTextSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    speech_endpoint: str


def _configure_speech_recognizer() -> speech_sdk.SpeechConfig:
    credential = DefaultAzureCredential()
    endpoint = SpeechToTextSetting().speech_endpoint  # type: ignore[call-arg]

    speech_config = speech_sdk.SpeechConfig(
        token_credential=credential, endpoint=endpoint
    )
    return speech_config


def _recognize_continuous(
    speech_recognizer: speech_sdk.SpeechRecognizer,
) -> tuple[list[str], list[str]]:
    """Run continuous recognition until the end of the audio.

    Args:
        speech_recognizer (speech_sdk.SpeechRecognizer): the recognizer to run.

    Returns:
        tuple[list[str], list[str]]: the recognized text segments and any
            error details collected during recognition.
    """
    segments: list[str] = []
    errors: list[str] = []
    done = threading.Event()

    def on_recognized(evt: speech_sdk.SpeechRecognitionEventArgs) -> None:
        if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            segments.append(evt.result.text)

    def on_canceled(evt: speech_sdk.SpeechRecognitionCanceledEventArgs) -> None:
        details = evt.cancellation_details
        if details.reason == speech_sdk.CancellationReason.Error:
            errors.append(details.error_details)
        done.set()

    def on_stopped(evt: speech_sdk.SessionEventArgs) -> None:
        done.set()

    speech_recognizer.recognized.connect(on_recognized)
    speech_recognizer.canceled.connect(on_canceled)
    speech_recognizer.session_stopped.connect(on_stopped)

    speech_recognizer.start_continuous_recognition()
    done.wait()
    speech_recognizer.stop_continuous_recognition()

    return segments, errors


class SpeechToText:
    """Callable that converts a WAV audio file to text."""

    def __call__(self, audio_file: str) -> str:
        """Convert speech in a WAV file to text.

        Recognizes the entire audio file using continuous recognition so that
        utterances after the first pause are not dropped.

        Args:
            audio_file (str): path to the input WAV audio file.

        Returns:
            str: the recognized text.
        """
        speech_recognizer = speech_sdk.SpeechRecognizer(
            speech_config=_configure_speech_recognizer(),
            audio_config=speech_sdk.audio.AudioConfig(filename=audio_file),
        )

        segments, errors = _recognize_continuous(speech_recognizer)

        if errors:
            raise RuntimeError("Speech recognition canceled: {}".format(errors[0]))

        return " ".join(segments)
