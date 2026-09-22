import os
import math
import random
import tkinter as tk
import webbrowser
import subprocess
import platform

from datetime import datetime
from PIL import Image, ImageTk, ImageEnhance


class Dashboard:
    def __init__(self):
        # ============================================================
        # WINDOW
        # ============================================================
        self.root = tk.Tk()
        self.root.title("AVNI 2.1")
        self.root.geometry("900x700")
        self.root.minsize(1150, 720)
        self.root.configure(bg="#020617")

        self.root.bind("<Escape>", lambda e: self.close())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # ============================================================
        # COLORS
        # ============================================================
        self.bg = "#020617"
        self.bg2 = "#030b24"
        self.panel = "#071334"
        self.panel2 = "#081947"
        self.panel_dark = "#030b24"

        self.blue = "#008cff"
        self.cyan = "#00eaff"
        self.purple = "#a855ff"
        self.pink = "#ff4dff"
        self.green = "#00ffd5"
        self.yellow = "#ffe66d"
        self.red = "#ff5577"

        self.text = "#f4f7ff"
        self.subtext = "#8db4ff"
        self.muted = "#5571ad"

        # ============================================================
        # STATE
        # ============================================================
        self.current_state = "IDLE"
        self.running = True
        self.fullscreen = False

        self.anim_tick = 0
        self.wave_phase = 0
        self.rotation = 0
        self.pulse = 0

        self.hologram_image = None
        self.hologram_photo = None

        self.particles = []

        # ============================================================
        # ROOT GRID
        # ============================================================
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_main_layout()

        self.create_greeting()
        self.create_status()
        self.create_clock()
        self.create_quick_actions()
        self.create_message_panel()
        self.create_waveform()

        self.create_background_particles()

        self.update_clock()
        self.animate()

    # ================================================================
    # HEADER
    # ================================================================
    def create_header(self):
        self.header = tk.Frame(
            self.root,
            bg=self.bg2,
            height=75
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        self.header.grid_propagate(False)

        # Logo
        logo_frame = tk.Frame(
            self.header,
            bg=self.bg2
        )
        logo_frame.pack(
            side="left",
            padx=30
        )

        tk.Label(
            logo_frame,
            text="AVNI",
            font=("Segoe UI", 24, "bold"),
            fg=self.text,
            bg=self.bg2
        ).pack(side="left")

        tk.Label(
            logo_frame,
            text="  2.1",
            font=("Segoe UI", 18, "bold"),
            fg=self.purple,
            bg=self.bg2
        ).pack(side="left", pady=(0,0))

        # Center title
        tk.Label(
            self.header,
            text="AUTONOMOUS VOICE NEURAL INTELLIGENCE",
            font=("Segoe UI", 12, "bold"),
            fg=self.subtext,
            bg=self.bg2
        ).pack(
            side="left",
            padx=20
        )

        # Right side
        right = tk.Frame(
            self.header,
            bg=self.bg2
        )
        right.pack(
            side="right",
            padx=30
        )

        self.connection_dot = tk.Label(
            right,
            text="●",
            font=("Segoe UI", 12),
            fg=self.green,
            bg=self.bg2
        )
        self.connection_dot.pack(side="left")

        tk.Label(
            right,
            text=" SYSTEM ONLINE",
            font=("Segoe UI", 9, "bold"),
            fg=self.green,
            bg=self.bg2
        ).pack(side="left")

    # ================================================================
    # MAIN LAYOUT
    # ================================================================
    def create_main_layout(self):
        self.main = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.main.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(8, 18)
        )

        self.main.grid_columnconfigure(0, minsize=350)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, minsize=350)

        self.main.grid_rowconfigure(0, weight=1)

        # LEFT
        self.left_panel = tk.Frame(
            self.main,
            bg=self.bg
        )
        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # CENTER
        self.center_frame = tk.Frame(
            self.main,
            bg=self.bg
        )
        self.center_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        # RIGHT
        self.right_panel = tk.Frame(
            self.main,
            bg=self.bg
        )
        self.right_panel.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        # ============================================================
        # IMPORTANT:
        # One single Canvas for ALL center graphics.
        # ============================================================
        self.center_canvas = tk.Canvas(
            self.center_frame,
            bg=self.bg,
            highlightthickness=0,
            bd=0
        )

        self.center_canvas.pack(
            fill="both",
            expand=True
        )

        self.center_canvas.bind(
            "<Configure>",
            self.on_canvas_resize
        )

    # ================================================================
    # GREETING
    # ================================================================
    def create_greeting(self):
        card = tk.Frame(
            self.left_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            card,
            text="WELCOME",
            font=("Segoe UI", 9, "bold"),
            fg=self.cyan,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 4)
        )

        tk.Label(
            card,
            text="Roushan",
            font=("Segoe UI", 25, "bold"),
            fg=self.text,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=22
        )

        tk.Label(
            card,
            text="Your personal AI command center",
            font=("Segoe UI", 10),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=22,
            pady=(3, 20)
        )

    # ================================================================
    # STATUS
    # ================================================================
    def create_status(self):
        card = tk.Frame(
            self.left_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=6
        )

        tk.Label(
            card,
            text="AVNI STATUS",
            font=("Segoe UI", 9, "bold"),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 8)
        )

        self.status_label = tk.Label(
            card,
            text="●  IDLE",
            font=("Segoe UI", 17, "bold"),
            fg=self.green,
            bg=self.panel
        )
        self.status_label.pack(
            anchor="w",
            padx=20
        )

        self.status_description = tk.Label(
            card,
            text="Waiting for your command...",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.panel
        )
        self.status_description.pack(
            anchor="w",
            padx=20,
            pady=(3, 16)
        )

        # Status buttons
        buttons = tk.Frame(
            card,
            bg=self.panel
        )
        buttons.pack(
            fill="x",
            padx=16,
            pady=(0, 16)
        )

        states = [
            ("IDLE", self.green),
            ("LISTENING", self.cyan),
            ("THINKING", self.purple),
            ("SPEAKING", self.pink)
        ]

        for state, color in states:
            tk.Button(
                buttons,
                text=state,
                command=lambda s=state: self.set_state(s),
                font=("Segoe UI", 8, "bold"),
                fg=color,
                bg=self.panel2,
                activeforeground=self.text,
                activebackground="#10265b",
                relief="flat",
                bd=0,
                padx=8,
                pady=7,
                cursor="hand2"
            ).pack(
                side="left",
                padx=3,
                expand=True,
                fill="x"
            )

    # ================================================================
    # HOLOGRAM
    # ================================================================
    def create_hologram(self):
        self.load_hologram()

        # Canvas handles everything in the center.
        self.center_canvas.bind(
            "<Configure>",
            self.resize_hologram
        )

    def load_hologram(self):
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "hologram.jpeg"
        )

        if not os.path.exists(image_path):
            print("hologram.jpeg not found - using AVNI hologram fallback.")
            return

        try:
            image = Image.open(image_path).convert("RGBA")

            image = ImageEnhance.Color(image).enhance(1.25)
            image = ImageEnhance.Contrast(image).enhance(1.15)
            image = ImageEnhance.Brightness(image).enhance(0.9)

            self.hologram_image = image

        except Exception as e:
            print("Could not load hologram.jpeg:", e)
            self.hologram_image = None

    def resize_hologram(self, event=None):
        self.draw_scene()

    # ================================================================
    # CLOCK
    # ================================================================
    def create_clock(self):
        card = tk.Frame(
            self.right_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            card,
            text="LOCAL SYSTEM TIME",
            font=("Segoe UI", 9, "bold"),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 5)
        )

        self.time_label = tk.Label(
            card,
            text="00:00:00",
            font=("Consolas", 28, "bold"),
            fg=self.cyan,
            bg=self.panel
        )
        self.time_label.pack(
            anchor="w",
            padx=20
        )

        self.date_label = tk.Label(
            card,
            text="Loading...",
            font=("Segoe UI", 10),
            fg=self.text,
            bg=self.panel
        )
        self.date_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 16)
        )

    def update_clock(self):
        if not self.running:
            return

        now = datetime.now()

        self.time_label.config(
            text=now.strftime("%H:%M:%S")
        )

        self.date_label.config(
            text=now.strftime("%A, %d %B %Y")
        )

        self.root.after(
            1000,
            self.update_clock
        )

    # ================================================================
    # QUICK ACTIONS
    # ================================================================
    def create_quick_actions(self):
        card = tk.Frame(
            self.right_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=6
        )

        tk.Label(
            card,
            text="QUICK ACTIONS",
            font=("Segoe UI", 9, "bold"),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 10)
        )

        actions = [
            ("🌐  Open Browser", self.open_browser),
            ("🎵  Play Music", self.play_music),
            ("☁  Check Weather", self.check_weather),
            ("📝  Open Notepad", self.open_notepad),
            ("⚙  System Info", self.system_info)
        ]

        for text, command in actions:
            btn = tk.Button(
                card,
                text=text,
                command=command,
                font=("Segoe UI", 10, "bold"),
                fg=self.text,
                bg=self.panel2,
                activeforeground=self.cyan,
                activebackground="#10265b",
                relief="flat",
                bd=0,
                anchor="w",
                padx=16,
                pady=10,
                cursor="hand2"
            )

            btn.pack(
                fill="x",
                padx=14,
                pady=3
            )

        tk.Label(
            card,
            text="",
            bg=self.panel
        ).pack(pady=5)

    # ================================================================
    # MESSAGE
    # ================================================================
    def create_message_panel(self):
        card = tk.Frame(
            self.left_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        tk.Label(
            card,
            text="AVNI RESPONSE",
            font=("Segoe UI", 9, "bold"),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 8)
        )

        self.message_label = tk.Label(
            card,
            text="Hello Roushan.\n\nI am ready for your command.",
            font=("Segoe UI", 12),
            fg=self.text,
            bg=self.panel,
            justify="left",
            wraplength=290
        )

        self.message_label.pack(
            anchor="nw",
            padx=20,
            pady=10
        )

    # ================================================================
    # WAVEFORM
    # ================================================================
    def create_waveform(self):
        card = tk.Frame(
            self.right_panel,
            bg=self.panel,
            highlightbackground="#12306b",
            highlightthickness=1
        )
        card.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        tk.Label(
            card,
            text="NEURAL ACTIVITY",
            font=("Segoe UI", 9, "bold"),
            fg=self.subtext,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 2)
        )

        tk.Label(
            card,
            text="Always here for you  ♡",
            font=("Monotype Corsiva", 20, "italic"),
            fg=self.purple,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        self.wave_canvas = tk.Canvas(
            card,
            bg=self.panel,
            highlightthickness=0
        )

        self.wave_canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

    # ================================================================
    # PARTICLES
    # ================================================================
    def create_background_particles(self):
        self.particles = []

        for _ in range(55):
            self.particles.append({
                "x": random.random(),
                "y": random.random(),
                "speed": random.uniform(0.0005, 0.002),
                "size": random.randint(1, 3),
                "phase": random.uniform(0, math.pi * 2)
            })

    # ================================================================
    # MAIN CENTER SCENE
    # ================================================================
    def draw_scene(self):
        if not hasattr(self, "center_canvas"):
            return

        canvas = self.center_canvas

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 10 or height <= 10:
            return

        canvas.delete("all")

        # ------------------------------------------------------------
        # Background
        # ------------------------------------------------------------
        canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=self.bg,
            outline=""
        )

        cx = width / 2
        cy = height / 2

        # ------------------------------------------------------------
        # Grid
        # ------------------------------------------------------------
        grid_size = 45

        for x in range(0, width, grid_size):
            canvas.create_line(
                x,
                0,
                x,
                height,
                fill="#06132f"
            )

        for y in range(0, height, grid_size):
            canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#06132f"
            )

        # ------------------------------------------------------------
        # Particles
        # ------------------------------------------------------------
        for p in self.particles:
            px = p["x"] * width
            py = p["y"] * height

            glow = 0.5 + 0.5 * math.sin(
                self.anim_tick * 0.05 + p["phase"]
            )

            size = max(
                1,
                int(p["size"] * glow)
            )

            canvas.create_oval(
                px - size,
                py - size,
                px + size,
                py + size,
                fill=self.cyan,
                outline=""
            )

        # ------------------------------------------------------------
        # Outer glow rings
        # ------------------------------------------------------------
        pulse = math.sin(self.anim_tick * 0.06) * 8

        rings = [
            (220 + pulse, "#06235b"),
            (195 + pulse * 0.8, "#07347d"),
            (170 + pulse * 0.6, "#08489c"),
            (145 + pulse * 0.4, "#006ab8")
        ]

        for radius, color in rings:
            canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline=color,
                width=2
            )

        # ------------------------------------------------------------
        # Rotating energy points
        # ------------------------------------------------------------
        for i in range(12):
            angle = (
                self.rotation
                + i * (math.pi * 2 / 12)
            )

            radius = 215 + math.sin(
                self.anim_tick * 0.04 + i
            ) * 8

            px = cx + math.cos(angle) * radius
            py = cy + math.sin(angle) * radius

            canvas.create_oval(
                px - 4,
                py - 4,
                px + 4,
                py + 4,
                fill=self.cyan,
                outline=""
            )

        # ------------------------------------------------------------
        # Platform
        # ------------------------------------------------------------
        self.draw_platform(canvas, cx, cy, width, height)

        # ------------------------------------------------------------
        # Center status
        # ------------------------------------------------------------
        canvas.create_text(
            cx,
            height - 42,
            text=f"AVNI CORE  •  {self.current_state}",
            font=("Segoe UI", 10, "bold"),
            fill=self.cyan
        )

    # ================================================================
    # FALLBACK HOLOGRAM
    # ================================================================
    def draw_fallback_hologram(self, canvas, cx, cy):
        radius = 105

        # Core glow
        for r in range(radius, 10, -12):
            intensity = (radius - r) / radius

            if intensity > 0.75:
                outline = "#0066aa"
            elif intensity > 0.45:
                outline = "#007fcc"
            else:
                outline = "#00aadd"

            canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline=outline,
                width=2
            )

        # Head
        canvas.create_oval(
            cx - 55,
            cy - 78,
            cx + 55,
            cy + 32,
            outline=self.cyan,
            width=3
        )

        # Body
        canvas.create_arc(
            cx - 95,
            cy - 15,
            cx + 95,
            cy + 180,
            start=180,
            extent=180,
            outline=self.cyan,
            width=3
        )

        # Eyes
        eye_y = cy - 28

        canvas.create_oval(
            cx - 35,
            eye_y - 7,
            cx - 17,
            eye_y + 7,
            fill=self.cyan,
            outline=""
        )

        canvas.create_oval(
            cx + 17,
            eye_y - 7,
            cx + 35,
            eye_y + 7,
            fill=self.cyan,
            outline=""
        )

        # Core
        canvas.create_oval(
            cx - 16,
            cy + 55,
            cx + 16,
            cy + 87,
            outline=self.purple,
            width=3
        )

        canvas.create_text(
            cx,
            cy + 135,
            text="AVNI CORE",
            font=("Segoe UI", 17, "bold"),
            fill=self.cyan
        )

        canvas.create_text(
            cx,
            cy + 160,
            text="NEURAL INTERFACE",
            font=("Segoe UI", 8, "bold"),
            fill=self.subtext
        )

    # ================================================================
    # PLATFORM
    # ================================================================
    def draw_platform(
        self,
        canvas,
        cx,
        cy,
        width,
        height
    ):
        y = height * 0.82

        canvas.create_oval(
            cx - 150,
            y - 12,
            cx + 150,
            y + 12,
            outline="#006aa8",
            width=2
        )

        canvas.create_oval(
            cx - 110,
            y - 7,
            cx + 110,
            y + 7,
            outline=self.cyan,
            width=1
        )

        for i in range(8):
            x = cx - 140 + i * 40

            canvas.create_line(
                x,
                y,
                x + 18,
                y + 12,
                fill="#07578c"
            )

    # ================================================================
    # CANVAS RESIZE
    # ================================================================
    def on_canvas_resize(self, event=None):
        self.draw_scene()

    # ================================================================
    # ANIMATION
    # ================================================================
    def animate(self):
        if not self.running:
            return

        self.anim_tick += 1
        self.rotation += 0.025
        self.wave_phase += 0.25
        self.pulse += 0.05

        # Move particles
        for p in self.particles:
            p["y"] -= p["speed"]

            if p["y"] < 0:
                p["y"] = 1
                p["x"] = random.random()

        self.draw_scene()
        self.draw_waveform()

        self.root.after(
            40,
            self.animate
        )

    # ================================================================
    # WAVEFORM
    # ================================================================
    def draw_waveform(self):
        if not hasattr(self, "wave_canvas"):
            return

        canvas = self.wave_canvas

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 20 or height <= 20:
            return

        canvas.delete("all")

        center_y = height / 2

        points = []

        for x in range(0, width, 5):
            normalized = x / max(width, 1)

            amplitude = 8

            if self.current_state == "LISTENING":
                amplitude = 18
            elif self.current_state == "THINKING":
                amplitude = 25
            elif self.current_state == "SPEAKING":
                amplitude = 30

            y = (
                center_y
                + math.sin(
                    normalized * 18
                    + self.wave_phase
                ) * amplitude
                + math.sin(
                    normalized * 42
                    - self.wave_phase * 1.5
                ) * amplitude * 0.35
            )

            points.extend([x, y])

        if len(points) >= 4:
            canvas.create_line(
                *points,
                fill=self.cyan,
                width=2,
                smooth=True
            )

        # Center line
        canvas.create_line(
            0,
            center_y,
            width,
            center_y,
            fill="#092554"
        )

    # ================================================================
    # STATE
    # ================================================================
    def set_state(self, state):
        colors = {
            "IDLE": self.green,
            "LISTENING": self.cyan,
            "THINKING": self.purple,
            "SPEAKING": self.pink
        }

        descriptions = {
            "IDLE": "Waiting for your command...",
            "LISTENING": "Listening to your voice...",
            "THINKING": "Processing your request...",
            "SPEAKING": "Preparing response..."
        }

        self.current_state = state

        self.status_label.config(
            text=f"●  {state}",
            fg=colors.get(state, self.green)
        )

        self.status_description.config(
            text=descriptions.get(
                state,
                "System ready..."
            )
        )

        messages = {
            "IDLE": "Hello Roushan.\n\nI am ready for your command.",
            "LISTENING": "I'm listening...\n\nSpeak your command.",
            "THINKING": "Processing...\n\nPlease wait.",
            "SPEAKING": "Response generated.\n\nI'm ready to speak."
        }

        self.message_label.config(
            text=messages.get(
                state,
                "AVNI is ready."
            )
        )

    # ================================================================
    # QUICK ACTIONS
    # ================================================================
    def open_browser(self):
        webbrowser.open("https://www.google.com")
        self.set_state("SPEAKING")

    def play_music(self):
        webbrowser.open("https://music.youtube.com")
        self.set_state("SPEAKING")

    def check_weather(self):
        webbrowser.open(
            "https://www.google.com/search?q=weather"
        )
        self.set_state("SPEAKING")

    def open_notepad(self):
        try:
            system = platform.system()

            if system == "Windows":
                subprocess.Popen(["notepad.exe"])

            elif system == "Darwin":
                subprocess.Popen(
                    ["open", "-a", "TextEdit"]
                )

            else:
                subprocess.Popen(["gedit"])

            self.set_state("SPEAKING")

        except Exception as e:
            print("Could not open text editor:", e)

    def system_info(self):
        info = tk.Toplevel(self.root)

        info.title("AVNI System Information")
        info.geometry("500x400")
        info.configure(bg=self.bg)

        tk.Label(
            info,
            text="AVNI SYSTEM INFORMATION",
            font=("Segoe UI", 16, "bold"),
            fg=self.cyan,
            bg=self.bg
        ).pack(
            pady=25
        )

        details = [
            f"Operating System: {platform.system()}",
            f"OS Version: {platform.version()}",
            f"Machine: {platform.machine()}",
            f"Processor: {platform.processor()}",
            f"Python: {platform.python_version()}",
            f"AVNI State: {self.current_state}"
        ]

        for item in details:
            tk.Label(
                info,
                text=item,
                font=("Segoe UI", 10),
                fg=self.text,
                bg=self.bg,
                anchor="w"
            ).pack(
                fill="x",
                padx=40,
                pady=6
            )

        tk.Button(
            info,
            text="CLOSE",
            command=info.destroy,
            font=("Segoe UI", 9, "bold"),
            fg=self.cyan,
            bg=self.panel2,
            activebackground="#10265b",
            activeforeground=self.text,
            relief="flat",
            padx=30,
            pady=8
        ).pack(
            pady=25
        )

    # ================================================================
    # FULLSCREEN
    # ================================================================
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        self.root.attributes(
            "-fullscreen",
            self.fullscreen
        )

    # ================================================================
    # CLOSE
    # ================================================================
    def close(self):
        self.running = False

        try:
            self.root.destroy()
        except Exception:
            pass

    # ================================================================
    # RUN
    # ================================================================
    def run(self):
        self.root.mainloop()


# ====================================================================
# STANDALONE TEST
# ====================================================================
if __name__ == "__main__":
    app = Dashboard()
    app.run()