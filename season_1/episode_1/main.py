from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from dotenv import load_dotenv
import os, random, openai

load_dotenv()

# Base VoiceoverScene that other scenes will inherit from
class BaseScene(VoiceoverScene):
    def setup(self):
        super().setup()
        # Use environment variable for API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Now set up the speech service
        self.set_speech_service(OpenAIService(
            voice="nova",
            api_key=os.getenv("OPENAI_API_KEY")
        ))

# Add after imports
START = LEFT  # Define START constant for power streams

class FadeToBlack(Animation):
    def __init__(self, **kwargs):
        # Create a black square that covers the screen
        black_square = Square(
            side_length=FRAME_WIDTH,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        super().__init__(
            black_square,
            rate_func=there_and_back,  # Move rate_func to super().__init__
            **kwargs
        )

# Create a simple high school building
class HighSchool(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main building structure
        self.building = Rectangle(
            width=8,
            height=4,
            fill_color="#555555",
            fill_opacity=0.8,
            stroke_color=WHITE
        )
        
        # Roof
        self.roof = Polygon(
            [-4, 2, 0],  # Left point
            [4, 2, 0],   # Right point
            [0, 3, 0],   # Top point
            fill_color="#773333",
            fill_opacity=0.8,
            stroke_color=WHITE
        )
        
        # Windows - store as attribute for later access
        self.windows = VGroup(*[
            Rectangle(
                width=0.8,
                height=1.2,
                fill_color=Colors.NOVA_BLUE,
                fill_opacity=0.3,
                stroke_color=WHITE
            ).move_to([-2.5 + i*1.5, 0, 0])
            for i in range(5)
        ])
        
        # Door
        self.door = Rectangle(
            width=1.2,
            height=2,
            fill_color="#442222",
            fill_opacity=1,
            stroke_color=WHITE
        ).move_to([0, -1, 0])
        
        # Add all elements to the VGroup
        self.add(self.building, self.roof, self.windows, self.door)

class OpeningHook(BaseScene):
    def construct(self):
        # Create night sky background
        sky = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#0D1B2A",
            fill_opacity=1,
            stroke_width=0
        )
        
        # Create high school building using our custom class
        school = HighSchool()
        school.set_width(config.frame_width * 0.8)
        school.to_edge(DOWN)
        
        # Create student placeholders until we have proper SVGs
        students = VGroup(
            # Ada placeholder (purple circle)
            Circle(radius=0.4, color=Colors.ADA_PURPLE, fill_opacity=0.8),
            # Marcus placeholder (green hexagon)
            RegularPolygon(n=6, color=Colors.MARCUS_GREEN, fill_opacity=0.8),
            # Maya placeholder (gold triangle)
            Triangle(color=Colors.MAYA_GOLD, fill_opacity=0.8)
        ).arrange(RIGHT, buff=1)
        students.scale(0.8)
        students.next_to(school, UP)
        
        with self.voiceover(text="""
            Sometimes the biggest discoveries happen by accident...
            And for three ordinary high school students, 
            one late night study session was about to change everything.
        """):
            # Show the setting
            self.play(
                FadeIn(sky),
                FadeIn(school)
            )
            
            # Animate windows changing colors
            window_colors = [
                Colors.ADA_PURPLE,
                Colors.MARCUS_GREEN,
                Colors.MAYA_GOLD,
                Colors.NOVA_BLUE
            ]
            
            # Create window color animation
            self.play(
                *[
                    window.animate.set_fill(
                        random.choice(window_colors),
                        opacity=random.uniform(0.3, 0.6)
                    )
                    for window in school.windows
                ],
                run_time=1
            )
            
            # Create and animate strange lights with more intensity
            lights = VGroup(*[
                Circle(
                    radius=random.uniform(0.1, 0.3),
                    fill_color=Colors.NOVA_BLUE,
                    fill_opacity=random.uniform(0.4, 0.8),
                    stroke_width=0
                ).move_to([
                    random.uniform(-config.frame_width/3, config.frame_width/3),
                    random.uniform(1, config.frame_height/2),
                    0
                ])
                for _ in range(15)  # More lights
            ])
            
            # Animate the lights while windows continue to change
            self.play(
                LaggedStart(*[
                    FadeIn(light, scale=random.uniform(1.2, 1.5))
                    for light in lights
                ], lag_ratio=0.2),
                *[
                    light.animate.shift(UP * random.uniform(0.5, 1.0))
                    for light in lights
                ],
                *[
                    window.animate.set_fill(
                        random.choice(window_colors),
                        opacity=random.uniform(0.3, 0.6)
                    )
                    for window in school.windows
                ],
                run_time=2
            )

        # New voiceover for dramatic buildup
        with self.voiceover(text="""
            As the strange lights filled the sky, 
            they had no idea they were about to become...
        """):
            # Show the students reacting with enhanced effects
            self.play(
                FadeIn(students),
                *[
                    Flash(
                        light,
                        color=Colors.NOVA_BLUE,
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for light in lights  # Flash all lights
                ],
                *[
                    window.animate.set_fill(
                        Colors.NOVA_BLUE,
                        opacity=0.8  # Brighter windows
                    )
                    for window in school.windows
                ],
                run_time=2
            )

            # Add power auras around students
            auras = VGroup(*[
                Circle(
                    radius=0.6,
                    stroke_color=student.get_color(),
                    stroke_opacity=0.6,
                    fill_color=student.get_color(),
                    fill_opacity=0.2
                ).move_to(student)
                for student in students
            ])

            self.play(
                *[
                    Create(aura)
                    for aura in auras
                ],
                *[
                    student.animate.scale(1.2)
                    for student in students
                ],
                run_time=1
            )

            # Final flash before title
            self.play(
                *[
                    Flash(
                        aura,
                        color=aura.get_stroke_color(),
                        line_length=0.5,
                        flash_radius=1.0
                    )
                    for aura in auras
                ],
                run_time=1
            )

class TitleSequence(BaseScene):
    def construct(self):
        # Create main title
        title = Text("GENIUS FORCE", color=Colors.TEXT_LIGHT)
        subtitle = Text("The Quantum Leap", 
                       color=Colors.NOVA_BLUE,
                       font_size=36)
        
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
        
        # Create character symbols using SVGs
        characters = VGroup(
            SVGMobject("assets/characters/maya/maya_base.svg"),    # Maya
            SVGMobject("assets/characters/nova/nova_base.svg"),    # Nova in center
            SVGMobject("assets/characters/marcus/marcus_base.svg") # Marcus
        ).arrange(RIGHT, buff=1)
        
        # Scale and position characters
        characters.scale(0.4)  # Adjust scale to fit nicely
        characters.next_to(title_group, DOWN, buff=1)
        
        # Set character colors
        characters[0].set_color(Colors.MAYA_GOLD)      # Maya
        characters[1].set_color(Colors.NOVA_BLUE)      # Nova
        characters[2].set_color(Colors.MARCUS_GREEN)   # Marcus

        with self.voiceover(text="""
            GENIUS FORCE!
            Where science meets the extraordinary.
        """):
            # Dramatic title reveal
            self.play(
                Write(title, run_time=1.5),
                *[
                    FadeIn(char, scale=1.5)
                    for char in characters
                ]
            )
            
            # Add subtitle with power effect
            self.play(
                Write(subtitle),
                *[
                    Flash(
                        char,
                        color=char.get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for char in characters
                ],
                run_time=1
            )
            
            # Final power surge
            self.play(
                *[
                    char.animate.scale(1.2)
                    for char in characters
                ],
                title_group.animate.set_color(Colors.NOVA_BLUE),
                run_time=0.5
            )
            
            # Add a small pulse animation to Nova
            self.play(
                characters[1].animate.scale(1.1),
                rate_func=there_and_back,
                run_time=0.5
            )
            
            self.wait(0.5)

class ProblemIntroduction(BaseScene):
    def construct(self):
        # Add your problem introduction animations here
        pass

class FirstAttempt(BaseScene):
    def construct(self):
        # Keep lab background
        lab = SVGMobject("assets/backgrounds/science_lab.svg")
        lab.set_width(config.frame_width)
        lab.set_height(config.frame_height)
        self.add(lab)

        # Create observation notes
        notes = VGroup()
        observations = [
            "Glowing entity",
            "Energy readings",
            "Lab disturbances"
        ]
        
        for obs in observations:
            note = Text(obs, color=Colors.TEXT_LIGHT, font_size=24)
            bullet = Dot(color=Colors.TEXT_LIGHT)
            line = Line(LEFT, RIGHT, color=Colors.TEXT_LIGHT)
            note_group = VGroup(bullet, line, Text(obs, color=Colors.TEXT_LIGHT))
            note_group.arrange(RIGHT, buff=0.2)
            notes.add(note_group)
        
        notes.arrange(DOWN, buff=0.5).to_edge(LEFT)

        with self.voiceover(text="""
            The students began making careful observations, trying to understand 
            what they were dealing with...
        """):
            self.play(
                LaggedStart(*[
                    Write(note)
                    for note in notes
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create hypothesis bubble
        hypothesis = ThoughtBubble()
        hypothesis_text = Text(
            "Energy-based\nlifeform?", 
            color=Colors.NOVA_BLUE,
            font_size=24
        )
        hypothesis_text.move_to(hypothesis.get_bubble_center())
        hypothesis_group = VGroup(hypothesis, hypothesis_text)
        hypothesis_group.next_to(notes, RIGHT, buff=1)

        with self.voiceover(text="""
            They formed hypotheses about Nova's nature, but as they tried to 
            test their theories, something unexpected happened...
        """):
            self.play(
                Create(hypothesis),
                Write(hypothesis_text),
                run_time=2
            )

            # Create power activation effects
            powers = VGroup(
                Circle(radius=0.4, color=Colors.ADA_PURPLE),  # Ada's time powers
                RegularPolygon(n=6, color=Colors.MARCUS_GREEN),  # Marcus's molecular powers
                Triangle(color=Colors.MAYA_GOLD)  # Maya's geometric powers
            ).arrange(RIGHT, buff=1)
            powers.next_to(hypothesis_group, RIGHT, buff=1)

            self.play(
                *[
                    Flash(
                        power,
                        color=power.get_color(),
                        line_length=0.3,
                        num_lines=12,
                        flash_radius=0.6
                    )
                    for power in powers
                ],
                *[
                    power.animate.scale(1.5).set_opacity(0.8)
                    for power in powers
                ],
                run_time=2
            )

class LearningSequence(BaseScene):
    def construct(self):
        # Create scientific method diagram
        method_steps = VGroup()
        steps = [
            ("Observation", Colors.ADA_PURPLE),
            ("Question", Colors.MARCUS_GREEN),
            ("Hypothesize", Colors.MAYA_GOLD),
            ("Experiment", Colors.NOVA_BLUE),
            ("Analysis", Colors.ADA_PURPLE),
            ("Conclusion", Colors.TEXT_LIGHT)
        ]

        for step, color in steps:
            box = Rectangle(height=1, width=2, color=color)
            text = Text(step, color=color, font_size=24)
            text.move_to(box)
            step_group = VGroup(box, text)
            method_steps.add(step_group)

        method_steps.arrange(DOWN, buff=0.3)
        method_steps.to_edge(LEFT)

        # Create arrows connecting steps
        arrows = VGroup(*[
            Arrow(
                method_steps[i].get_bottom(),
                method_steps[i+1].get_top(),
                color=Colors.TEXT_LIGHT
            )
            for i in range(len(method_steps)-1)
        ])

        with self.voiceover(text="""
            To understand their new powers, the team needed to apply 
            the scientific method systematically...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(step)
                    for step in method_steps
                ], lag_ratio=0.2),
                LaggedStart(*[
                    GrowArrow(arrow)
                    for arrow in arrows
                ], lag_ratio=0.2),
                run_time=3
            )

        # Create power demonstration areas
        demo_areas = VGroup(*[
            Circle(radius=1, color=color)
            for _, color in steps[:3]  # One for each student
        ]).arrange(RIGHT, buff=1).to_edge(RIGHT)

        with self.voiceover(text="""
            Each student's power aligned with different aspects of scientific thinking.
            Ada's time manipulation helped with careful observation...
        """):
            # Ada's demonstration
            time_effect = VGroup(
                Circle(radius=0.8, color=Colors.ADA_PURPLE),
                Arrow(LEFT, RIGHT, color=Colors.ADA_PURPLE),
                Arrow(RIGHT, LEFT, color=Colors.ADA_PURPLE)
            ).move_to(demo_areas[0])
            
            self.play(
                FadeIn(time_effect),
                Flash(
                    demo_areas[0],
                    color=Colors.ADA_PURPLE,
                    line_length=0.3,
                    flash_radius=0.8
                ),
                method_steps[0].animate.scale(1.2),
                run_time=2
            )

        with self.voiceover(text="""
            Marcus's molecular understanding helped form precise questions...
        """):
            # Marcus's demonstration
            molecules = VGroup(*[
                Circle(radius=0.1, color=Colors.MARCUS_GREEN)
                for _ in range(6)
            ]).arrange_in_grid(2, 3, buff=0.2)
            molecules.move_to(demo_areas[1])
            
            self.play(
                FadeIn(molecules),
                molecules.animate.shift(UP * 0.3),
                method_steps[1].animate.scale(1.2),
                run_time=2
            )

        with self.voiceover(text="""
            And Maya's geometric insight helped create testable hypotheses...
        """):
            # Maya's demonstration
            shapes = VGroup(
                Triangle(color=Colors.MAYA_GOLD),
                Square(color=Colors.MAYA_GOLD),
                RegularPolygon(5, color=Colors.MAYA_GOLD)
            ).arrange(RIGHT, buff=0.2)
            shapes.move_to(demo_areas[2])
            
            self.play(
                FadeIn(shapes),
                Rotate(shapes, PI),
                method_steps[2].animate.scale(1.2),
                run_time=2
            )

class TeamRegroup(BaseScene):
    def construct(self):
        # Create lab background
        lab = SVGMobject("assets/backgrounds/science_lab.svg")
        lab.set_width(config.frame_width)
        lab.set_height(config.frame_height)
        self.add(lab)

        # Create data collection setup
        whiteboard = Rectangle(
            width=4,
            height=3,
            color=Colors.TEXT_LIGHT,
            fill_opacity=0.2
        ).to_edge(LEFT)

        data_points = VGroup(*[
            Dot(color=Colors.TEXT_LIGHT)
            for _ in range(10)
        ]).arrange_in_grid(2, 5, buff=0.3)
        data_points.move_to(whiteboard)

        with self.voiceover(text="""
            The team gathered to analyze their data and plan controlled experiments...
        """):
            self.play(
                Create(whiteboard),
                LaggedStart(*[
                    FadeIn(point)
                    for point in data_points
                ], lag_ratio=0.1),
                run_time=2
            )

        # Create experiment setup
        test_area = Circle(radius=1.5, color=Colors.NOVA_BLUE)
        test_area.to_edge(RIGHT)
        
        safety_boundary = DashedVMobject(
            Circle(radius=2, color=Colors.TEXT_LIGHT)
        ).move_to(test_area)

        equipment = VGroup(
            Rectangle(height=0.5, width=0.3),  # Sensor
            Triangle(color=Colors.TEXT_LIGHT),  # Stand
            Circle(radius=0.2)  # Detector
        ).arrange(RIGHT, buff=0.2)
        equipment.next_to(test_area, DOWN)

        with self.voiceover(text="""
            They set up safety protocols and measurement systems to track their progress...
        """):
            self.play(
                Create(test_area),
                Create(safety_boundary),
                FadeIn(equipment),
                run_time=2
            )

        # Create power testing visualization
        power_tests = VGroup()
        for color in [Colors.ADA_PURPLE, Colors.MARCUS_GREEN, Colors.MAYA_GOLD]:
            test = VGroup(
                Circle(radius=0.3, color=color),
                Arrow(LEFT, RIGHT, color=color),
                Text("Test", color=color, font_size=20)
            ).arrange(RIGHT, buff=0.2)
            power_tests.add(test)
        
        power_tests.arrange(DOWN, buff=0.5)
        power_tests.move_to(test_area)

        with self.voiceover(text="""
            Each team member would test their powers under controlled conditions,
            carefully documenting every result...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(test)
                    for test in power_tests
                ], lag_ratio=0.3),
                *[
                    ShowPassingFlash(
                        Line(
                            data_points.get_center(),
                            test_area.get_center(),
                            color=Colors.NOVA_BLUE
                        ),
                        time_width=0.5,
                        run_time=2
                    )
                    for _ in range(3)
                ]
            )

class ResearchMontage(BaseScene):
    def construct(self):
        # Create split screen effect with three sections
        sections = VGroup(*[
            Rectangle(
                width=config.frame_width/3 - 0.5,
                height=config.frame_height,
                color=color,
                fill_opacity=0.1
            ) for color in [
                Colors.ADA_PURPLE,
                Colors.MARCUS_GREEN,
                Colors.MAYA_GOLD
            ]
        ]).arrange(RIGHT, buff=0.5)
        self.add(sections)

        # Create research elements for each student
        with self.voiceover(text="""
            The team dove into their research, each exploring their unique abilities...
        """):
            # Ada's time research
            time_graphs = VGroup(*[
                FunctionGraph(
                    lambda x: np.sin(x + i),
                    x_range=[-3, 3],
                    color=Colors.ADA_PURPLE
                )
                for i in range(3)
            ]).arrange(DOWN, buff=0.5)
            time_graphs.move_to(sections[0])

            # Marcus's molecular studies
            molecules = VGroup(*[
                VGroup(*[
                    Circle(radius=0.1, color=Colors.MARCUS_GREEN)
                    for _ in range(random.randint(3, 6))
                ]).arrange_in_grid(2, 3, buff=0.2)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.5)
            molecules.move_to(sections[1])

            # Maya's geometric patterns
            patterns = VGroup(*[
                RegularPolygon(n=i+3, color=Colors.MAYA_GOLD)
                for i in range(3)
            ]).arrange(DOWN, buff=0.5)
            patterns.move_to(sections[2])

            # Animate research appearing
            self.play(
                LaggedStart(*[
                    Create(graph)
                    for graph in time_graphs
                ], lag_ratio=0.3),
                LaggedStart(*[
                    FadeIn(molecule)
                    for molecule in molecules
                ], lag_ratio=0.3),
                LaggedStart(*[
                    DrawBorderThenFill(pattern)
                    for pattern in patterns
                ], lag_ratio=0.3),
                run_time=3
            )

        # Show progress indicators
        progress_bars = VGroup(*[
            Rectangle(
                width=0.5,
                height=3,
                color=section.get_color()
            ).next_to(section, DOWN)
            for section in sections
        ])

        with self.voiceover(text="""
            Through trial and error, they began to understand their powers better...
        """):
            # Fill progress bars with some setbacks
            for bar in progress_bars:
                fill = bar.copy().set_fill(bar.get_color(), opacity=0.8)
                fill.set_height(0)
                fill.move_to(bar.get_bottom())
                
                # Progress with occasional setbacks
                heights = [1, 0.8, 1.5, 1.2]
                for height in heights:
                    self.play(
                        fill.animate.scale_to_fit_height(height),
                        run_time=0.5
                    )

        # Show comic relief moment
        with self.voiceover(text="""
            Of course, there were a few unexpected results along the way...
        """):
            # Create funny power malfunction effects
            self.play(
                *[
                    Flash(
                        section,
                        color=section.get_color(),
                        line_length=0.3,
                        flash_radius=0.8
                    )
                    for section in sections
                ],
                *[
                    Rotate(mob, angle=TAU)
                    for mob in [time_graphs, molecules, patterns]
                ],
                run_time=2
            )

class BreakthroughMoment(BaseScene):
    def construct(self):
        # Create central breakthrough visualization
        breakthrough = Circle(radius=2, color=Colors.NOVA_BLUE)
        
        # Create scientific method cycle
        method_cycle = VGroup(*[
            Text(step, color=Colors.TEXT_LIGHT, font_size=24)
            for step in [
                "Observe",
                "Question",
                "Hypothesize",
                "Experiment",
                "Analyze",
                "Conclude"
            ]
        ])

        # Arrange in circle
        angle = TAU / len(method_cycle)
        for i, step in enumerate(method_cycle):
            step.move_to(
                breakthrough.point_from_proportion(i/len(method_cycle))
            )

        with self.voiceover(text="""
            Finally, the team made a crucial breakthrough. The scientific method 
            wasn't just helping them study their powers...
        """):
            self.play(
                Create(breakthrough),
                LaggedStart(*[
                    Write(step)
                    for step in method_cycle
                ], lag_ratio=0.2),
                run_time=3
            )

        # Create power control visualization
        control_rings = VGroup(*[
            Circle(
                radius=1.5 + i*0.3,
                color=color,
                stroke_opacity=0.5
            ) for i, color in enumerate([
                Colors.ADA_PURPLE,
                Colors.MARCUS_GREEN,
                Colors.MAYA_GOLD
            ])
        ])

        with self.voiceover(text="""
            It was the key to controlling them!
        """):
            self.play(
                *[
                    Create(ring)
                    for ring in control_rings
                ],
                breakthrough.animate.scale(1.2),
                method_cycle.animate.scale(1.2),
                run_time=2
            )

            # Show power mastery effect
            self.play(
                *[
                    ring.animate.scale(1.5).set_opacity(0.8)
                    for ring in control_rings
                ],
                Flash(
                    breakthrough,
                    color=Colors.NOVA_BLUE,
                    line_length=0.5,
                    flash_radius=1.0
                ),
                run_time=2
            )

class PlanFormation(BaseScene):
    def construct(self):
        # Create lab background
        lab = SVGMobject("assets/backgrounds/science_lab.svg")
        lab.set_width(config.frame_width)
        lab.set_height(config.frame_height)
        self.add(lab)

        # Create planning board
        board = Rectangle(
            width=6,
            height=4,
            color=Colors.TEXT_LIGHT,
            fill_opacity=0.1
        ).to_edge(LEFT)

        # Create plan sections
        sections = VGroup()
        titles = ["Safety Protocols", "Testing Sequence", "Data Collection"]
        
        for title in titles:
            section = VGroup(
                Text(title, color=Colors.TEXT_LIGHT, font_size=28),
                Rectangle(width=5, height=0.8, color=Colors.TEXT_LIGHT)
            ).arrange(DOWN, buff=0.2)
            sections.add(section)
        
        sections.arrange(DOWN, buff=0.5)
        sections.move_to(board)

        with self.voiceover(text="""
            The team developed a structured plan to test and document their powers safely...
        """):
            self.play(
                Create(board),
                LaggedStart(*[
                    Write(section)
                    for section in sections
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create role assignments
        roles = VGroup()
        assignments = [
            (Colors.ADA_PURPLE, "Time Analysis"),
            (Colors.MARCUS_GREEN, "Safety Monitor"),
            (Colors.MAYA_GOLD, "Data Recording")
        ]

        for color, role in assignments:
            role_group = VGroup(
                Circle(radius=0.2, color=color),
                Arrow(LEFT, RIGHT, color=color),
                Text(role, color=color, font_size=24)
            ).arrange(RIGHT, buff=0.2)
            roles.add(role_group)

        roles.arrange(DOWN, buff=0.5)
        roles.to_edge(RIGHT)

        with self.voiceover(text="""
            Each team member took on specific responsibilities based on their strengths...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(role)
                    for role in roles
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create equipment setup visualization
        equipment = VGroup()
        for i in range(3):
            station = VGroup(
                Rectangle(height=0.8, width=0.5),  # Base
                Triangle(color=Colors.TEXT_LIGHT),  # Sensor
                Circle(radius=0.1)  # Indicator
            ).arrange(UP, buff=0.1)
            equipment.add(station)
        
        equipment.arrange(RIGHT, buff=1)
        equipment.next_to(board, DOWN, buff=1)

        with self.voiceover(text="""
            They set up specialized equipment to measure and monitor their powers...
        """):
            self.play(
                LaggedStart(*[
                    Create(station)
                    for station in equipment
                ], lag_ratio=0.2),
                run_time=2
            )

class InitialTest(BaseScene):
    def construct(self):
        # Create test environment
        test_area = Circle(radius=2, color=Colors.NOVA_BLUE, fill_opacity=0.1)
        test_area.to_edge(LEFT)

        # Create data collection interface
        interface = VGroup(
            Rectangle(width=4, height=3, color=Colors.TEXT_LIGHT),
            *[
                Line(
                    LEFT * 1.8, RIGHT * 1.8,
                    color=Colors.TEXT_LIGHT,
                    stroke_opacity=0.5
                )
                for _ in range(4)
            ]
        )
        interface.arrange(DOWN, buff=0.3)
        interface.to_edge(RIGHT)

        with self.voiceover(text="""
            The team began their first controlled power tests, carefully monitoring every detail...
        """):
            self.play(
                Create(test_area),
                Create(interface),
                run_time=2
            )

        # Create individual power tests
        power_tests = VGroup()
        for color, shape_func in [
            (Colors.ADA_PURPLE, lambda: Circle()),
            (Colors.MARCUS_GREEN, lambda: RegularPolygon(6)),
            (Colors.MAYA_GOLD, lambda: Triangle())
        ]:
            shape = shape_func()
            shape.set_color(color)
            shape.set_fill(opacity=0.3)
            power_tests.add(shape)

        power_tests.arrange(RIGHT, buff=1)
        power_tests.move_to(test_area)

        # Create data visualization
        data_points = VGroup()
        graphs = VGroup()

        with self.voiceover(text="""
            Each power was tested individually, with data collected on intensity, 
            duration, and control levels...
        """):
            for i, test in enumerate(power_tests):
                # Test animation
                self.play(
                    FadeIn(test),
                    Flash(
                        test,
                        color=test.get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    ),
                    run_time=1
                )

                # Data collection animation
                points = VGroup(*[
                    Dot(color=test.get_color())
                    for _ in range(5)
                ]).arrange(RIGHT, buff=0.2)
                points.move_to(interface[i+1])
                data_points.add(points)

                # Create graph
                graph = FunctionGraph(
                    lambda x: np.sin(x + i) * np.exp(-0.2*x),
                    x_range=[0, 4],
                    color=test.get_color()
                ).scale(0.3)
                graph.next_to(points, RIGHT)
                graphs.add(graph)

                self.play(
                    LaggedStart(*[
                        FadeIn(point)
                        for point in points
                    ], lag_ratio=0.2),
                    Create(graph),
                    run_time=1
                )

        # Show success indicators
        success_markers = VGroup(*[
            Text("✓", color=Colors.MARCUS_GREEN, font_size=36)
            for _ in range(3)
        ]).arrange(RIGHT, buff=2)
        success_markers.next_to(power_tests, UP)

        with self.voiceover(text="""
            The initial results were promising, though there was still room for improvement...
        """):
            self.play(
                LaggedStart(*[
                    Write(marker)
                    for marker in success_markers
                ], lag_ratio=0.3),
                *[
                    test.animate.set_opacity(0.8)
                    for test in power_tests
                ],
                run_time=2
            )

class BPlotEscalation(BaseScene):
    def construct(self):
        # Create Nova's urgent message visualization
        nova = VGroup(
            Circle(radius=1, color=Colors.NOVA_BLUE, fill_opacity=0.4),
            Circle(radius=0.7, color=Colors.NOVA_BLUE, fill_opacity=0.6),
            Circle(radius=0.4, color=Colors.NOVA_BLUE, fill_opacity=0.8)
        )
        nova.to_edge(UP)

        # Create timeline visualization
        timeline = Line(LEFT * 4, RIGHT * 4, color=Colors.TEXT_LIGHT)
        timeline.to_edge(DOWN, buff=2)
        
        markers = VGroup(*[
            Dot(color=Colors.TEXT_LIGHT)
            for _ in range(5)
        ]).arrange(RIGHT, buff=1.5)
        markers.move_to(timeline)

        with self.voiceover(text="""
            Nova revealed that time was running out. A greater challenge was approaching, 
            and the team needed to master their powers quickly...
        """):
            self.play(
                FadeIn(nova, scale=1.2),
                Create(timeline),
                LaggedStart(*[
                    FadeIn(marker)
                    for marker in markers
                ], lag_ratio=0.2),
                run_time=2
            )

            # Create urgency effect
            warning_pulses = VGroup(*[
                Circle(
                    radius=0.3,
                    color=Colors.NOVA_BLUE,
                    stroke_opacity=0.8 - i*0.2
                )
                for i in range(3)
            ]).move_to(markers[-1])

            self.play(
                *[
                    pulse.animate.scale(3).set_opacity(0)
                    for pulse in warning_pulses
                ],
                markers[-1].animate.set_color(Colors.NOVA_BLUE),
                run_time=2
            )

        # Show environmental effects
        lab_equipment = VGroup(*[
            VGroup(
                Rectangle(height=0.8, width=0.4),  # Base
                Circle(radius=0.2)  # Display
            ).arrange(UP, buff=0.1)
            for _ in range(4)
        ]).arrange(RIGHT, buff=1)
        lab_equipment.next_to(timeline, UP, buff=1)

        with self.voiceover(text="""
            Their growing powers were already affecting the lab equipment around them...
        """):
            # Show equipment malfunctions
            for equipment in lab_equipment:
                self.play(
                    FadeIn(equipment),
                    equipment.animate.shift(
                        UP * random.uniform(0.1, 0.3)
                    ).set_color(Colors.NOVA_BLUE),
                    run_time=0.5
                )

            self.play(
                *[
                    Flash(
                        equipment,
                        color=Colors.NOVA_BLUE,
                        line_length=0.2,
                        flash_radius=0.4
                    )
                    for equipment in lab_equipment
                ],
                run_time=1.5
            )

class TeamAdaptation(BaseScene):
    def construct(self):
        # Create data analysis display
        display = Rectangle(
            width=6,
            height=4,
            color=Colors.TEXT_LIGHT,
            fill_opacity=0.1
        ).to_edge(LEFT)

        # Create power graphs
        graphs = VGroup()
        for color in [Colors.ADA_PURPLE, Colors.MARCUS_GREEN, Colors.MAYA_GOLD]:
            graph = FunctionGraph(
                lambda x: np.exp(-0.5*x) * np.sin(2*x),
                x_range=[0, 4],
                color=color
            ).scale(0.5)
            graphs.add(graph)
        
        graphs.arrange(DOWN, buff=0.5)
        graphs.move_to(display)

        with self.voiceover(text="""
            The team quickly adapted their approach, refining their hypotheses 
            based on the new data...
        """):
            self.play(
                Create(display),
                LaggedStart(*[
                    Create(graph)
                    for graph in graphs
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create improved testing setup
        test_setup = VGroup()
        for color in [Colors.ADA_PURPLE, Colors.MARCUS_GREEN, Colors.MAYA_GOLD]:
            station = VGroup(
                Circle(radius=0.5, color=color, fill_opacity=0.2),
                *[
                    Line(
                        ORIGIN,
                        UP * 0.5,
                        color=color,
                        stroke_opacity=0.6
                    ).rotate(angle)
                    for angle in np.linspace(0, TAU, 8)
                ]
            )
            test_setup.add(station)
        
        test_setup.arrange(RIGHT, buff=1)
        test_setup.to_edge(RIGHT)

        with self.voiceover(text="""
            They developed more sophisticated testing methods, using the lab 
            equipment in innovative ways...
        """):
            self.play(
                LaggedStart(*[
                    Create(station)
                    for station in test_setup
                ], lag_ratio=0.3),
                run_time=2
            )

            # Show improved data collection
            data_streams = VGroup(*[
                DashedLine(
                    station.get_center(),
                    display.get_right(),
                    color=station[0].get_color(),
                    stroke_opacity=0.6
                )
                for station in test_setup
            ])

            self.play(
                LaggedStart(*[
                    Create(stream)
                    for stream in data_streams
                ], lag_ratio=0.2),
                *[
                    ShowPassingFlash(
                        stream.copy().set_stroke(width=3),
                        time_width=0.5,
                        run_time=2
                    )
                    for stream in data_streams
                ],
                run_time=2
            )

        # Show team collaboration
        team_circle = Circle(radius=1.5, color=Colors.NOVA_BLUE)
        team_circle.move_to(
            VGroup(display, test_setup).get_center()
        )

        with self.voiceover(text="""
            Working together, they began to see patterns in how their powers 
            complemented each other...
        """):
            self.play(
                Create(team_circle),
                *[
                    station.animate.scale(1.2)
                    for station in test_setup
                ],
                *[
                    graph.animate.set_stroke(width=3)
                    for graph in graphs
                ],
                run_time=2
            )

            # Show power synergy
            self.play(
                *[
                    Flash(
                        station,
                        color=station[0].get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for station in test_setup
                ],
                team_circle.animate.scale(1.2).set_opacity(0.8),
                run_time=2
            )

class SecondaryChallenge(BaseScene):
    def construct(self):
        # Create power interaction visualization
        interaction_field = Circle(radius=2, color=Colors.NOVA_BLUE, fill_opacity=0.1)
        
        # Create individual power representations
        powers = VGroup(
            Circle(radius=0.5, color=Colors.ADA_PURPLE),  # Time
            RegularPolygon(6, color=Colors.MARCUS_GREEN),  # Molecular
            Triangle(color=Colors.MAYA_GOLD)  # Geometric
        ).arrange(RIGHT, buff=1)
        powers.move_to(interaction_field)

        with self.voiceover(text="""
            Just as they were making progress, the team discovered their powers 
            could interact in unexpected ways...
        """):
            self.play(
                Create(interaction_field),
                LaggedStart(*[
                    FadeIn(power)
                    for power in powers
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create power interaction effects
        interaction_lines = VGroup(*[
            Line(
                powers[i].get_center(),
                powers[j].get_center(),
                color=Colors.NOVA_BLUE,
                stroke_opacity=0.6
            )
            for i in range(len(powers))
            for j in range(i + 1, len(powers))
        ])

        with self.voiceover(text="""
            When their abilities combined, they created complex chain reactions 
            that needed careful analysis...
        """):
            self.play(
                Create(interaction_lines),
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.TEXT_LIGHT),
                        time_width=0.5,
                        run_time=2
                    )
                    for line in interaction_lines
                ],
                *[
                    power.animate.scale(1.2)
                    for power in powers
                ],
                run_time=2
            )

        # Create variable tracking system
        variables = VGroup()
        for i, power in enumerate(powers):
            readings = VGroup(*[
                Text(f"V{i+1}: {random.randint(0, 100)}%", 
                     color=power.get_color(),
                     font_size=24)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.2)
            variables.add(readings)
        
        variables.arrange(RIGHT, buff=1)
        variables.to_edge(UP)

        with self.voiceover(text="""
            The team had to quickly apply the scientific method to understand 
            these new interactions...
        """):
            self.play(
                LaggedStart(*[
                    Write(var)
                    for var in variables
                ], lag_ratio=0.2),
                *[
                    Flash(
                        power,
                        color=power.get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for power in powers
                ],
                run_time=2
            )

class ConceptMastery(BaseScene):
    def construct(self):
        # Create scientific method flowchart
        method_boxes = VGroup()
        steps = [
            ("Observe", Colors.ADA_PURPLE),
            ("Question", Colors.MARCUS_GREEN),
            ("Hypothesize", Colors.MAYA_GOLD),
            ("Experiment", Colors.NOVA_BLUE),
            ("Analyze", Colors.ADA_PURPLE),
            ("Conclude", Colors.TEXT_LIGHT)
        ]

        for step, color in steps:
            box = VGroup(
                Rectangle(height=0.8, width=2, color=color),
                Text(step, color=color, font_size=24)
            )
            box[1].move_to(box[0])
            method_boxes.add(box)

        method_boxes.arrange(RIGHT, buff=0.5)
        method_boxes.to_edge(UP)

        # Create connecting arrows
        arrows = VGroup(*[
            Arrow(
                method_boxes[i][0].get_right(),
                method_boxes[i+1][0].get_left(),
                color=Colors.TEXT_LIGHT
            )
            for i in range(len(method_boxes)-1)
        ])

        with self.voiceover(text="""
            As their understanding grew, the team saw how each step of the 
            scientific method strengthened their control...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(box)
                    for box in method_boxes
                ], lag_ratio=0.2),
                LaggedStart(*[
                    GrowArrow(arrow)
                    for arrow in arrows
                ], lag_ratio=0.2),
                run_time=3
            )

        # Create power demonstration area
        demo_area = Circle(radius=2, color=Colors.NOVA_BLUE)
        demo_area.next_to(method_boxes, DOWN, buff=1)

        # Create controlled power effects
        power_effects = VGroup()
        for color in [Colors.ADA_PURPLE, Colors.MARCUS_GREEN, Colors.MAYA_GOLD]:
            effect = VGroup(
                Circle(radius=0.5, color=color, fill_opacity=0.2),
                *[
                    Line(
                        ORIGIN,
                        UP * 0.5,
                        color=color,
                        stroke_opacity=0.6
                    ).rotate(angle)
                    for angle in np.linspace(0, TAU, 8)
                ]
            )
            power_effects.add(effect)
        
        power_effects.arrange(RIGHT, buff=1)
        power_effects.move_to(demo_area)

        with self.voiceover(text="""
            They could now demonstrate precise control over their abilities...
        """):
            self.play(
                Create(demo_area),
                LaggedStart(*[
                    Create(effect)
                    for effect in power_effects
                ], lag_ratio=0.3),
                run_time=2
            )

            # Show controlled power activation
            self.play(
                *[
                    Succession(
                        Flash(
                            effect,
                            color=effect[0].get_color(),
                            line_length=0.3,
                            flash_radius=0.6
                        ),
                        effect.animate.scale(1.2),
                        effect.animate.scale(1/1.2)
                    )
                    for effect in power_effects
                ],
                run_time=3
            )

        # Create teaching visualization
        teaching_bubbles = VGroup(*[
            ThoughtBubble(
                scale_factor=1.2
            ).move_to([
                3 * (1 if i%2==0 else -1),  # X position
                2 - i,  # Y position
                0
            ])
            for i in range(3)
        ])
        teaching_bubbles.next_to(demo_area, DOWN)

        with self.voiceover(text="""
            And more importantly, they could explain their findings to each other, 
            strengthening their teamwork...
        """):
            self.play(
                LaggedStart(*[
                    Create(bubble)
                    for bubble in teaching_bubbles
                ], lag_ratio=0.3),
                *[
                    method_boxes[i].animate.set_color(color)
                    for i, color in enumerate([
                        Colors.ADA_PURPLE,
                        Colors.MARCUS_GREEN,
                        Colors.MAYA_GOLD
                    ])
                ],
                run_time=2
            )

class RisingAction(BaseScene):
    def construct(self):
        # Create lab background
        lab = SVGMobject("assets/backgrounds/science_lab.svg")
        lab.set_width(config.frame_width)
        lab.set_height(config.frame_height)
        self.add(lab)

        # Create power effect indicators
        power_levels = VGroup(*[
            VGroup(
                Circle(radius=0.8, color=color, fill_opacity=0.2),
                Text(f"Power Level: {random.randint(60, 90)}%", 
                     color=color, font_size=24)
            ).arrange(DOWN, buff=0.2)
            for color in [Colors.ADA_PURPLE, Colors.MARCUS_GREEN, Colors.MAYA_GOLD]
        ]).arrange(RIGHT, buff=1)
        power_levels.to_edge(UP)

        with self.voiceover(text="""
            As their powers grew stronger, the team's control was put to the test...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(level)
                    for level in power_levels
                ], lag_ratio=0.3),
                *[
                    Flash(
                        level[0],
                        color=level[0].get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for level in power_levels
                ],
                run_time=2
            )

        # Create affected lab equipment
        equipment = VGroup(*[
            VGroup(
                Rectangle(height=0.8, width=0.4),  # Base
                Circle(radius=0.2),  # Display
                Arrow(DOWN, UP, color=Colors.TEXT_LIGHT)  # Reading indicator
            ).arrange(UP, buff=0.1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=1)
        equipment.next_to(power_levels, DOWN, buff=1)

        with self.voiceover(text="""
            The lab equipment began responding to their enhanced abilities...
        """):
            for eq in equipment:
                self.play(
                    FadeIn(eq),
                    eq[2].animate.scale(random.uniform(1.5, 2.0)),
                    eq.animate.set_color(Colors.NOVA_BLUE),
                    run_time=0.4
                )

        # Create Nova's approval effect
        nova_approval = VGroup(
            Circle(radius=1.2, color=Colors.NOVA_BLUE, fill_opacity=0.4),
            Circle(radius=0.8, color=Colors.NOVA_BLUE, fill_opacity=0.6),
            Text("Progress\nConfirmed", color=Colors.TEXT_LIGHT, font_size=24)
        )
        nova_approval[2].move_to(nova_approval[0])
        nova_approval.to_edge(RIGHT)

        with self.voiceover(text="""
            Nova's approval was clear - they were ready for the next phase...
        """):
            self.play(
                FadeIn(nova_approval, scale=1.2),
                *[
                    ShowPassingFlash(
                        Line(
                            eq.get_center(),
                            nova_approval.get_center(),
                            color=Colors.NOVA_BLUE
                        ),
                        time_width=0.5,
                        run_time=2
                    )
                    for eq in equipment
                ]
            )

class Complication(BaseScene):
    def construct(self):
        # Create power surge visualization
        surge_center = Circle(radius=2, color=Colors.NOVA_BLUE, fill_opacity=0.2)
        
        # Create warning indicators
        warnings = VGroup(*[
            Text("WARNING!", color=Colors.TEXT_LIGHT, font_size=36)
            for _ in range(4)
        ])
        
        for i, warning in enumerate(warnings):
            warning.rotate(i * PI/2)
            warning.shift(OUT * 2)
            warning.move_to(
                surge_center.point_from_proportion(i/4)
            )

        with self.voiceover(text="""
            Suddenly, a massive power surge threatened to overwhelm the lab...
        """):
            self.play(
                Create(surge_center),
                LaggedStart(*[
                    Write(warning)
                    for warning in warnings
                ], lag_ratio=0.2),
                run_time=2
            )

        # Create emergency containment measures
        containment_field = VGroup(*[
            Circle(
                radius=2 + i*0.3,
                color=Colors.TEXT_LIGHT,
                stroke_opacity=0.5
            )
            for i in range(3)
        ])

        # Create power readings
        readings = VGroup(*[
            Text(f"CRITICAL: {random.randint(90, 99)}%",
                 color=Colors.TEXT_LIGHT,
                 font_size=24)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.5)
        readings.to_edge(RIGHT)

        with self.voiceover(text="""
            Emergency containment protocols were activated, but time was running out...
        """):
            self.play(
                LaggedStart(*[
                    Create(field)
                    for field in containment_field
                ], lag_ratio=0.2),
                Write(readings),
                surge_center.animate.set_color(Colors.ADA_PURPLE),
                run_time=2
            )

        # Show containment struggle
        with self.voiceover(text="""
            The team had to act fast to prevent a catastrophic release of energy...
        """):
            for _ in range(2):
                self.play(
                    surge_center.animate.scale(1.2),
                    *[
                        field.animate.scale(1.1)
                        for field in containment_field
                    ],
                    run_time=1
                )
                self.play(
                    surge_center.animate.scale(1/1.2),
                    *[
                        field.animate.scale(1/1.1)
                        for field in containment_field
                    ],
                    run_time=1
                )

            # Show critical warning flash
            self.play(
                Flash(
                    surge_center,
                    color=Colors.ADA_PURPLE,
                    line_length=0.5,
                    flash_radius=1.0
                ),
                *[
                    reading.animate.set_color(Colors.ADA_PURPLE)
                    for reading in readings
                ],
                run_time=1
            )

class InnovativeSolution(BaseScene):
    def construct(self):
        # Create scientific method steps in circular arrangement
        method_circle = Circle(radius=2, color=Colors.TEXT_LIGHT)
        steps = VGroup(*[
            Text(step, color=Colors.TEXT_LIGHT, font_size=24)
            for step in [
                "Observe",
                "Question",
                "Hypothesize",
                "Experiment",
                "Analyze",
                "Conclude"
            ]
        ])

        for i, step in enumerate(steps):
            angle = i * TAU / len(steps)
            step.move_to(method_circle.point_from_proportion(i/len(steps)))

        with self.voiceover(text="""
            The team realized they needed to combine all aspects of the scientific method 
            in a new way...
        """):
            self.play(
                Create(method_circle),
                LaggedStart(*[
                    Write(step)
                    for step in steps
                ], lag_ratio=0.2),
                run_time=2
            )

        # Create power combination visualization
        powers = VGroup(
            Circle(radius=0.5, color=Colors.ADA_PURPLE),  # Time
            RegularPolygon(6, color=Colors.MARCUS_GREEN),  # Molecular
            Triangle(color=Colors.MAYA_GOLD)  # Geometric
        ).arrange(RIGHT, buff=1)
        powers.next_to(method_circle, DOWN, buff=1)

        with self.voiceover(text="""
            By synchronizing their powers with scientific principles...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(power, scale=1.2)
                    for power in powers
                ], lag_ratio=0.3),
                *[
                    Flash(
                        power,
                        color=power.get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for power in powers
                ],
                run_time=2
            )

        # Create stabilization effect
        stabilizer = VGroup(*[
            Circle(
                radius=1.5 + i*0.3,
                color=Colors.NOVA_BLUE,
                stroke_opacity=0.5
            )
            for i in range(3)
        ])
        stabilizer.move_to(powers)

        with self.voiceover(text="""
            They could create a stable containment field using lab equipment as power stabilizers...
        """):
            self.play(
                Create(stabilizer),
                *[
                    power.animate.scale(0.8)
                    for power in powers
                ],
                run_time=2
            )

            # Show energy flow
            for _ in range(2):
                self.play(
                    *[
                        ring.animate.scale(1.1)
                        for ring in stabilizer
                    ],
                    rate_func=there_and_back,
                    run_time=1
                )

class BuildUp(BaseScene):
    def construct(self):
        # Create lab background
        lab = SVGMobject("assets/backgrounds/science_lab.svg")
        lab.set_width(config.frame_width)
        lab.set_height(config.frame_height)
        self.add(lab)

        # Create final preparation elements
        prep_stations = VGroup(*[
            VGroup(
                Circle(radius=0.8, color=color),
                Text(label, color=color, font_size=24)
            ).arrange(DOWN, buff=0.2)
            for color, label in [
                (Colors.ADA_PURPLE, "Time Control"),
                (Colors.MARCUS_GREEN, "Molecular Balance"),
                (Colors.MAYA_GOLD, "Geometric Stability")
            ]
        ]).arrange(RIGHT, buff=2)
        prep_stations.to_edge(UP)

        with self.voiceover(text="""
            The team made their final preparations, each taking their position...
        """):
            self.play(
                LaggedStart(*[
                    FadeIn(station, shift=UP)
                    for station in prep_stations
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create power synchronization visualization
        sync_lines = VGroup(*[
            Line(
                prep_stations[i][0].get_center(),
                prep_stations[j][0].get_center(),
                color=Colors.NOVA_BLUE,
                stroke_opacity=0.6
            )
            for i in range(len(prep_stations))
            for j in range(i + 1, len(prep_stations))
        ])

        with self.voiceover(text="""
            Their powers began to synchronize, creating a harmonious energy field...
        """):
            self.play(
                Create(sync_lines),
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.TEXT_LIGHT),
                        time_width=0.5,
                        run_time=2
                    )
                    for line in sync_lines
                ],
                run_time=2
            )

        # Create tension building elements
        nova_energy = VGroup(
            Circle(radius=1.2, color=Colors.NOVA_BLUE, fill_opacity=0.4),
            Circle(radius=0.8, color=Colors.NOVA_BLUE, fill_opacity=0.6)
        )
        nova_energy.next_to(prep_stations, DOWN, buff=1)

        energy_readings = VGroup(*[
            Text(f"Energy Level: {random.randint(85, 95)}%",
                 color=Colors.TEXT_LIGHT,
                 font_size=24)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.5)
        energy_readings.to_edge(RIGHT)

        with self.voiceover(text="""
            Nova's energy grew stronger, testing the limits of their control...
        """):
            self.play(
                FadeIn(nova_energy),
                Write(energy_readings),
                *[
                    station[0].animate.scale(1.2)
                    for station in prep_stations
                ],
                run_time=2
            )

            # Show energy buildup
            for _ in range(2):
                self.play(
                    nova_energy.animate.scale(1.2),
                    *[
                        station[0].animate.scale(1.1)
                        for station in prep_stations
                    ],
                    rate_func=there_and_back,
                    run_time=1
                )

class PreClimax(BaseScene):
    def construct(self):
        # Create final obstacle visualization
        power_surge = Circle(radius=2, color=Colors.NOVA_BLUE, fill_opacity=0.3)
        power_surge.to_edge(LEFT)

        # Create team positions
        team_positions = VGroup(*[
            VGroup(
                Circle(radius=0.6, color=color),
                Text(label, color=color, font_size=24)
            ).arrange(DOWN, buff=0.2)
            for color, label in [
                (Colors.ADA_PURPLE, "Time"),
                (Colors.MARCUS_GREEN, "Molecular"),
                (Colors.MAYA_GOLD, "Geometric")
            ]
        ]).arrange(RIGHT, buff=2)
        team_positions.to_edge(RIGHT)

        with self.voiceover(text="""
            For their powers to work together perfectly, the team needed complete synchronization...
        """):
            self.play(
                Create(power_surge),
                LaggedStart(*[
                    FadeIn(position)
                    for position in team_positions
                ], lag_ratio=0.3),
                run_time=2
            )

        # Create synchronization effect
        sync_waves = VGroup(*[
            Circle(
                radius=0.8 + i*0.3,
                color=position[0].get_color(),
                stroke_opacity=0.5
            ).move_to(position[0])
            for i in range(3)
            for position in team_positions
        ])

        with self.voiceover(text="""
            Each member channeled their understanding of the scientific method...
        """):
            self.play(
                LaggedStart(*[
                    Create(wave)
                    for wave in sync_waves
                ], lag_ratio=0.1),
                *[
                    Flash(
                        position[0],
                        color=position[0].get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for position in team_positions
                ],
                run_time=2
            )

class ClimaxResolution(BaseScene):
    def construct(self):
        # Create central energy focus
        energy_core = VGroup(
            Circle(radius=2, color=Colors.NOVA_BLUE, fill_opacity=0.4),
            Circle(radius=1.5, color=Colors.NOVA_BLUE, fill_opacity=0.6),
            Circle(radius=1, color=Colors.NOVA_BLUE, fill_opacity=0.8)
        )

        # Create team power streams
        power_streams = VGroup(*[
            VGroup(
                Line(
                    START * 3,
                    ORIGIN,
                    color=color,
                    stroke_opacity=0.8
                ),
                *[
                    Circle(
                        radius=0.1,
                        color=color,
                        fill_opacity=0.8
                    ).move_to(Line(START * 3, ORIGIN).point_from_proportion(i/5))
                    for i in range(6)
                ]
            ).rotate(angle)
            for color, angle in [
                (Colors.ADA_PURPLE, 0),
                (Colors.MARCUS_GREEN, TAU/3),
                (Colors.MAYA_GOLD, 2*TAU/3)
            ]
        ])

        with self.voiceover(text="""
            In perfect harmony, their powers combined with scientific precision...
        """):
            self.play(
                Create(energy_core),
                LaggedStart(*[
                    Create(stream)
                    for stream in power_streams
                ], lag_ratio=0.2),
                run_time=2
            )

        # Create success indicators
        success_rings = VGroup(*[
            Circle(
                radius=2.5 + i*0.5,
                color=Colors.TEXT_LIGHT,
                stroke_opacity=0.6 - i*0.1
            )
            for i in range(4)
        ])

        with self.voiceover(text="""
            The energy stabilized, their control complete...
        """):
            self.play(
                LaggedStart(*[
                    Create(ring)
                    for ring in success_rings
                ], lag_ratio=0.2),
                energy_core.animate.scale(0.8),
                *[
                    stream.animate.scale(0.8)
                    for stream in power_streams
                ],
                run_time=2
            )

class EpilogueHook(BaseScene):
    def construct(self):
        # Create scientific method summary
        method_circle = Circle(radius=2, color=Colors.TEXT_LIGHT)
        steps = VGroup(*[
            Text(step, color=Colors.TEXT_LIGHT, font_size=24)
            for step in [
                "Observe",
                "Question",
                "Hypothesize",
                "Experiment",
                "Analyze",
                "Conclude"
            ]
        ])

        for i, step in enumerate(steps):
            angle = i * TAU / len(steps)
            step.move_to(method_circle.point_from_proportion(i/len(steps)))

        with self.voiceover(text="""
            Through the scientific method, they had mastered their extraordinary abilities...
        """):
            self.play(
                Create(method_circle),
                LaggedStart(*[
                    Write(step)
                    for step in steps
                ], lag_ratio=0.2),
                run_time=2
            )

        # Create team unity visualization
        team_symbol = VGroup(
            Circle(radius=1, color=Colors.ADA_PURPLE),
            RegularPolygon(6, color=Colors.MARCUS_GREEN),
            Triangle(color=Colors.MAYA_GOLD)
        ).arrange(RIGHT, buff=0.5)
        team_symbol.next_to(method_circle, DOWN, buff=1)

        with self.voiceover(text="""
            But this was just the beginning of their journey...
        """):
            self.play(
                FadeIn(team_symbol),
                *[
                    Flash(
                        symbol,
                        color=symbol.get_color(),
                        line_length=0.3,
                        flash_radius=0.6
                    )
                    for symbol in team_symbol
                ],
                run_time=2
            )

        # Create future challenge hint
        mystery_element = VGroup(
            Circle(radius=1.2, color=Colors.NOVA_BLUE, fill_opacity=0.4),
            Text("?", color=Colors.TEXT_LIGHT, font_size=72)
        )
        mystery_element[1].move_to(mystery_element[0])
        mystery_element.to_edge(RIGHT)

        with self.voiceover(text="""
            For Nova had revealed that an even greater challenge awaited...
        """):
            self.play(
                FadeIn(mystery_element, shift=LEFT),
                Flash(
                    mystery_element[0],
                    color=Colors.NOVA_BLUE,
                    line_length=0.4,
                    flash_radius=0.8
                ),
                run_time=2
            )

            # Final energy pulse
            self.play(
                *[
                    step.animate.set_color(Colors.NOVA_BLUE)
                    for step in steps
                ],
                method_circle.animate.set_color(Colors.NOVA_BLUE),
                *[
                    symbol.animate.set_color(Colors.NOVA_BLUE)
                    for symbol in team_symbol
                ],
                run_time=1.5
            )

class Episode1(BaseScene):
    def construct(self):
        # Create all scenes first
        scene_classes = [
            OpeningHook,
            TitleSequence,
            # ProblemIntroduction,
            # FirstAttempt,
            # LearningSequence,
            # TeamRegroup,
            # ResearchMontage,
            # BreakthroughMoment,
            # PlanFormation,
            # InitialTest,
            # BPlotEscalation,
            # TeamAdaptation,
            # SecondaryChallenge,
            # ConceptMastery,
            # RisingAction,
            # Complication,
            # InnovativeSolution,
            # BuildUp,
            # PreClimax,
            # ClimaxResolution,
            # EpilogueHook
        ]

        # Play each scene in sequence
        for i, SceneClass in enumerate(scene_classes):
            # Create a black screen transition
            if i > 0:
                self.clear()  # Clear previous scene
            
            # Create and run scene
            scene = SceneClass()
            scene_method = scene.construct.__get__(self, self.__class__)
            scene_method()  # Run the scene's construct method in our context
            
            self.wait(0.25)  # Wait between scenes

# Configure for 16:9 format
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920

class Colors:
    BACKGROUND = "#1A1A1A"
    NOVA_BLUE = "#29B6F6"
    ADA_PURPLE = "#9C27B0"
    MARCUS_GREEN = "#4CAF50"
    MAYA_GOLD = "#FFD700"
    TEXT_LIGHT = "#FFFFFF"

class ThoughtBubble(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        
        # Create main bubble
        main_bubble = Circle(
            radius=1 * scale_factor,
            fill_color=WHITE,
            fill_opacity=0.2,
            stroke_color=WHITE,
            stroke_width=2
        )
        
        # Create smaller bubbles
        small_bubbles = VGroup(*[
            Circle(
                radius=(0.2 - i*0.05) * scale_factor,
                fill_color=WHITE,
                fill_opacity=0.2,
                stroke_color=WHITE,
                stroke_width=2
            ).next_to(main_bubble, DL, buff=(-0.1 + i*0.1) * scale_factor)
            for i in range(3)
        ])
        
        # Add all parts to the thought bubble
        self.add(main_bubble, small_bubbles)
    
    def get_bubble_center(self):
        # Returns the center of the main bubble (first element)
        return self[0].get_center()

if __name__ == "__main__":
    # Set Manim configuration
    config.update({
        "quality": "high",
        "frame_rate": 60,
        "pixel_height": 1080,
        "pixel_width": 1920,
        "output_file": "episode_1",
        "preview": True,
        "format": "mp4",
        "write_to_movie": True
    })
    
    # Load environment variables and set OpenAI API key
    load_dotenv()
    
    # Create and render the scene directly
    scene = Episode1()
    scene.render() 