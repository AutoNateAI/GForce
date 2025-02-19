from manim import *
import numpy as np

class Nova(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        
        # Colors from the main configuration
        NOVA_ORANGE = "#FFA500"  # Changed to orange to match SVG
        EYE_COLOR = "#FFFF00"    # Bright yellow for the eyes
        
        # Create the main circular head
        head = Circle(
            radius=1 * scale_factor,
            fill_color=NOVA_ORANGE,
            fill_opacity=1,
            stroke_color=NOVA_ORANGE,
            stroke_width=2
        )
        
        # Create eyes (bright yellow circles)
        eye_radius = 0.15 * scale_factor
        left_eye = Circle(
            radius=eye_radius,
            fill_color=EYE_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.3 * scale_factor)
        
        right_eye = Circle(
            radius=eye_radius,
            fill_color=EYE_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.3 * scale_factor)
        
        # Create a simple smile
        smile = ArcBetweenPoints(
            start=LEFT * 0.3 * scale_factor + DOWN * 0.2 * scale_factor,
            end=RIGHT * 0.3 * scale_factor + DOWN * 0.2 * scale_factor,
            angle=TAU/8,
            stroke_color=EYE_COLOR,
            stroke_width=3
        )
        
        # Create radiating lines (sun rays)
        rays = VGroup()
        num_rays = 8  # Number of rays around the circle
        ray_length = 0.4 * scale_factor
        for i in range(num_rays):
            angle = (i * TAU / num_rays)
            ray = Line(
                start=ORIGIN,
                end=ray_length * RIGHT,
                stroke_color=NOVA_ORANGE,
                stroke_width=3
            ).rotate(angle)
            # Position ray to start from edge of circle
            ray.shift((1 + ray_length/2) * scale_factor * (np.cos(angle) * RIGHT + np.sin(angle) * UP))
            rays.add(ray)
        
        # Add small dots at ray ends
        dots = VGroup()
        for ray in rays:
            dot = Dot(
                ray.get_end(),
                color=NOVA_ORANGE,
                radius=0.05 * scale_factor
            )
            dots.add(dot)
        
        # Combine all elements
        self.add(head, rays, dots, left_eye, right_eye, smile)
        
    def blink(self):
        """Animation for blinking"""
        left_eye = self[3]  # Eyes are now fourth and fifth elements
        right_eye = self[4]
        
        # Create scaled versions of the eyes
        blinked_left = left_eye.copy().stretch(0.1, dim=1)
        blinked_right = right_eye.copy().stretch(0.1, dim=1)
        
        return AnimationGroup(
            Transform(left_eye, blinked_left),
            Transform(right_eye, blinked_right),
            rate_func=there_and_back,
            run_time=0.2
        )
    
    def bounce(self):
        """Animation for a playful bounce"""
        return self.animate.shift(UP * 0.3).shift(DOWN * 0.3)
    
    def think(self):
        """Animation for thinking state - rotates the rays"""
        rays = self[1]  # Rays are the second element
        dots = self[2]  # Dots are the third element
        return AnimationGroup(
            Rotate(rays, angle=TAU/2, rate_func=linear),
            Rotate(dots, angle=TAU/2, rate_func=linear),
            run_time=2
        )

# Test scene to visualize Nova
class NovaDemo(Scene):
    def construct(self):
        # Create Nova
        nova = Nova(scale_factor=2)
        
        # Initial appearance
        self.play(Create(nova))
        self.wait()
        
        # Demonstrate animations
        self.play(nova.blink())
        self.wait(0.5)
        self.play(nova.bounce())
        self.wait(0.5)
        self.play(nova.think())
        self.wait()

if __name__ == "__main__":
    # Configure for high quality rendering
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_height = 9
    config.frame_width = 16
    config.background_color = "#1A1A1A"  # Dark background to match main scene
