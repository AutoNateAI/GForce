from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

class Maya(VGroup):
    # Colors from the SVG
    MAYA_PURPLE = "#9C27B0"
    MAYA_GOLD = "#FFD700"
    
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        
        # Store scale factor for animations
        self.scale_factor = scale_factor
        
        # Create the hat shape using a smoother polygon with more points
        hat_points = []
        # Left side
        hat_points.extend([
            [-0.6, 0, 0],      # Base left
            [-0.55, 0.3, 0],   # Smooth corner
            [-0.5, 0.6, 0],    # Mid left
            [-0.3, 1.0, 0],    # Upper left
            [-0.15, 1.2, 0],   # Near top left
        ])
        # Top
        hat_points.extend([
            [0, 1.3, 0],       # Top point
        ])
        # Right side (mirror of left)
        hat_points.extend([
            [0.15, 1.2, 0],    # Near top right
            [0.3, 1.0, 0],     # Upper right
            [0.5, 0.6, 0],     # Mid right
            [0.55, 0.3, 0],    # Smooth corner
            [0.6, 0, 0],       # Base right
        ])
        
        hat = Polygon(
            *[np.array(p) * scale_factor for p in hat_points],
            fill_color=self.MAYA_PURPLE,
            fill_opacity=1,
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * scale_factor
        )
        
        # Create the three dots on the hat (now as circles with purple fill)
        dots = VGroup()
        dot_positions_and_sizes = [
            ([-0.45, 0.6, 0], 0.12),    # Left eye - moved inward but still protrudes
            ([0, 1.3, 0], 0.18),        # Third eye - made even larger
            ([0.45, 0.6, 0], 0.12)      # Right eye - moved inward but still protrudes
        ]
        for pos, radius in dot_positions_and_sizes:
            dot = Circle(
                radius=radius * scale_factor,
                stroke_color=self.MAYA_GOLD,
                stroke_width=8 * scale_factor,
                fill_color=self.MAYA_PURPLE,
                fill_opacity=1
            ).move_to(np.array(pos) * scale_factor)
            dots.add(dot)
        
        # Create the smile
        smile = ArcBetweenPoints(
            start=np.array([-0.2, 0.3, 0]) * scale_factor,
            end=np.array([0.2, 0.3, 0]) * scale_factor,
            angle=TAU/8,
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * scale_factor
        )
        
        # Create a more mathematical wave (derivative-like) using multiple bezier curves
        wave_group = VGroup()
        
        # Create the carpet area (filled region under the wave)
        carpet_points = [
            [-0.8, 0, 0],       # Start at wave start
            [-0.4, -0.15, 0],   # Follow wave curve
            [0, 0, 0],          # Middle point
            [0.4, -0.15, 0],    # Follow wave curve
            [0.6, 0, 0],        # Wave end
            [0.8, -0.15, 0],    # Curl end
            [0.8, -0.25, 0],    # Bottom right
            [-0.8, -0.25, 0],   # Bottom left
        ]
        carpet = Polygon(
            *[np.array(p) * scale_factor for p in carpet_points],
            fill_color="#886600",  # Darker gold for the carpet
            fill_opacity=0.9,
            stroke_width=0
        )
        
        # First wave segment (smoother derivative-like curve)
        wave1_points = [
            [-0.8, 0, 0],       # Start
            [-0.4, -0.15, 0],   # Control 1 - smoother dip
            [-0.2, 0.1, 0],     # Control 2 - gentler rise
            [0, 0, 0],          # End
        ]
        wave1 = CubicBezier(
            *[np.array(p) * scale_factor for p in wave1_points],
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * scale_factor
        )
        
        # Second wave segment
        wave2_points = [
            [0, 0, 0],          # Start
            [0.2, -0.1, 0],     # Control 1 - gentler dip
            [0.4, 0.1, 0],      # Control 2 - gentler rise
            [0.6, 0, 0],        # End
        ]
        wave2 = CubicBezier(
            *[np.array(p) * scale_factor for p in wave2_points],
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * scale_factor
        )
        
        # Final curl (gentler curve)
        curl = ArcBetweenPoints(
            start=np.array([0.6, 0, 0]) * scale_factor,
            end=np.array([0.8, -0.15, 0]) * scale_factor,
            angle=-TAU/4,  # Gentler angle for smoother curl
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * scale_factor
        )
        
        wave_group.add(carpet, wave1, wave2, curl)
        
        # Combine all elements
        self.add(hat, dots, smile, wave_group)
        
        # Store elements for animations
        self.dots = dots
        self.smile = smile
        self.wave_group = wave_group
        
    def bounce(self):
        """Animation for a playful bounce"""
        return self.animate.shift(UP * 0.3).shift(DOWN * 0.3)
    
    def wave_animation(self):
        """Animation for waving the base"""
        wave_group = self[3]  # Wave group is the fourth element
        return AnimationGroup(
            wave_group.animate.shift(UP * 0.1),
            wave_group.animate.shift(DOWN * 0.1),
            rate_func=there_and_back,
            run_time=1
        )
    
    def sparkle(self):
        """Animation for sparkling dots"""
        dots = self[1]  # Dots group is the second element
        animations = []
        for i, dot in enumerate(dots):
            animations.append(
                Succession(
                    dot.animate.scale(1.2),
                    dot.animate.scale(1/1.2),
                    run_time=0.3,
                    rate_func=smooth,
                    lag_ratio=0.1
                )
            )
        return AnimationGroup(*animations, lag_ratio=0.2)
    
    def blink(self):
        """Animation for Maya blinking her eyes"""
        # Only animate the side eyes (first and third dots)
        left_eye = self.dots[0]
        right_eye = self.dots[2]
        
        # Create slightly squished eyes for the blink
        blink_anim = AnimationGroup(
            Transform(
                left_eye,
                Line(
                    start=left_eye.get_center() + np.array([-0.06, 0.02, 0]) * self.scale_factor,
                    end=left_eye.get_center() + np.array([0.06, -0.02, 0]) * self.scale_factor,
                    stroke_color=self.MAYA_GOLD,
                    stroke_width=8 * self.scale_factor
                )
            ),
            Transform(
                right_eye,
                Line(
                    start=right_eye.get_center() + np.array([-0.06, 0.02, 0]) * self.scale_factor,
                    end=right_eye.get_center() + np.array([0.06, -0.02, 0]) * self.scale_factor,
                    stroke_color=self.MAYA_GOLD,
                    stroke_width=8 * self.scale_factor
                )
            ),
            lag_ratio=0
        )
        
        # Quick blink animation sequence
        return Succession(
            blink_anim,
            Wait(0.08),  # Hold closed position briefly
            AnimationGroup(
                Transform(left_eye, left_eye.copy()),
                Transform(right_eye, right_eye.copy()),
                lag_ratio=0
            )
        )
    
    def talk(self):
        """Animation for Maya talking"""
        original_smile = self.smile.copy()
        
        # Create a more dynamic open mouth
        open_mouth = ArcBetweenPoints(
            start=self.smile.get_start(),
            end=self.smile.get_end(),
            angle=TAU/10,  # Slightly larger angle for open mouth
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * self.scale_factor
        ).shift(UP * 0.08 * self.scale_factor)  # Shift up more for better movement
        
        # Create a wider smile for variation
        wide_smile = ArcBetweenPoints(
            start=self.smile.get_start() + np.array([-0.05, 0, 0]) * self.scale_factor,
            end=self.smile.get_end() + np.array([0.05, 0, 0]) * self.scale_factor,
            angle=TAU/8,
            stroke_color=self.MAYA_GOLD,
            stroke_width=6 * self.scale_factor
        )
        
        # More dynamic talk animation sequence
        return Succession(
            Transform(self.smile, open_mouth),
            Wait(0.15),
            Transform(self.smile, wide_smile),
            Wait(0.15),
            Transform(self.smile, original_smile),
            Wait(0.1)
        )

class MayaDemo(VoiceoverScene):
    def setup(self):
        super().setup()
        # Set up the speech service
        self.set_speech_service(
            OpenAIService(
                api_key=os.getenv("OPENAI_API_KEY"),
                voice="nova"
            )
        )
    
    def construct(self):
        # Create Maya and position in center
        maya = Maya(scale_factor=1.5)
        maya.move_to(ORIGIN)
        self.add(maya)
        
        # Create text elements
        name_text = Text("Maya", font_size=48, color=PURPLE_A)
        subtitle_text = Text("Math Wizard", font_size=32, color=GOLD)
        
        # Position texts below Maya
        name_text.next_to(maya, DOWN, buff=0.5)
        subtitle_text.next_to(name_text, DOWN, buff=0.2)
        
        # Add the voiceover with synchronized animations
        with self.voiceover(text="Hi, I am Maya, your math wizard! Let's explore math together.") as tracker:
            # Create a continuous talking animation for the duration of the speech
            talk_cycle = 0.4  # Slower mouth movement
            wait_time = 0.2   # Longer pause between movements
            
            talk_anim = Succession(
                *[
                    Succession(
                        maya.talk(),
                        Wait(wait_time)
                    )
                    for _ in range(int(tracker.duration / (talk_cycle + wait_time)))
                ]
            )
            
            # Play the talking animation and write in texts
            self.play(
                talk_anim,
                Write(name_text),
                Write(subtitle_text, lag_ratio=0.5),  # Slightly delayed start
                run_time=tracker.duration
            )
        
        # Add a blink at the end of speaking
        self.play(
            maya.blink(),
            run_time=0.3
        )
        
        # Small pause before exit
        self.wait(0.2)
        
        # Create a path for smooth exit
        start_pos = maya.get_center()
        end_pos = RIGHT * 12 + UP * 0.5  # Move further right to ensure complete exit
        
        def update_maya(mob, alpha):
            # Move Maya along path with sine wave
            t = alpha * 3 * PI  # Faster wave
            current_x = interpolate(start_pos[0], end_pos[0], alpha)
            current_y = interpolate(start_pos[1], end_pos[1], alpha) + 0.2 * np.sin(t)
            mob.move_to([current_x, current_y, 0])
        
        # Exit animations
        self.play(
            UpdateFromAlphaFunc(maya, update_maya),
            name_text.animate.shift(DOWN * 6),
            subtitle_text.animate.shift(DOWN * 6),
            run_time=1.2,  # Faster exit
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Hold the final pose
        self.wait(0.3)

class MayaIntroductionDemo(Scene):
    def construct(self):
        # Create Maya with a larger scale
        maya = Maya(scale_factor=1.5)
        self.add(maya)
        
        # Showcase animations
        self.wait(0.5)
        
        # Demonstrate natural blinking
        self.play(maya.blink())
        self.wait(0.4)
        
        # Show talking with some blinks
        self.play(maya.talk())
        self.wait(0.2)
        self.play(maya.blink())
        self.wait(0.1)
        self.play(maya.talk())
        self.play(maya.talk())
        
        # Final expression
        self.wait(0.3)
        self.play(maya.blink())
        
        self.wait(0.5)

if __name__ == "__main__":
    # Configure for standard format
    config.frame_height = 9
    config.frame_width = 16
    config.pixel_height = 1080
    
    # Render the demo
    scene = MayaDemo()
    scene.render()
