from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from manim.utils.rate_functions import ease_in_cubic, ease_out_cubic, smooth, linear, there_and_back
import sys
import os
import numpy as np
from PIL import Image

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.characters.marcus.marcus_character import Marcus
from assets.characters.maya.maya_character import Maya
from assets.characters.sage.sage_character import Sage

class GeniusForceIntro(VoiceoverScene):
    def create_concept_text(self, text, color=BLUE):
        return Text(text, font_size=48, color=color, weight=BOLD)
    
    def create_background(self):
        """Create a dark background."""
        background = Rectangle(
            width=16,
            height=9,
            fill_color="#1A1B2E",  # Dark blue-gray
            fill_opacity=0.5,  # Make it semi-transparent
            stroke_width=0
        )
        return background

    def construct(self):
        # Set scene background color
        self.camera.background_color = "#1A1B2E"

        # Set up narrator voice (Ash)
        self.set_speech_service(OpenAIService(voice="alloy", model="tts-1"))
        
        # Create and display the Genius Force logo
        logo = ImageMobject(
            "assets/logos/png/genius_force_official_500px.png"
        ).set_height(4)
        logo.scale(0.1)  # Start very small
        logo.move_to(ORIGIN)
        
        # Add to scene
        self.add(logo)
        
        # Epic intro
        with self.voiceover(text="In a world where learning meets adventure..."):
            # Animate the logo entrance with a growth effect
            self.play(
                logo.animate.scale(15),  # Scale from small to full size
                run_time=2,
                rate_func=smooth
            )
            self.wait(0.5)
            self.play(
                logo.animate.scale(0.5).to_edge(UP, buff=0.2),
                run_time=1
            )
        
        # Marcus Introduction
        marcus = Marcus(scale_factor=0.8)
        marcus.move_to(LEFT * 4 + DOWN * 1)  # Moved down more
        
        with self.voiceover(text="Meet Marcus, our energy expert! He'll show us how light, radio waves, and all kinds of invisible energy work in our everyday lives!"):
            self.play(FadeIn(marcus, shift=LEFT))
            # Start continuous orbital animation
            self.play(
                marcus.animate_orbitals(),
                run_time=1,
                rate_func=linear
            )
        
        # Switch to Marcus's voice
        self.set_speech_service(OpenAIService(voice="onyx", model="tts-1"))
        with self.voiceover(text="Hi everyone! I'm Marcus, and I'll help you discover the amazing invisible forces that power our world, from the radio waves in your phone to the light that helps us see!") as tracker:
            # Create talking animation with continuous orbital rotation
            n_cycles = int(tracker.duration / 0.4)
            for _ in range(n_cycles):
                self.play(
                    AnimationGroup(
                        marcus.talk(),
                        marcus.animate_orbitals(),
                        lag_ratio=0
                    ),
                    run_time=0.4
                )
        
        # Maya Introduction
        maya = Maya(scale_factor=0.8)
        maya.move_to(ORIGIN + DOWN * 1)  # Moved down more
        
        # Switch back to narrator
        self.set_speech_service(OpenAIService(voice="alloy", model="tts-1"))
        with self.voiceover(text="Next is Maya, our math explorer! She makes numbers fun and shows us how they help us understand the world of energy and waves!"):
            self.play(FadeIn(maya, shift=UP))
        
        # Switch to Maya's voice
        self.set_speech_service(OpenAIService(voice="nova", model="tts-1"))
        with self.voiceover(text="Hello! I'm Maya, and together we'll see how math helps us measure and predict amazing things, like how radio signals travel or how rainbows form!") as tracker:
            self.play(
                Succession(*[
                    maya.talk()
                    for _ in range(int(tracker.duration / 0.4))
                ], run_time=tracker.duration)
            )
        
        # Sage Introduction
        sage = Sage(scale_factor=0.8)
        sage.move_to(RIGHT * 4 + DOWN * 1)  # Moved down more
        shadow = sage.get_shadow()
        shadow.next_to(sage, DOWN, buff=0.1)
        
        # Switch back to narrator
        self.set_speech_service(OpenAIService(voice="alloy", model="tts-1"))
        with self.voiceover(text="And finally, meet Sage, our tech wizard! He'll help us build amazing gadgets and understand how our favorite devices work!"):
            self.play(FadeIn(sage, shift=RIGHT), FadeIn(shadow))
        
        # Switch to Sage's voice
        self.set_speech_service(OpenAIService(voice="echo", model="tts-1"))
        with self.voiceover(text="Greetings! I'm Sage, and I'll show you how to create cool projects using technology, from building simple circuits to programming your own games!") as tracker:
            # Create smoother hovering animation for Sage
            hover_time = 1.2  # Longer duration for smoother bounce
            n_cycles = int(tracker.duration / hover_time)
            
            for i in range(n_cycles):
                # Up movement with ease out
                self.play(
                    AnimationGroup(
                        sage.talk(),
                        AnimationGroup(
                            sage.animate.shift(UP * 0.15),
                            shadow.animate.scale(0.9),
                            rate_func=ease_out_cubic  # Smooth start, slower end
                        ),
                        run_time=hover_time/2
                    )
                )
                # Down movement with ease in
                self.play(
                    AnimationGroup(
                        sage.talk(),
                        AnimationGroup(
                            sage.animate.shift(DOWN * 0.15),
                            shadow.animate.scale(1.1),
                            rate_func=ease_in_cubic  # Slower start, smooth end
                        ),
                        run_time=hover_time/2
                    )
                )
        
        # Switch back to narrator for finale
        self.set_speech_service(OpenAIService(voice="alloy", model="tts-1"))
        
        # Scale down characters for better visibility of concept words
        self.play(
            AnimationGroup(
                marcus.animate.scale(0.7),
                maya.animate.scale(0.7),
                sage.animate.scale(0.7),
                shadow.animate.scale(0.7),
                run_time=1
            )
        )
        
        # Final group shot
        with self.voiceover(text="Together, they are the GENIUS FORCE! Join them on their incredible journey of discovery!"):
            # Fade out characters
            self.play(
                FadeOut(marcus),
                FadeOut(maya),
                FadeOut(sage),
                FadeOut(shadow),
                run_time=1
            )
            
            # Move logo back to center and scale up, but position it higher
            self.play(
                logo.animate.scale(2).move_to(UP * 1.5),  # Move logo higher
                run_time=1.5,
                rate_func=smooth
            )
            
            # Create and animate concept words
            concepts = VGroup(
                self.create_concept_text("Science", BLUE),
                self.create_concept_text("Technology", GREEN),
                self.create_concept_text("Math", RED),
                self.create_concept_text("Energy", YELLOW)
            ).arrange(RIGHT, buff=1.2)  # Increased spacing between words
            concepts.scale(0.8)  # Made text larger
            concepts.move_to(DOWN * 2)  # Move concepts lower for more separation
            
            # Animate concepts appearing with glowing effect
            for concept in concepts:
                self.play(
                    FadeIn(concept, scale=1.5),
                    concept.animate.set_opacity(1),  # Full opacity
                    run_time=0.3
                )
            
            # Hold the final frame
            self.wait(1)
            
            # Fade out everything
            self.play(
                *[FadeOut(mob) for mob in self.mobjects],
                run_time=1
            )
