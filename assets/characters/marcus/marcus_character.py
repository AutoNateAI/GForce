from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

class Marcus(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        
        # Create the face (center circle) - green body with thicker darker border
        face = Circle(
            radius=0.5,
            fill_color="#4CAF50",  # Updated green fill
            fill_opacity=1,
            stroke_color="#2E7D32",  # Updated green stroke
            stroke_width=6  # Thicker border
        )
        
        # Create ears (protons) - centered on face edge
        left_ear = Circle(
            radius=0.08,
            fill_color="#7B1FA2",  # Purple
            fill_opacity=1,
            stroke_width=0
        ).move_to(face.get_center() + LEFT * 0.5)  # Exactly on edge (radius is 0.5)
        
        right_ear = Circle(
            radius=0.08,
            fill_color="#7B1FA2",  # Purple
            fill_opacity=1,
            stroke_width=0
        ).move_to(face.get_center() + RIGHT * 0.5)  # Exactly on edge (radius is 0.5)
        
        # Create eyes - blue stroke with lighter blue fill
        eye_radius = 0.12
        eye_style = {"stroke_color": "#1976D2", "stroke_width": 8, "fill_color": "#BBDEFB", "fill_opacity": 1}  # Light blue fill
        left_eye = Circle(radius=eye_radius, **eye_style).move_to(face.get_center() + LEFT * 0.15 + UP * 0.05)
        right_eye = Circle(radius=eye_radius, **eye_style).move_to(face.get_center() + RIGHT * 0.15 + UP * 0.05)
        
        # Create smile - purple, thicker stroke and more curved for happiness
        smile = ArcBetweenPoints(
            face.get_center() + LEFT * 0.25 + DOWN * 0.25,  # Wider and lower
            face.get_center() + RIGHT * 0.25 + DOWN * 0.25,  # Wider and lower
            angle=PI/3,  # Positive angle for upward curve (smile)
            stroke_width=6,  # Thick
            color="#7B1FA2"  # Purple
        )
        
        # Create electron rings (orbits) with electrons
        outer_ring = VGroup()
        inner_ring = VGroup()
        
        # Both rings purple now
        ring_color = "#7B1FA2"  # Purple
        
        # Outer ring (purple)
        outer_orbit = Ellipse(
            width=2.6,
            height=1.0,
            stroke_color=ring_color,
            stroke_width=3
        )
        
        # Add electrons to outer ring
        outer_electrons = VGroup(*[
            Dot(
                point=outer_orbit.point_from_proportion(i/3),
                radius=0.05,
                color=ring_color,
                fill_opacity=1
            )
            for i in range(3)
        ])
        outer_ring.add(outer_orbit, outer_electrons)
        
        # Inner ring (blue)
        inner_orbit = Ellipse(
            width=2.2,
            height=0.9,
            stroke_color="#1976D2",  # Updated blue
            stroke_width=3
        )
        
        # Add electrons to inner ring
        inner_electrons = VGroup(*[
            Dot(
                point=inner_orbit.point_from_proportion(i/2),
                radius=0.05,
                color="#1976D2",  # Updated blue
                fill_opacity=1
            )
            for i in range(2)
        ])
        inner_ring.add(inner_orbit, inner_electrons)
        
        # Rotate rings to match SVG
        outer_ring.rotate(PI/6)
        inner_ring.rotate(-PI/6)
        
        # Add everything to the VGroup
        self.add(face, left_ear, right_ear, outer_ring, inner_ring, left_eye, right_eye, smile)
        
        # Store references for animations
        self.face = face
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.smile = smile
        self.outer_ring = outer_ring
        self.inner_ring = inner_ring
        self.outer_electrons = outer_electrons
        self.inner_electrons = inner_electrons
        self.left_ear = left_ear
        self.right_ear = right_ear
        self.orbitals = [outer_ring, inner_ring]
        
        # Apply scale
        self.scale(scale_factor)
    
    def blink(self):
        """Create a blinking animation."""
        # Create thin lines with blue stroke for blinking
        return AnimationGroup(
            Transform(self.left_eye, 
                     Line(self.left_eye.get_center() + LEFT * 0.08,
                          self.left_eye.get_center() + RIGHT * 0.08,
                          stroke_width=8,  # Thicker
                          color="#1976D2")),  # Updated blue
            Transform(self.right_eye,
                     Line(self.right_eye.get_center() + LEFT * 0.08,
                          self.right_eye.get_center() + RIGHT * 0.08,
                          stroke_width=8,  # Thicker
                          color="#1976D2")),  # Updated blue
            rate_func=there_and_back
        )
    
    def talk(self):
        """Create a talking animation by morphing the smile."""
        # Create a slight curve for talking while maintaining happiness
        talking_mouth = ArcBetweenPoints(
            self.smile.get_start(),
            self.smile.get_end(),
            angle=PI/4,  # Positive angle for upward curve (smile)
            stroke_width=6,
            color="#7B1FA2"  # Purple
        )
        return Transform(self.smile, talking_mouth, rate_func=there_and_back)
    
    def animate_orbitals(self):
        """Create a spinning animation for the electron rings."""
        return AnimationGroup(
            Rotating(self.outer_ring, radians=PI/2, about_point=self.outer_ring.get_center()),
            Rotating(self.inner_ring, radians=-PI/2, about_point=self.inner_ring.get_center()),
            run_time=3,
            rate_func=linear
        )

    def spin_rings(self):
        """Create a spinning animation for the electron rings."""
        return AnimationGroup(
            Rotate(self.outer_ring, angle=PI/4, rate_func=linear),
            Rotate(self.inner_ring, angle=-PI/4, rate_func=linear)
        )

class MarcusDemo(VoiceoverScene):
    def setup(self):
        super().setup()
        # Set up the speech service
        self.set_speech_service(
            OpenAIService(
                api_key=os.getenv("OPENAI_API_KEY"),
                voice="onyx"  # Using a different voice for Marcus
            )
        )
    
    def construct(self):
        # Create Marcus and position in center
        marcus = Marcus(scale_factor=1.5)
        marcus.move_to(ORIGIN)
        self.add(marcus)
        
        # Create text elements
        name_text = Text("Marcus", font_size=48, color=BLUE)
        subtitle_text = Text("Science Explorer", font_size=32, color=PURPLE)
        
        # Position texts below Marcus
        name_text.next_to(marcus, DOWN, buff=0.5)
        subtitle_text.next_to(name_text, DOWN, buff=0.2)
        
        # Add the voiceover with synchronized animations
        with self.voiceover(text="Hello! I'm Marcus, and I love exploring the wonders of science!") as tracker:
            # Create a continuous talking animation for the duration of the speech
            talk_cycle = 0.4
            wait_time = 0.2
            
            # Combine talking and ring spinning animations
            talk_anim = Succession(
                *[
                    Succession(
                        AnimationGroup(
                            marcus.talk(),
                            marcus.spin_rings(),
                        ),
                        Wait(wait_time)
                    )
                    for _ in range(int(tracker.duration / (talk_cycle + wait_time)))
                ]
            )
            
            # Play the talking animation and write in texts
            self.play(
                talk_anim,
                Write(name_text),
                Write(subtitle_text, lag_ratio=0.5),
                run_time=tracker.duration
            )
        
        # Add a blink at the end of speaking
        self.play(
            marcus.blink(),
            run_time=0.3
        )
        
        # Small pause before exit
        self.wait(0.2)
        
        # Create a path for smooth exit
        start_pos = marcus.get_center()
        end_pos = RIGHT * 12 + UP * 0.5
        
        def update_marcus(mob, alpha):
            # Move Marcus along path with sine wave
            t = alpha * 3 * PI
            current_x = interpolate(start_pos[0], end_pos[0], alpha)
            current_y = interpolate(start_pos[1], end_pos[1], alpha) + 0.2 * np.sin(t)
            mob.move_to([current_x, current_y, 0])
        
        # Exit animations
        self.play(
            UpdateFromAlphaFunc(marcus, update_marcus),
            name_text.animate.shift(DOWN * 6),
            subtitle_text.animate.shift(DOWN * 6),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine
        )
