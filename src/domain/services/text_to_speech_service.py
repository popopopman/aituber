from infrastructure.voicevox_synthesizer import VoicevoxSynthesizer

class TextToSpeechService:
    def __init__(self):
        self.synthesizer = VoicevoxSynthesizer()

    def synthesize_and_play(self, text):
        self.synthesizer.synthesize_and_play(text)
