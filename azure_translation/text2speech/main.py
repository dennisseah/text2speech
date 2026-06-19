import azure.cognitiveservices.speech as speech_sdk  # type: ignore[import-untyped]
from pydantic_settings import BaseSettings, SettingsConfigDict

from azure_translation.common.configure import configure_speech_recognizer
from azure_translation.text2speech.voices import Voice


class TextToSpeechSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    speech_endpoint: str


class TextToSpeech:
    """Callable that converts text to speech and saves it to an audio file."""

    def __call__(
        self, text: str, output_file: str, voice: Voice = Voice.EN_GB_THOMAS
    ) -> None:
        """Convert text to speech and save it to an audio file.

        Args:
            text (str): text to convert to speech
            output_file (str): output file for the generated audio.
            voice (Voice, optional): voice to be used. Defaults to
                Voice.EN_GB_THOMAS.
        """
        speech_synthesizer = speech_sdk.SpeechSynthesizer(
            speech_config=configure_speech_recognizer(
                TextToSpeechSetting().speech_endpoint,  # type: ignore[call-arg]
                voice,
            ),
            audio_config=speech_sdk.audio.AudioOutputConfig(filename=output_file),
        )

        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result is None:
            raise RuntimeError("Speech synthesis failed: No result returned")

        if speech_synthesis_result.reason == speech_sdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            raise RuntimeError(
                "Speech synthesis canceled: {}".format(cancellation_details.reason)
            )
