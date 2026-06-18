from text2speech.voices import Voice


def test_voice_values():
    assert Voice.EN_GB_THOMAS == "en-GB-ThomasNeural"
    assert Voice.EN_SG_WAYNE == "en-SG-WayneNeural"
    assert Voice.EN_US_MONICA == "en-US-MonicaNeural"
    assert Voice.EN_US_ERIC == "en-US-EricNeural"
    assert Voice.EN_IN_NEERJA == "en-IN-NeerjaNeural"


def test_voice_is_str():
    assert isinstance(Voice.EN_GB_THOMAS, str)


def test_voice_members_count():
    assert len(Voice) == 5
