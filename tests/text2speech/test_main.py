from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from text2speech import main as t2s_main
from text2speech.main import _configure_speech_synthesizer, convert
from text2speech.voices import Voice


def test_configure_speech_synthesizer(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "DefaultAzureCredential", return_value="cred")
    speech_config = MagicMock()
    speech_config_cls = mocker.patch.object(
        t2s_main.speech_sdk, "SpeechConfig", return_value=speech_config
    )

    result = _configure_speech_synthesizer(Voice.EN_US_ERIC)

    speech_config_cls.assert_called_once_with(
        token_credential="cred",
        endpoint="https://test-resource.cognitiveservices.azure.com/",
    )
    assert speech_config.speech_synthesis_voice_name == Voice.EN_US_ERIC
    assert result is speech_config


def test_convert_success(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "_configure_speech_synthesizer")
    synthesizer = MagicMock()
    result = MagicMock()
    result.reason = "Completed"
    synthesizer.speak_text_async.return_value.get.return_value = result
    mocker.patch.object(
        t2s_main.speech_sdk, "SpeechSynthesizer", return_value=synthesizer
    )
    mocker.patch.object(t2s_main.speech_sdk.audio, "AudioOutputConfig")

    convert("hello world", output_file="out.wav", voice=Voice.EN_GB_THOMAS)

    synthesizer.speak_text_async.assert_called_once_with("hello world")


def test_convert_no_result(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "_configure_speech_synthesizer")
    synthesizer = MagicMock()
    synthesizer.speak_text_async.return_value.get.return_value = None
    mocker.patch.object(
        t2s_main.speech_sdk, "SpeechSynthesizer", return_value=synthesizer
    )
    mocker.patch.object(t2s_main.speech_sdk.audio, "AudioOutputConfig")

    with pytest.raises(RuntimeError, match="No result returned"):
        convert("hello", output_file="out.wav")


def test_convert_canceled(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "_configure_speech_synthesizer")
    synthesizer = MagicMock()
    result = MagicMock()
    result.reason = t2s_main.speech_sdk.ResultReason.Canceled
    result.cancellation_details.reason = "boom"
    synthesizer.speak_text_async.return_value.get.return_value = result
    mocker.patch.object(
        t2s_main.speech_sdk, "SpeechSynthesizer", return_value=synthesizer
    )
    mocker.patch.object(t2s_main.speech_sdk.audio, "AudioOutputConfig")

    with pytest.raises(RuntimeError, match="Speech synthesis canceled"):
        convert("hello", output_file="out.wav")
