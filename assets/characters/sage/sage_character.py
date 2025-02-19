from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
import numpy as np

class Sage(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        
        # Create the head (circle with grey fill and darker grey stroke)
        head = Circle(
            radius=0.5,
            fill_color="#4A4A4A",  # Darker grey
            fill_opacity=1,
            stroke_color="#2A2A2A",  # Even darker grey for stroke
            stroke_width=6
        )
        
        # Create eyes (rectangles with bright green fill)
        eye_width = 0.15
        eye_height = 0.1
        eye_style = {"fill_color": "#00FF00", "fill_opacity": 1, "stroke_width": 0}
        left_eye = Rectangle(width=eye_width, height=eye_height, **eye_style)\
            .move_to(head.get_center() + LEFT * 0.2 + UP * 0.1)
        right_eye = Rectangle(width=eye_width, height=eye_height, **eye_style)\
            .move_to(head.get_center() + RIGHT * 0.2 + UP * 0.1)
        
        # Create antenna dots (small green squares)
        dot_size = 0.08
        dot_style = {"fill_color": "#00FF00", "fill_opacity": 1, "stroke_width": 2}
        left_dot = Square(side_length=dot_size, **dot_style)\
            .move_to(head.get_center() + LEFT * 0.4 + UP * 0.6)
        center_dot = Square(side_length=dot_size, **dot_style)\
            .move_to(head.get_center() + UP * 0.7)
        right_dot = Square(side_length=dot_size, **dot_style)\
            .move_to(head.get_center() + RIGHT * 0.4 + UP * 0.6)
        
        # Create mouth (green rectangle)
        mouth = Rectangle(
            width=0.3,
            height=0.05,
            fill_color="#00FF00",
            fill_opacity=1,
            stroke_width=2
        ).move_to(head.get_center() + DOWN * 0.2)
        
        # Create body (black rectangle with green binary code)
        body = Rectangle(
            width=1.0,
            height=1.5,
            fill_color="#000000",
            fill_opacity=1,
            stroke_color="#00FF00",
            stroke_width=4
        ).next_to(head, DOWN, buff=0.3)
        
        # Add binary code to the body
        binary_text = VGroup()
        num_lines = 5
        line_spacing = body.height / (num_lines + 1)
        
        for i in range(num_lines):
            binary_line = Text(
                "10" * 5,  # Repeat "10" pattern
                font_size=16,
                color="#00FF00"  # Bright green
            ).move_to([body.get_center()[0], body.get_top()[1] - (i + 1) * line_spacing, 0])
            binary_text.add(binary_line)
        
        # Create arms (bent dashed lines)
        left_arm = VGroup()
        right_arm = VGroup()
        
        # Parameters for bent arms
        arm_length = 0.8
        
        # Left arm segments (upper and lower)
        left_upper = DashedLine(
            start=body.get_left() + UP * body.height/3,
            end=body.get_left() + LEFT * arm_length/2 + UP * (body.height/3 - arm_length/4),
            dash_length=0.05,
            color="#00FF00"
        )
        left_lower = DashedLine(
            start=left_upper.get_end(),
            end=left_upper.get_end() + LEFT * arm_length/2 + DOWN * arm_length/3,
            dash_length=0.05,
            color="#00FF00"
        )
        left_arm.add(left_upper, left_lower)
        
        # Right arm segments (upper and lower)
        right_upper = DashedLine(
            start=body.get_right() + UP * body.height/3,
            end=body.get_right() + RIGHT * arm_length/2 + UP * (body.height/3 - arm_length/4),
            dash_length=0.05,
            color="#00FF00"
        )
        right_lower = DashedLine(
            start=right_upper.get_end(),
            end=right_upper.get_end() + RIGHT * arm_length/2 + DOWN * arm_length/3,
            dash_length=0.05,
            color="#00FF00"
        )
        right_arm.add(right_upper, right_lower)
        
        # Create floating base (parabola)
        base_width = 2.5
        base_height = 1.2
        base_points = []
        
        # Add shadow ellipse first (underneath everything)
        shadow = Ellipse(
            width=base_width * 0.8,
            height=0.3,
            fill_color="#00FF00",
            fill_opacity=0.3,
            stroke_width=0
        ).move_to([body.get_center()[0], body.get_bottom()[1] - 1.2, 0])
        
        for x in np.linspace(-base_width/2, base_width/2, 30):
            y = base_height * (x * x)/(base_width * base_width/4)  # Concave up parabola
            base_points.append([x + body.get_center()[0], y + body.get_bottom()[1] - 0.8, 0])
        
        floating_base = VMobject()
        floating_base.set_points_smoothly(base_points)
        floating_base.set_stroke(color="#00FF00", width=2)
        floating_base.set_fill(opacity=0)  # Remove fill between legs
        
        # Group everything
        character = VGroup(shadow, floating_base, body, binary_text, left_arm, right_arm, head, left_eye, right_eye, mouth, left_dot, center_dot, right_dot)
        character.shift(UP * 1.5)
        
        # Add everything to the VGroup
        self.add(character)
        
        # Store references for animations
        self.head = head
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.mouth = mouth
        self.binary_text = binary_text
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.floating_base = floating_base
        self.dots = VGroup(left_dot, center_dot, right_dot)
        
        # Apply scale
        self.scale(scale_factor)
    
    def talk(self):
        """Create a talking animation."""
        # Create a talking mouth shape
        mouth_center = self.mouth.get_center() + DOWN * 0.1  # Move mouth down slightly
        talking_mouth = Line(
            start=mouth_center + LEFT * 0.2,
            end=mouth_center + RIGHT * 0.2,
            stroke_width=3,
            color=self.mouth.get_color()
        )
        return Transform(self.mouth, talking_mouth, rate_func=there_and_back)

    def get_shadow(self):
        # Create an elliptical shadow
        shadow = Ellipse(
            width=self.width * 0.8,
            height=self.height * 0.2,
            fill_opacity=0.3,
            stroke_width=0,
            color=GREY
        )
        return shadow

    def blink(self):
        """Create a blinking animation by scaling eyes vertically."""
        return AnimationGroup(
            Transform(
                self.left_eye,
                Rectangle(
                    width=self.left_eye.width,
                    height=self.left_eye.height * 0.1,
                    fill_color="#00FF00",
                    fill_opacity=1,
                    stroke_width=0
                ).move_to(self.left_eye.get_center())
            ),
            Transform(
                self.right_eye,
                Rectangle(
                    width=self.right_eye.width,
                    height=self.right_eye.height * 0.1,
                    fill_color="#00FF00",
                    fill_opacity=1,
                    stroke_width=0
                ).move_to(self.right_eye.get_center())
            ),
            rate_func=there_and_back
        )
    
    def process(self):
        """Create a processing animation by moving binary code and flashing dots."""
        return AnimationGroup(
            self.binary_text.animate.shift(UP * 0.1).shift(DOWN * 0.1),
            self.dots.animate.set_color("#1976D2").set_color("#00FF00"),
            rate_func=there_and_back
        )

class SageDemo(VoiceoverScene):
    def construct(self):
        # Initialize OpenAI service with Echo voice
        self.set_speech_service(
            OpenAIService(
                voice="echo",
                model="tts-1"
            )
        )
        
        # Create Sage and position in center
        sage = Sage(scale_factor=0.8)
        sage.move_to(ORIGIN)
        self.add(sage)
        
        # Create title and subtitle
        name_text = Text("SAGE", font_size=36, color="#00FF00")
        subtitle_text = Text("The Digital Guide", font_size=24, color="#00FF00")
        
        # Position texts below Sage
        name_text.next_to(sage, DOWN, buff=0.3)
        subtitle_text.next_to(name_text, DOWN, buff=0.15)
        
        # Add the voiceover with synchronized animations
        with self.voiceover(text="Hello, I'm Sage, your friendly coding companion. I love helping others learn and grow.") as tracker:
            # Create a continuous talking animation for the duration of the speech
            talk_cycle = 0.8  # Slower mouth movement
            
            # Combine talking and processing animations
            talk_anim = Succession(
                *[
                    AnimationGroup(
                        sage.talk(),
                        sage.process(),
                        run_time=talk_cycle  # Ensure each cycle takes the full duration
                    )
                    for _ in range(int(tracker.duration / talk_cycle))
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
            sage.blink(),
            run_time=0.3
        )
        
        # Small pause before exit
        self.wait(0.2)
        
        # Create a path for smooth exit
        start_pos = sage.get_center()
        end_pos = RIGHT * 12 + UP * 0.5
        
        def update_sage(mob, alpha):
            # Move Sage along path with sine wave
            t = alpha * 3 * PI
            current_x = interpolate(start_pos[0], end_pos[0], alpha)
            current_y = interpolate(start_pos[1], end_pos[1], alpha) + 0.2 * np.sin(t)
            mob.move_to([current_x, current_y, 0])
        
        # Exit animations
        self.play(
            UpdateFromAlphaFunc(sage, update_sage),
            name_text.animate.shift(DOWN * 6),
            subtitle_text.animate.shift(DOWN * 6),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine
        )
