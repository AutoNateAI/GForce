from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService

class CharacterScene(VoiceoverScene):
    def __init__(self, character_class, scale=0.8, position=ORIGIN, voice="alloy", intro_text="", speech_text=""):
        super().__init__()
        self.character_class = character_class
        self.scale = scale
        self.position = position
        self.voice = voice
        self.intro_text = intro_text
        self.speech_text = speech_text
        self.character = None
    
    def construct(self):
        # Initialize character
        self.character = self.character_class(scale_factor=self.scale)
        self.character.move_to(self.position)
        
        # Initialize voice
        self.set_speech_service(OpenAIService(voice=self.voice, model="tts-1"))
        
        # Intro animation with narrator voice
        with self.voiceover(text=self.intro_text):
            self.play(
                FadeIn(self.character, shift=UP)
            )
        
        # Character speaks
        with self.voiceover(text=self.speech_text):
            self.play(
                Succession(*[
                    self.character.talk()
                    for _ in range(4)
                ], run_time=0.8)
            )
        
        # Add blink for personality
        self.play(self.character.blink(), run_time=0.3)
    
    def get_character(self):
        return self.character
