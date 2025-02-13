from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from dotenv import load_dotenv
import os
import random
import numpy as np

load_dotenv()

# Configure for 16:9 format
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920

class Colors:
    COD_BLUE = "#004B8D"
    COD_ORANGE = "#F7931D"
    ACCENT_GOLD = "#FFB74D"
    ACCENT_GREEN = "#4DB6AC"
    BG_DARK = "#1A1A1A"
    TEXT_LIGHT = "#FFFFFF"
    NSBE_BLUE = "#00008B"

class SmartCityInitiative(VoiceoverScene):
    def construct(self):
        self.set_speech_service(OpenAIService(
            voice="nova",
            api_key=os.getenv("OPENAI_API_KEY")
        ))

        # OPENING SCENE
        with self.voiceover(text="""
            Welcome to Community on Demand, where we're transforming college towns 
            into smart city laboratories for the future.
        """):
            # Create title with slower animation
            title = Text("Community on Demand", color=Colors.COD_BLUE)
            subtitle = Text("Smart City Initiative", color=Colors.COD_ORANGE).scale(0.7)
            title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
            
            # Slower title animation
            self.play(
                AnimationGroup(*[
                    Write(letter) 
                    for letter in title
                ], lag_ratio=0.2),  # Increased lag
                run_time=1.2  # Slower
            )
            
            self.play(
                FadeIn(subtitle, shift=UP * 0.3),
                run_time=0.8
            )
            
            self.play(
                title_group.animate.scale(0.8).to_edge(UP),
                run_time=0.7
            )

            # Create and position buildings
            buildings = VGroup()
            
            # Academic building (same setup as before)
            academic = VGroup(
                Triangle(color=Colors.COD_BLUE, fill_opacity=0.3),
                Rectangle(height=1.5, width=2, color=Colors.COD_BLUE, fill_opacity=0.3),
                *[
                    Square(side_length=0.3, color=Colors.COD_BLUE, fill_opacity=0.2)
                    for _ in range(4)
                ]
            ).arrange(UP, buff=0)
            
            # Position windows
            for i, window in enumerate(academic[2:]):
                window.move_to(academic[1].get_center() + 
                             RIGHT * (i%2 - 0.5) * 0.7 +
                             UP * (i//2 - 0.25) * 0.7)
            
            # Dorm buildings
            dorms = VGroup(*[
                VGroup(
                    Rectangle(
                        height=random.uniform(1.0, 1.5),
                        width=0.8,
                        color=Colors.COD_BLUE,
                        fill_opacity=0.3
                    ),
                    *[
                        Square(side_length=0.2, color=Colors.COD_BLUE, fill_opacity=0.2)
                        for _ in range(4)
                    ]
                ).arrange(UP, buff=0.1)
                for _ in range(3)
            ]).arrange(RIGHT, buff=1.5)  # More spacing
            
            buildings.add(academic, dorms)
            buildings.arrange(RIGHT, buff=3).center()  # More spacing
            
            # Slower building animation
            self.play(
                LaggedStart(*[
                    DrawBorderThenFill(building)
                    for building in buildings
                ], lag_ratio=0.3),  # More lag
                run_time=1.5
            )
            
            # Create smart city elements
            smart_layer = VGroup()
            
            # Connection points
            points = VGroup(*[
                Dot(radius=0.05, color=Colors.ACCENT_GOLD)
                for _ in range(8)
            ])
            
            # Better point positioning
            building_centers = [b.get_center() for b in buildings]
            for i, point in enumerate(points):
                if i < len(building_centers):
                    center = building_centers[i]
                    offset = [random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), 0]
                    point.move_to(center + offset)
                else:
                    x = random.uniform(-3, 3)
                    y = random.uniform(-1.5, 1.5)
                    point.move_to([x, y, 0])
            
            # Add points to smart layer
            smart_layer.add(points)
            
            # Slower point animation
            self.play(
                LaggedStart(*[
                    FadeIn(p, scale=1.5)
                    for p in points
                ], lag_ratio=0.2),
                run_time=1.0
            )

            # Create transformation label
            transform_label = VGroup(
                Text("College Towns", color=Colors.COD_BLUE),
                Text("→", color=Colors.COD_ORANGE),
                Text("Smart Cities", color=Colors.ACCENT_GREEN)
            ).arrange(RIGHT, buff=0.4).scale(0.7).to_edge(DOWN, buff=0.5)
            
            # Animate in the label
            self.play(
                Write(transform_label[0]),
                Write(transform_label[1]),
                Write(transform_label[2]),
                run_time=1.0
            )
            
            # Create connections
            connections = VGroup()
            for i, p1 in enumerate(points):
                for j, p2 in enumerate(points[i+1:], start=i+1):
                    if random.random() < 0.3:
                        line = Line(
                            p1.get_center(), 
                            p2.get_center(),
                            color=Colors.COD_ORANGE,
                            stroke_opacity=0.4
                        )
                        connections.add(line)
            
            smart_layer.add(connections)
            
            # Slower connection animation
            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in connections
                ], lag_ratio=0.2),
                buildings.animate.set_opacity(0.7),
                run_time=1.2
            )
            
            # Smart system indicators
            data_circles = VGroup(*[
                Circle(
                    radius=0.4,  # Slightly larger
                    color=Colors.ACCENT_GREEN,
                    stroke_opacity=0.5,
                    fill_opacity=0.1  # Added slight fill
                ).move_to(point.get_center())
                for point in points[::2]
            ])
            
            smart_layer.add(data_circles)
            
            # Slower circle animation
            self.play(
                LaggedStart(*[
                    Create(circle)
                    for circle in data_circles
                ], lag_ratio=0.2),
                run_time=1.0
            )
            
            # Continuous pulse effect that remains visible
            self.play(
                *[
                    circle.animate.scale(1.2).set_fill(opacity=0.2)
                    for circle in data_circles
                ],
                rate_func=there_and_back,
                run_time=1.0
            )
            
            # Keep the final state visible
            self.wait(0.5)

        # NSBE INTRODUCTION SCENE
        with self.voiceover(text="""
            Through National Society of Black Engineers chapters like Virginia State University's, student engineers are becoming the leaders
            who will transform their college towns into innovation hubs.
        """):
            # Completely clear previous scene except title
            self.play(
                *[
                    FadeOut(mob)
                    for mob in [buildings, smart_layer, transform_label]
                ],
                run_time=0.8
            )

            # Create student engineer that will grow/transform
            student = VGroup(
                Circle(radius=0.3, color=Colors.COD_BLUE, fill_opacity=0.3),  # Head
                Line(ORIGIN, DOWN, color=Colors.COD_BLUE),  # Body
                Line(UP * 0.5, UP * 0.5 + LEFT * 0.3, color=Colors.COD_BLUE),  # Arms
                Line(UP * 0.5, UP * 0.5 + RIGHT * 0.3, color=Colors.COD_BLUE),
            ).scale(0.8).move_to(LEFT * 3)

            # Create transformation elements
            graduation_cap = Polygon(
                LEFT * 0.2, RIGHT * 0.2, RIGHT * 0.2 + UP * 0.1, LEFT * 0.2 + UP * 0.1,
                color=Colors.COD_ORANGE,
                fill_opacity=0.8
            ).next_to(student[0], UP, buff=0.05)

            # Innovation symbols
            lightbulb = VGroup(
                Circle(radius=0.15, color=Colors.ACCENT_GOLD, fill_opacity=0.2),  # Bulb
                Line(DOWN * 0.15, DOWN * 0.3, color=Colors.ACCENT_GOLD),  # Base
            ).next_to(student, UP + RIGHT, buff=0.3)

            # Show initial student
            self.play(
                FadeIn(student, shift=UP),
                run_time=0.8
            )

            # Transform into leader
            self.play(
                student.animate.scale(1.3).move_to(ORIGIN),
                FadeIn(graduation_cap),
                FadeIn(lightbulb),
                run_time=1.0
            )

            # Create ripple effect of influence
            ripples = VGroup(*[
                Circle(
                    radius=0.5 + i*0.5,
                    stroke_width=2,
                    stroke_opacity=0.8 - i*0.2,
                    color=Colors.ACCENT_GREEN
                )
                for i in range(3)
            ]).move_to(student)

            # Animate ripples expanding
            self.play(
                *[
                    ripple.animate.scale(3).set_opacity(0)
                    for ripple in ripples
                ],
                run_time=1.5
            )

            # Create smaller engineers appearing around
            surrounding_engineers = VGroup(*[
                student.copy().scale(0.6).move_to(
                    [2*np.cos(angle), 2*np.sin(angle), 0]
                )
                for angle in np.linspace(0, TAU, 6)[:-1]
            ])

            # Add caps to surrounding engineers
            surrounding_caps = VGroup(*[
                graduation_cap.copy().scale(0.6).next_to(eng[0], UP, buff=0.05)
                for eng in surrounding_engineers
            ])

            # Show surrounding engineers emerging
            self.play(
                LaggedStart(*[
                    FadeIn(eng, scale=0.8)
                    for eng in surrounding_engineers
                ], lag_ratio=0.1),
                LaggedStart(*[
                    FadeIn(cap, scale=0.8)
                    for cap in surrounding_caps
                ], lag_ratio=0.1),
                run_time=1.2
            )

            # Create connection network
            connections = VGroup(*[
                Line(
                    student.get_center(),
                    eng.get_center(),
                    color=Colors.ACCENT_GOLD,
                    stroke_opacity=0.6
                )
                for eng in surrounding_engineers
            ])

            # Create NSBE label
            nsbe_label = Text("VSU NSBE: Tomorrow's Innovation Leaders", 
                            color=WHITE).scale(0.8)
            nsbe_label.to_edge(DOWN, buff=0.4)

            # Animate connections with data flow and add label
            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in connections
                ], lag_ratio=0.1),
                Write(nsbe_label),
                run_time=0.8
            )

            # Show innovation spreading
            self.play(
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.COD_ORANGE),
                        time_width=0.7,
                        run_time=1.5
                    )
                    for line in connections
                ],
                Flash(
                    lightbulb[0],
                    color=Colors.ACCENT_GOLD,
                    line_length=0.3,
                    num_lines=8,
                    flash_radius=0.3
                )
            )

        # SMART CITY CONCEPT SCENE
        with self.voiceover(text="""
            A smart city integrates technology into every aspect of urban life,
            making it more efficient, sustainable, and livable.
        """):
            # Clear previous scene while keeping title
            self.play(
                *[
                    FadeOut(mob)
                    for mob in [student, graduation_cap, lightbulb, surrounding_engineers, 
                              surrounding_caps, connections, nsbe_label]
                ],
                run_time=0.8
            )

            # Create base city infrastructure
            city_base = VGroup()
            
            # Create different sectors of city life
            sectors = {
                "Transportation": (LEFT * 3 + UP * 1.5, Colors.COD_BLUE),
                "Energy": (LEFT * 3 + DOWN * 1.5, Colors.ACCENT_GREEN),
                "Communication": (RIGHT * 3 + UP * 1.5, Colors.COD_ORANGE),
                "Housing": (RIGHT * 3 + DOWN * 1.5, Colors.ACCENT_GOLD)
            }

            sector_circles = VGroup()
            sector_icons = VGroup()
            sector_labels = VGroup()

            for name, (pos, color) in sectors.items():
                # Create sector circle
                circle = Circle(
                    radius=0.8,
                    color=color,
                    fill_opacity=0.2,
                    stroke_opacity=0.8
                ).move_to(pos)
                
                # Create unique icon for each sector
                if name == "Transportation":
                    icon = VGroup(
                        Rectangle(height=0.3, width=0.5),
                        Circle(radius=0.1).next_to(ORIGIN, LEFT),
                        Circle(radius=0.1).next_to(ORIGIN, RIGHT)
                    ).set_color(color).move_to(circle)
                elif name == "Energy":
                    # Create custom zigzag path for energy icon
                    zigzag = VMobject()
                    points = []
                    x = -0.3
                    y = 0
                    for i in range(4):
                        points.append([x, y, 0])
                        y = 0.2 if i % 2 == 0 else -0.2
                        x += 0.2
                    zigzag.set_points_as_corners(points)
                    
                    icon = VGroup(
                        zigzag,
                        Triangle(color=color).scale(0.3)
                    ).set_color(color).move_to(circle)
                elif name == "Communication":
                    icon = VGroup(
                        *[
                            Line(ORIGIN, UP * 0.4).rotate(angle)
                            for angle in [-PI/6, 0, PI/6]
                        ]
                    ).set_color(color).move_to(circle)
                else:  # Housing
                    icon = VGroup(
                        Triangle(color=color).scale(0.4),
                        Square(side_length=0.4, color=color)
                    ).arrange(UP, buff=0).move_to(circle)

                label = Text(name, color=color, font_size=24).next_to(circle, DOWN)
                
                sector_circles.add(circle)
                sector_icons.add(icon)
                sector_labels.add(label)

            # Create central hub
            hub = Circle(radius=1.2, color=Colors.COD_BLUE)
            hub_text = Text("Smart\nCity", color=Colors.COD_BLUE, font_size=32).move_to(hub)
            
            # Animate sectors appearing
            self.play(
                LaggedStart(*[
                    AnimationGroup(
                        FadeIn(circle, scale=1.2),
                        Write(label),
                        Create(icon)
                    )
                    for circle, label, icon in zip(sector_circles, sector_labels, sector_icons)
                ], lag_ratio=0.2),
                run_time=2
            )

            # Create and animate connections to central hub
            connections = VGroup(*[
                Line(
                    circle.get_center(),
                    hub.get_center(),
                    color=Colors.ACCENT_GOLD,
                    stroke_opacity=0.6
                ).set_stroke(width=2)
                for circle in sector_circles
            ])

            self.play(
                Create(hub),
                Write(hub_text),
                run_time=0.8
            )

            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in connections
                ], lag_ratio=0.1),
                run_time=1
            )

            # Show data flow between sectors
            data_paths = VGroup()
            for i, start_circle in enumerate(sector_circles):
                for end_circle in sector_circles[i+1:]:
                    path = CubicBezier(
                        start_circle.get_center(),
                        start_circle.get_center() + UP * 0.5,
                        end_circle.get_center() + UP * 0.5,
                        end_circle.get_center()
                    )
                    data_paths.add(path)

            # Animate data flow
            self.play(
                *[
                    ShowPassingFlash(
                        path.copy().set_color(Colors.ACCENT_GREEN),
                        time_width=0.7,
                        run_time=2
                    )
                    for path in data_paths
                ],
                # *[
                #     Flash(
                #         circle,
                #         color=circle.get_color(),
                #         line_length=0.2,
                #         num_lines=8,
                #         flash_radius=0.3,
                #         time_width=0.5
                #     )
                #     for circle in sector_circles
                # ],
                rate_func=linear
            )

            self.wait(0.5)

        # SMART CITY DEEP DIVE SCENE
        with self.voiceover(text="""
            A smart city is more than just connected technology. It's an ecosystem 
            where data and innovation work together to solve real community challenges.
        """):
            # Clear previous scene while keeping title
            self.play(
                *[
                    FadeOut(mob)
                    for mob in [sector_circles, sector_icons, sector_labels, 
                              hub, hub_text, connections, data_paths]
                ],
                run_time=0.8
            )

            # Create ecosystem representation
            ecosystem = VGroup()
            
            # Central brain/processor symbol
            processor = Square(
                side_length=1.2,
                color=Colors.COD_BLUE,
                fill_opacity=0.2
            ).move_to(ORIGIN)
            
            # Circuit patterns inside processor
            circuits = VGroup(*[
                Line(
                    processor.get_corner(UL) + RIGHT * 0.2 + DOWN * (i * 0.2),
                    processor.get_corner(UR) + LEFT * 0.2 + DOWN * (i * 0.2),
                    color=Colors.COD_ORANGE,
                    stroke_opacity=0.6
                )
                for i in range(4)
            ])
            
            ecosystem.add(processor, circuits)

            # Create data nodes around processor
            data_points = VGroup(*[
                Circle(
                    radius=0.3,
                    color=Colors.ACCENT_GOLD,
                    fill_opacity=0.2
                ).move_to([
                    2 * np.cos(angle),
                    2 * np.sin(angle),
                    0
                ])
                for angle in np.linspace(0, TAU, 6, endpoint=False)
            ])
            
            # Add challenge symbols to data points
            challenge_icons = VGroup()
            for i, point in enumerate(data_points):
                if i % 2 == 0:
                    icon = Text("!", color=Colors.ACCENT_GOLD).scale(0.4)
                else:
                    icon = Text("?", color=Colors.ACCENT_GOLD).scale(0.4)
                icon.move_to(point)
                challenge_icons.add(icon)
            
            ecosystem.add(data_points, challenge_icons)

            # Show ecosystem elements
            self.play(
                Create(processor),
                run_time=0.8
            )
            
            self.play(
                LaggedStart(*[
                    Create(circuit)
                    for circuit in circuits
                ], lag_ratio=0.1),
                run_time=1
            )
            
            # Add data points with ripple effect
            self.play(
                LaggedStart(*[
                    AnimationGroup(
                        FadeIn(point, scale=1.2),
                        FadeIn(icon, scale=1.2)
                    )
                    for point, icon in zip(data_points, challenge_icons)
                ], lag_ratio=0.2),
                run_time=1.2
            )

            # Create connections between processor and data points
            connections = VGroup(*[
                Line(
                    processor.get_center(),
                    point.get_center(),
                    color=Colors.COD_ORANGE,
                    stroke_opacity=0.4
                )
                for point in data_points
            ])
            
            self.play(
                LaggedStart(*[
                    Create(conn)
                    for conn in connections
                ], lag_ratio=0.1),
                run_time=0.8
            )

            # Show data processing animation
            self.play(
                *[
                    ShowPassingFlash(
                        conn.copy().set_color(Colors.ACCENT_GREEN),
                        time_width=0.5,
                        run_time=1.5
                    )
                    for conn in connections
                ],
                Flash(
                    processor,
                    color=Colors.ACCENT_GREEN,
                    line_length=0.2,
                    num_lines=8,
                    flash_radius=0.5
                )
            )

            # Transform challenge symbols to checkmarks
            solutions = VGroup(*[
                Text("✓", color=Colors.ACCENT_GREEN).scale(0.4).move_to(icon)
                for icon in challenge_icons
            ])
            
            self.play(
                LaggedStart(*[
                    Transform(icon, solution)
                    for icon, solution in zip(challenge_icons, solutions)
                ], lag_ratio=0.1),
                run_time=0.8
            )

        with self.voiceover(text="""
            From intelligent transportation systems that reduce congestion, to smart 
            energy grids that optimize power usage, to data-driven security networks 
            that enhance campus safety - every system becomes more efficient through 
            real-time data analysis.
        """):
            # Clear previous scene and fade out title
            self.play(
                *[
                    FadeOut(mob)
                    for mob in [ecosystem, processor, circuits, data_points, 
                              challenge_icons, connections, solutions, title_group]
                ],
                run_time=1.0
            )

            # Create three main systems positioned horizontally
            systems = VGroup()
            
            # Transportation System on left
            roads = VGroup(
                Line(LEFT * 2, RIGHT * 2, color=Colors.COD_BLUE),
                Line(LEFT * 2 + UP * 0.8, RIGHT * 2 + UP * 0.8, color=Colors.COD_BLUE),
                Line(LEFT * 2 + DOWN * 0.8, RIGHT * 2 + DOWN * 0.8, color=Colors.COD_BLUE),
            ).move_to(LEFT * 4)
            
            cars = VGroup(*[
                Square(side_length=0.3, color=Colors.COD_ORANGE)
                for _ in range(6)
            ])
            
            # Position cars on roads with more spacing
            for i, car in enumerate(cars):
                road_index = i % 3
                car.move_to(roads[road_index].point_from_proportion((i/6) + 0.1))
            
            transport_label = Text("Transportation", color=Colors.TEXT_LIGHT).scale(0.5)
            transport_label.next_to(roads, DOWN)
            transport_system = VGroup(roads, cars, transport_label)
            
            # Energy Grid System in middle
            grid_points = VGroup(*[
                Dot(color=Colors.ACCENT_GREEN)
                for _ in range(9)
            ]).arrange_in_grid(3, 3, buff=0.8).move_to(ORIGIN)
            
            grid_lines = VGroup()
            for i in range(len(grid_points)):
                for j in range(i + 1, len(grid_points)):
                    if abs(i//3 - j//3) <= 1 and abs(i%3 - j%3) <= 1:
                        line = Line(
                            grid_points[i].get_center(),
                            grid_points[j].get_center(),
                            color=Colors.ACCENT_GREEN,
                            stroke_opacity=0.4
                        )
                        grid_lines.add(line)
            
            energy_label = Text("Energy Grid", color=Colors.TEXT_LIGHT).scale(0.5)
            energy_label.next_to(grid_points, DOWN)
            energy_system = VGroup(grid_points, grid_lines, energy_label)
            
            # Security Network on right
            security_cams = VGroup(*[
                Triangle(color=Colors.ACCENT_GOLD, fill_opacity=0.3).scale(0.3)
                for _ in range(4)
            ]).arrange_in_grid(2, 2, buff=1.5).move_to(RIGHT * 4)
            
            coverage_areas = VGroup(*[
                Arc(
                    radius=0.8,
                    angle=PI/2,
                    color=Colors.ACCENT_GOLD,
                    stroke_opacity=0.2
                ).move_to(cam.get_center())
                for cam in security_cams
            ])
            
            security_label = Text("Security Network", color=Colors.TEXT_LIGHT).scale(0.5)
            security_label.next_to(security_cams, DOWN)
            security_system = VGroup(security_cams, coverage_areas, security_label)
            
            # Animate systems appearing sequentially with longer pauses
            self.play(
                Create(transport_system),
                run_time=1.2
            )
            
            self.wait(0.4)
            
            self.play(
                Create(energy_system),
                run_time=2
            )
            
            self.wait(0.4)
            
            self.play(
                Create(security_system),
                run_time=2
            )
            
            self.wait(1.4)
            
            # Show synchronized data analysis effect
            self.play(
                *[
                    Flash(
                        system,
                        color=Colors.ACCENT_GREEN,
                        line_length=0.3,
                        flash_radius=0.5,
                        num_lines=8
                    )
                    for system in [transport_system, energy_system, security_system]
                ],
                *[
                    system.animate.set_color(Colors.ACCENT_GREEN)
                    for system in [transport_system, energy_system, security_system]
                ],
                run_time=2
            )
            
            self.wait(1)
            
            # Show synchronized optimization effects with longer duration
            self.play(
                *[
                    car.animate.shift(RIGHT * 0.5)
                    for car in cars
                ],
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.COD_ORANGE),
                        time_width=0.8,
                        run_time=2.0
                    )
                    for line in grid_lines
                ],
                *[
                    area.animate.scale(1.2).set_opacity(0.4)
                    for area in coverage_areas
                ],
                run_time=2.0
            )
            
            # Add extra animation to fill remaining voiceover time
            self.play(
                *[
                    Flash(
                        label,
                        color=Colors.ACCENT_GOLD,
                        line_length=0.2,
                        flash_radius=0.3,
                        num_lines=6
                    )
                    for label in [transport_label, energy_label, security_label]
                ],
                run_time=1.0
            )

        with self.voiceover(text="""
            But the true power of a smart city comes from integration. When these 
            systems talk to each other, we create solutions that weren't possible before.
        """):
            # Create connection lines between systems
            system_connections = VGroup(*[
                Line(
                    start=system1.get_center(),
                    end=system2.get_center(),
                    color=Colors.ACCENT_GOLD,
                    stroke_opacity=0.6
                )
                for system1, system2 in [
                    (transport_system, energy_system),
                    (energy_system, security_system),
                    (security_system, transport_system)
                ]
            ])

            # Show systems connecting
            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in system_connections
                ], lag_ratio=0.3),
                run_time=1.2
            )

            # Create data flow particles
            particles = VGroup(*[
                Dot(
                    radius=0.05,
                    color=Colors.COD_ORANGE,
                    fill_opacity=0.8
                ).move_to(line.get_start())
                for line in system_connections
            ])

            # Animate data flowing between systems
            self.play(
                *[
                    MoveAlongPath(
                        particle,
                        line,
                        rate_func=linear
                    )
                    for particle, line in zip(particles, system_connections)
                ],
                run_time=1.5
            )

            # Show optimization flash effect
            self.play(
                *[
                    Flash(
                        system,
                        color=Colors.ACCENT_GREEN,
                        line_length=0.4,
                        flash_radius=0.6,
                        num_lines=10
                    )
                    for system in [transport_system, energy_system, security_system]
                ],
                run_time=1
            )

            # Create synergy effect
            synergy_circle = Circle(
                radius=3,
                color=Colors.ACCENT_GOLD,
                stroke_opacity=0.4,
                fill_opacity=0.1
            )

            self.play(
                Create(synergy_circle),
                *[
                    system.animate.set_color(Colors.ACCENT_GOLD)
                    for system in [transport_system, energy_system, security_system]
                ],
                run_time=1
            )

            # Pulse effect showing systems working together
            self.play(
                synergy_circle.animate.scale(1.2).set_opacity(0.2),
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.COD_ORANGE),
                        time_width=0.7,
                        run_time=2
                    )
                    for line in system_connections
                ],
                rate_func=there_and_back,
                run_time=1.5
            )

        # ENGINEERING LEADERSHIP SCENE
        with self.voiceover(text="""
            This is where you, as student engineers, become vital. Your understanding 
            of both technology and community needs puts you in a unique position to 
            lead this transformation.
        """):
            # Clear previous scene while keeping title
            self.play(
                *[
                    FadeOut(mob) 
                    for mob in [synergy_circle, transport_system, energy_system, 
                              security_system, system_connections, particles]
                ],
                run_time=0.8
            )

            # Create central student engineer
            student = VGroup(
                Circle(radius=0.3, color=Colors.COD_BLUE, fill_opacity=0.3),  # Head
                Line(ORIGIN, DOWN, color=Colors.COD_BLUE),  # Body
                Line(UP * 0.5, UP * 0.5 + LEFT * 0.3, color=Colors.COD_BLUE),  # Arms
                Line(UP * 0.5, UP * 0.5 + RIGHT * 0.3, color=Colors.COD_BLUE),
            ).scale(1.2).move_to(ORIGIN)

            student_label = Text("Student Engineer", color=Colors.TEXT_LIGHT).scale(0.4)
            student_label.next_to(student, DOWN, buff=0.3)
            student_group = VGroup(student, student_label)

            # Create thought bubbles showing technical and community understanding
            tech_bubble = Circle(radius=0.8, color=Colors.ACCENT_GREEN, fill_opacity=0.2)
            tech_label = Text("Technical Skills", color=Colors.ACCENT_GREEN).scale(0.4)
            tech_bubble.move_to(LEFT * 3)
            tech_label.next_to(tech_bubble, UP, buff=0.3)
            
            community_bubble = Circle(radius=0.8, color=Colors.COD_ORANGE, fill_opacity=0.2)
            community_label = Text("Community Needs", color=Colors.COD_ORANGE).scale(0.4)
            community_bubble.move_to(RIGHT * 3)
            community_label.next_to(community_bubble, UP, buff=0.3)

            # Add icons inside bubbles
            tech_icon = VGroup(
                Rectangle(height=0.4, width=0.4),  # Computer screen
                Rectangle(height=0.1, width=0.5)   # Computer base
            ).arrange(DOWN, buff=0.05).move_to(tech_bubble)

            community_icon = VGroup(*[
                Circle(radius=0.1)  # People
                for _ in range(3)
            ]).arrange(RIGHT, buff=0.1).move_to(community_bubble)

            # Show student appearing
            self.play(
                FadeIn(student_group, shift=UP),
                run_time=0.8
            )

            # Show thought bubbles and labels emerging with better timing
            self.play(
                FadeIn(tech_bubble),
                FadeIn(tech_icon),
                run_time=0.6
            )
            self.play(
                FadeIn(tech_label, shift=DOWN),
                run_time=0.4
            )
            
            self.play(
                FadeIn(community_bubble),
                FadeIn(community_icon),
                run_time=0.6
            )
            self.play(
                FadeIn(community_label, shift=DOWN),
                run_time=0.4
            )

            # Create connection between bubbles through student
            connections = VGroup(
                CurvedArrow(
                    tech_bubble.get_right(),
                    student.get_left(),
                    color=Colors.ACCENT_GREEN,
                    angle=-TAU/6
                ),
                CurvedArrow(
                    community_bubble.get_left(),
                    student.get_right(),
                    color=Colors.COD_ORANGE,
                    angle=TAU/6
                )
            )

            # Show connections forming
            self.play(
                Create(connections),
                run_time=1.0
            )

            # Show synthesis effect
            glow = Circle(
                radius=0.5,
                color=Colors.ACCENT_GOLD,
                fill_opacity=0.3,
                stroke_opacity=0.8
            ).move_to(student.get_top())

            synthesis_label = Text("Leadership\nSynthesis", color=Colors.ACCENT_GOLD).scale(0.4)
            synthesis_label.next_to(glow, UP, buff=0.3)

            self.play(
                FadeIn(glow),
                FadeIn(synthesis_label, shift=DOWN),
                Flash(
                    glow,
                    color=Colors.ACCENT_GOLD,
                    line_length=0.3,
                    flash_radius=0.5,
                    num_lines=12
                ),
                run_time=1.0
            )

        # PRACTICAL IMPLEMENTATION SCENE
        with self.voiceover(text="""
            Starting with campus projects like smart parking and energy monitoring, 
            you'll develop solutions that can scale to entire communities. Each project 
            becomes a stepping stone toward larger innovations.
        """):
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in [tech_bubble, tech_icon, community_bubble, 
                                         community_icon, connections, glow, student,
                                         tech_label, community_label, synthesis_label, student_group, student_label]],
                run_time=0.8
            )

            # Create initial small campus project icons with labels on left side
            parking_group = VGroup()
            parking_icon = VGroup(
                Rectangle(height=0.6, width=0.8, color=Colors.COD_BLUE, fill_opacity=0.3),
                Text("P", color=Colors.TEXT_LIGHT).scale(0.4)
            )
            parking_label = Text("Smart Parking", color=Colors.COD_BLUE).scale(0.5)
            parking_label.next_to(parking_icon, DOWN, buff=0.2)
            parking_group.add(parking_icon, parking_label).move_to(LEFT * 5 + UP * 1.5)

            energy_group = VGroup()
            energy_icon = VGroup(
                Circle(radius=0.3, color=Colors.ACCENT_GREEN, fill_opacity=0.3),
                Polygon(UP*0.2, RIGHT*0.2, DOWN*0.2, LEFT*0.2, 
                       color=Colors.ACCENT_GREEN)
            )
            energy_label = Text("Energy Monitoring", color=Colors.ACCENT_GREEN).scale(0.5)
            energy_label.next_to(energy_icon, DOWN, buff=0.2)
            energy_group.add(energy_icon, energy_label).move_to(LEFT * 5 + DOWN * 1.5)

            # Show initial small projects appearing with labels
            self.play(
                FadeIn(parking_group, shift=RIGHT),
                FadeIn(energy_group, shift=RIGHT),
                run_time=1.0
            )

            # Create community buildings in center-right area
            buildings = VGroup()
            for i in range(3):
                for j in range(2):
                    building = Rectangle(
                        height=random.uniform(1.0, 1.4),
                        width=0.7,
                        color=Colors.COD_ORANGE,
                        fill_opacity=0.3
                    ).move_to([j*2 + 1, 2 - i*2, 0])
                    buildings.add(building)

            # Add "Community" label above buildings
            community_label = Text("Growing Community", color=Colors.COD_ORANGE).scale(0.7)
            community_label.next_to(buildings, UP, buff=0.7)
            
            # Show buildings appearing with label
            self.play(
                FadeIn(community_label),
                LaggedStart(*[
                    FadeIn(building, scale=0.8)
                    for building in buildings
                ], lag_ratio=0.15),
                run_time=1.2
            )

            # Create connection arrows from projects to buildings
            connections = VGroup()
            for building in buildings:
                # Create curved arrows from each project to buildings
                connections.add(
                    CurvedArrow(
                        parking_icon.get_right(),
                        building.get_left(),
                        color=Colors.ACCENT_GREEN,
                        angle=-TAU/8,
                        stroke_opacity=0.6
                    ),
                    CurvedArrow(
                        energy_icon.get_right(),
                        building.get_left(),
                        color=Colors.ACCENT_GREEN,
                        angle=TAU/8,
                        stroke_opacity=0.6
                    )
                )

            # Show connections forming with data flow
            self.play(
                LaggedStart(*[
                    Create(conn)
                    for conn in connections
                ], lag_ratio=0.05),
                run_time=1.2
            )

            # Add scaling effect with expanding circles
            scale_indicators = VGroup(*[
                Circle(
                    radius=0.3,
                    color=Colors.ACCENT_GOLD,
                    stroke_opacity=0.8,
                    fill_opacity=0.1
                ).move_to(building.get_center())
                for building in buildings
            ])

            # Show scaling effect with expanding circles
            self.play(
                LaggedStart(*[
                    Succession(
                        FadeIn(circle),
                        circle.animate.scale(2).set_opacity(0)
                    )
                    for circle in scale_indicators
                ], lag_ratio=0.2),
                *[
                    ShowPassingFlash(
                        conn.copy().set_color(Colors.COD_ORANGE),
                        time_width=0.6,
                        run_time=1.5
                    )
                    for conn in connections
                ],
                run_time=2
            )

        # FUTURE IMPACT SCENE
        with self.voiceover(text="""
            As you develop these solutions, you're not just improving campus life - 
            you're creating blueprints that other universities and communities can follow.
            This is how student engineers become community leaders.
        """):
            # Clear all previous elements
            self.play(
                *[
                    FadeOut(mob)
                    for mob in [buildings, connections, scale_indicators, energy_icon, 
                              energy_group, parking_group, energy_label, community_label]
                ],
                run_time=0.8
            )

            # Create central campus icon
            campus = VGroup(
                Rectangle(height=1.5, width=2, color=Colors.COD_BLUE, fill_opacity=0.3),
                Triangle(color=Colors.COD_BLUE, fill_opacity=0.3).scale(0.8)
                    .next_to(Rectangle(height=1.5, width=2), UP, buff=0)
            ).scale(0.8).move_to(ORIGIN)

            campus_label = Text("Your Campus", color=Colors.COD_BLUE).scale(0.4)
            campus_label.next_to(campus, DOWN)
            campus_group = VGroup(campus, campus_label)

            # Create surrounding community icons that will appear
            communities = VGroup(*[
                campus.copy().scale(0.6).set_color(Colors.ACCENT_GOLD).move_to(
                    [3*np.cos(angle), 3*np.sin(angle), 0]
                )
                for angle in np.linspace(0, TAU, 7)[:-1]  # 6 surrounding communities
            ])

            community_labels = VGroup(*[
                Text(f"Community {i+1}", color=Colors.ACCENT_GOLD).scale(0.3)
                .next_to(community, DOWN)
                for i, community in enumerate(communities)
            ])

            # Show central campus with label
            self.play(
                FadeIn(campus_group, scale=1.2),
                run_time=0.8
            )

            # Create blueprint effect
            blueprint_lines = VGroup(*[
                DashedLine(
                    campus.get_center(),
                    community.get_center(),
                    dash_length=0.15,
                    color=Colors.COD_ORANGE,
                    stroke_opacity=0.6
                )
                for community in communities
            ])

            blueprint_label = Text("Innovation Blueprints", color=Colors.COD_ORANGE).scale(0.4)
            blueprint_label.to_edge(UP)

            # Show blueprint lines spreading with label
            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in blueprint_lines
                ], lag_ratio=0.2),
                FadeIn(blueprint_label),
                run_time=1.2
            )

            # Show communities appearing along blueprints
            self.play(
                LaggedStart(*[
                    AnimationGroup(
                        FadeIn(community, scale=0.8),
                        FadeIn(label)
                    )
                    for community, label in zip(communities, community_labels)
                ], lag_ratio=0.15),
                run_time=1.5
            )

            # Create interconnecting network
            network_lines = VGroup(*[
                Line(
                    communities[i].get_center(),
                    communities[(i+1)%6].get_center(),
                    color=Colors.ACCENT_GREEN,
                    stroke_opacity=0.4
                )
                for i in range(6)
            ])

            network_label = Text("Collaboration Network", color=Colors.ACCENT_GREEN).scale(0.4)
            network_label.to_edge(DOWN)

            # Show network forming with label
            self.play(
                LaggedStart(*[
                    Create(line)
                    for line in network_lines
                ], lag_ratio=0.1),
                FadeIn(network_label),
                run_time=1.0
            )

            # Animate data/innovation flow
            self.play(
                *[
                    ShowPassingFlash(
                        line.copy().set_color(Colors.COD_ORANGE),
                        time_width=0.5,
                        run_time=2
                    )
                    for line in [*blueprint_lines, *network_lines]
                ],
                *[
                    Flash(
                        community,
                        color=Colors.ACCENT_GOLD,
                        line_length=0.2,
                        num_lines=8,
                        flash_radius=0.4
                    )
                    for community in communities
                ],
                run_time=2
            )

        # CALL TO ACTION SCENE - GRAND FINALE
        with self.voiceover(text="""
            Your college town is your laboratory, and through Community on Demand, 
            you have the platform to turn your innovative ideas into real-world solutions. 
            The future of smart cities starts with you.
        """):
            # Dramatic transition - spiral out previous elements
            old_mobjects = self.mobjects.copy()
            self.play(
                *[
                    mob.animate.scale(0.1).rotate(2*PI).set_opacity(0)
                    for mob in old_mobjects
                ],
                run_time=1.2
            )
            self.clear()

            # Create bold title that stays throughout scene
            title = Text("BE THE CHANGE", color=Colors.ACCENT_GOLD).scale(1.0)
            subtitle = Text("Shape Tomorrow's Cities Today", color=Colors.TEXT_LIGHT).scale(0.5)
            title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.8)
            
            self.play(
                Write(title, run_time=0.8),
                FadeIn(subtitle, shift=UP, run_time=0.6)
            )

            # Create larger, more prominent student figure center-left
            student = VGroup(
                Circle(radius=0.3, color=Colors.COD_BLUE, fill_opacity=0.4),  # Head
                Line(ORIGIN, DOWN*1.0, color=Colors.COD_BLUE),  # Body
                Line(UP * 0.5, UP * 0.5 + LEFT * 0.3, color=Colors.COD_BLUE),  # Arms
                Line(UP * 0.5, UP * 0.5 + RIGHT * 0.3, color=Colors.COD_BLUE),
            ).scale(1.2).move_to(LEFT * 4)
            
            student_label = Text("YOU", color=Colors.COD_BLUE, weight=BOLD).scale(0.6)
            student_label.next_to(student, DOWN, buff=0.4)
            student_group = VGroup(student, student_label)

            # Create larger vision bubble with more detailed city concept
            vision_bubble = Circle(radius=1.8, color=Colors.ACCENT_GOLD, fill_opacity=0.15)
            vision_bubble.move_to(RIGHT * 2)
            vision_label = Text("TOMORROW'S CITY", color=Colors.ACCENT_GOLD, weight=BOLD).scale(0.6)
            vision_label.next_to(vision_bubble, UP, buff=0.4)
            
            # More detailed smart city visualization inside bubble
            buildings = VGroup(*[
                Rectangle(
                    height=random.uniform(0.5, 1.0),
                    width=0.3,
                    color=Colors.COD_ORANGE,
                    fill_opacity=0.3
                ).shift(RIGHT * i * 0.4 - RIGHT * 1.0)
                for i in range(6)
            ]).move_to(vision_bubble)

            # Add tech elements to buildings
            tech_dots = VGroup(*[
                Dot(color=Colors.ACCENT_GREEN, radius=0.04)
                for _ in range(8)
            ]).arrange_in_grid(rows=2, cols=4, buff=0.3)
            tech_dots.move_to(vision_bubble)

            # Create dynamic platform base
            platform = Rectangle(
                height=1.0,
                width=7,
                color=Colors.ACCENT_GREEN,
                fill_opacity=0.3,
                stroke_width=2
            ).to_edge(DOWN, buff=1.0)
            platform_text = Text("COMMUNITY ON DEMAND", color=Colors.TEXT_LIGHT, weight=BOLD).scale(0.6)
            platform_subtext = Text("Your Innovation Platform", color=Colors.ACCENT_GREEN).scale(0.4)
            platform_text_group = VGroup(platform_text, platform_subtext).arrange(DOWN, buff=0.15)
            platform_text_group.move_to(platform)
            platform_group = VGroup(platform, platform_text_group)

            # Dramatic entrance animations
            self.play(
                FadeIn(student_group, shift=UP*1.2, scale=1.1),
                run_time=1.0
            )

            self.play(
                Create(vision_bubble),
                Write(vision_label),
                run_time=1.0
            )
            
            self.play(
                LaggedStart(*[
                    GrowFromCenter(building)
                    for building in buildings
                ], lag_ratio=0.1),
                FadeIn(tech_dots),
                run_time=1.2
            )

            self.play(
                FadeIn(platform_group, shift=UP*0.4, scale=1.1),
                run_time=1.0
            )

            # Create dynamic connecting arrows with gradients
            arrows = VGroup(
                Arrow(student.get_right(), vision_bubble.get_left(), 
                      color=Colors.ACCENT_GREEN, stroke_width=3),
                Arrow(student_label.get_bottom(), platform.get_left(), 
                      color=Colors.ACCENT_GREEN, stroke_width=3)
            )

            self.play(
                Create(arrows),
                run_time=0.8
            )

            # Final powerful flourish
            self.play(
                *[
                    ShowPassingFlash(
                        arrow.copy().set_color(Colors.COD_ORANGE).set_stroke(width=5),
                        time_width=0.8,
                        run_time=2
                    )
                    for arrow in arrows
                ],
                *[
                    Flash(
                        mob,
                        color=Colors.ACCENT_GOLD,
                        line_length=0.3,
                        flash_radius=0.6,
                        num_lines=12
                    )
                    for mob in [vision_bubble, platform]
                ],
                tech_dots.animate.shift(UP*0.15).set_color(Colors.ACCENT_GOLD),
                rate_func=there_and_back,
                run_time=2
            )

        # Continue with next scene... 