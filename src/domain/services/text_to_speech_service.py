from infrastructure.voicevox_synthesizer import VoiceVoxSynthesizer

class TextToSpeechService:
    def __init__(self):
        self.synthesizer = VoiceVoxSynthesizer()

    def synthesize_and_play(self, text):
        self.synthesizer.synthesize(text)
        self.synthesizer.play()
