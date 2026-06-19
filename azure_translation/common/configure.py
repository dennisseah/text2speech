import azure.cognitiveservices.speech as speech_sdk  # type: ignore[import-untyped]
from azure.identity import DefaultAzureCredential


def configure_speech_recognizer(
    endpoint: str, voice_name: str | None = None
) -> speech_sdk.SpeechConfig:
    """Configure speech recognizer or synthesizer

    Args:
        endpoint (str): The azure ai services endpoint
        voice_name (str | None, optional): The voice to synthesize. Defaults to None.

    Returns:
        speech_sdk.SpeechConfig: the configured speech config object
    """
    credential = DefaultAzureCredential()

    speech_config = speech_sdk.SpeechConfig(
        token_credential=credential, endpoint=endpoint
    )

    if voice_name is not None:
        speech_config.speech_synthesis_voice_name = voice_name
    return speech_config
