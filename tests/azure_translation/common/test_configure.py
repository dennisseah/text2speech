from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from azure_translation.common import configure as configure_mod
from azure_translation.common.configure import configure_speech_recognizer


def test_configure_speech_recognizer(mocker: MockerFixture):
    mocker.patch.object(configure_mod, "DefaultAzureCredential", return_value="cred")
    speech_config = MagicMock()
    speech_config_cls = mocker.patch.object(
        configure_mod.speech_sdk, "SpeechConfig", return_value=speech_config
    )

    result = configure_speech_recognizer(
        endpoint="https://test-resource.cognitiveservices.azure.com/"
    )

    speech_config_cls.assert_called_once_with(
        token_credential="cred",
        endpoint="https://test-resource.cognitiveservices.azure.com/",
    )
    assert result is speech_config


def test_configure_speech_recognizer_with_voice(mocker: MockerFixture):
    mocker.patch.object(configure_mod, "DefaultAzureCredential", return_value="cred")
    speech_config = MagicMock()
    mocker.patch.object(
        configure_mod.speech_sdk, "SpeechConfig", return_value=speech_config
    )

    result = configure_speech_recognizer(
        endpoint="https://test-resource.cognitiveservices.azure.com/",
        voice_name="en-US-JennyNeural",
    )

    assert result is speech_config
    assert speech_config.speech_synthesis_voice_name == "en-US-JennyNeural"
