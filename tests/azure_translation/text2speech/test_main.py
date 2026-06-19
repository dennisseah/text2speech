from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_translation.text2speech import main as t2s_main
from azure_translation.text2speech.main import TextToSpeech
from azure_translation.text2speech.voices import Voice


def test_convert_success(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "configure_speech_recognizer")
    synthesizer = MagicMock()
    result = MagicMock()
    result.reason = "Completed"
    synthesizer.speak_text_async.return_value.get.return_value = result
    mocker.patch.object(
        t2s_main.speech_sdk, "SpeechSynthesizer", return_value=synthesizer
    )
    mocker.patch.object(t2s_main.speech_sdk.audio, "AudioOutputConfig")

    TextToSpeech()("hello world", output_file="out.wav", voice=Voice.EN_GB_THOMAS)

    synthesizer.speak_text_async.assert_called_once_with("hello world")


def test_convert_no_result(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "configure_speech_recognizer")
    synthesizer = MagicMock()
    synthesizer.speak_text_async.return_value.get.return_value = None
    mocker.patch.object(
        t2s_main.speech_sdk, "SpeechSynthesizer", return_value=synthesizer
    )
    mocker.patch.object(t2s_main.speech_sdk.audio, "AudioOutputConfig")

    with pytest.raises(RuntimeError, match="No result returned"):
        TextToSpeech()("hello", output_file="out.wav")


def test_convert_canceled(mocker: MockerFixture):
    mocker.patch.object(t2s_main, "configure_speech_recognizer")
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
        TextToSpeech()("hello", output_file="out.wav")
