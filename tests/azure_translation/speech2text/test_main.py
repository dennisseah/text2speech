from collections.abc import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_translation.speech2text import main as s2t_main
from azure_translation.speech2text.main import SpeechToText, _recognize_continuous


def _recognized_event(text: str) -> MagicMock:
    evt = MagicMock()
    evt.result.reason = s2t_main.speech_sdk.ResultReason.RecognizedSpeech
    evt.result.text = text
    return evt


def _nomatch_event() -> MagicMock:
    evt = MagicMock()
    evt.result.reason = s2t_main.speech_sdk.ResultReason.NoMatch
    return evt


def _canceled_event(reason, error_details: str = "") -> MagicMock:
    evt = MagicMock()
    evt.cancellation_details.reason = reason
    evt.cancellation_details.error_details = error_details
    return evt


def _make_recognizer(events: list[tuple[str, MagicMock]]) -> MagicMock:
    """Build a mock recognizer that fires the given events on start."""
    recognizer = MagicMock()
    handlers: dict[str, Callable[[MagicMock], None]] = {}

    recognizer.recognized.connect.side_effect = lambda cb: handlers.__setitem__(
        "recognized", cb
    )
    recognizer.canceled.connect.side_effect = lambda cb: handlers.__setitem__(
        "canceled", cb
    )
    recognizer.session_stopped.connect.side_effect = lambda cb: handlers.__setitem__(
        "stopped", cb
    )

    def start() -> None:
        for kind, evt in events:
            handlers[kind](evt)

    recognizer.start_continuous_recognition.side_effect = start
    return recognizer


def test_recognize_continuous_collects_segments():
    recognizer = _make_recognizer(
        [
            ("recognized", _recognized_event("hello")),
            ("recognized", _nomatch_event()),
            ("recognized", _recognized_event("world")),
            ("stopped", MagicMock()),
        ]
    )

    segments, errors = _recognize_continuous(recognizer)

    assert segments == ["hello", "world"]
    assert errors == []
    recognizer.start_continuous_recognition.assert_called_once()
    recognizer.stop_continuous_recognition.assert_called_once()


def test_recognize_continuous_collects_errors():
    recognizer = _make_recognizer(
        [
            (
                "canceled",
                _canceled_event(s2t_main.speech_sdk.CancellationReason.Error, "boom"),
            ),
        ]
    )

    segments, errors = _recognize_continuous(recognizer)

    assert segments == []
    assert errors == ["boom"]


def test_recognize_continuous_ignores_non_error_cancellation():
    recognizer = _make_recognizer(
        [
            (
                "canceled",
                _canceled_event(s2t_main.speech_sdk.CancellationReason.EndOfStream),
            ),
        ]
    )

    segments, errors = _recognize_continuous(recognizer)

    assert segments == []
    assert errors == []


def test_call_success(mocker: MockerFixture):
    mocker.patch.object(s2t_main, "configure_speech_recognizer")

    mocker.patch.object(s2t_main.speech_sdk, "SpeechRecognizer")
    mocker.patch.object(s2t_main.speech_sdk.audio, "AudioConfig")
    mocker.patch.object(
        s2t_main, "_recognize_continuous", return_value=(["hello", "world"], [])
    )

    result = SpeechToText()("audio.wav")

    assert result == "hello world"


def test_call_canceled(mocker: MockerFixture):
    mocker.patch.object(s2t_main, "configure_speech_recognizer")
    mocker.patch.object(s2t_main.speech_sdk, "SpeechRecognizer")
    mocker.patch.object(s2t_main.speech_sdk.audio, "AudioConfig")
    mocker.patch.object(s2t_main, "_recognize_continuous", return_value=([], ["boom"]))

    with pytest.raises(RuntimeError, match="Speech recognition canceled"):
        SpeechToText()("audio.wav")
