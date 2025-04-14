import tkinter as tk
from tkinter import ttk, font, colorchooser
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neko Stopwatch Module")
        self.root.geometry("400x250")

        # Top frame for timer (green for chroma key)
        self.top_frame = tk.Frame(root, bg="#00FF00")  # Green background
        self.top_frame.pack(fill="both", expand=True)

        # Bottom frame for buttons (dark mode)
        self.bottom_frame = tk.Frame(root, bg="#1C2526")  # Dark gray background
        self.bottom_frame.pack(fill="both", expand=True)

        # Timer variables
        self.running = False
        self.paused = False
        self.start_time = 0
        self.elapsed_time = 0

        # Timer display in the top frame
        self.time_var = tk.StringVar(value="00:00:00")
        self.current_font = "Arial"
        self.current_font_size = 40
        self.time_label = tk.Label(
            self.top_frame,
            textvariable=self.time_var,
            font=(self.current_font, self.current_font_size),
            fg="black",
            bg="#00FF00"
        )
        self.time_label.pack(pady=10)

        # Button frame in the bottom frame
        button_frame = tk.Frame(self.bottom_frame, bg="#1C2526")  # Match dark gray
        button_frame.pack(pady=5)

        # Control buttons
        self.start_button = tk.Button(
            button_frame, text="Start", command=self.start_timer
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            button_frame, text="Pause", command=self.pause_timer
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(
            button_frame, text="Stop/Reset", command=self.reset_timer
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        # Color, font, and font-size controls in the bottom frame
        control_frame = tk.Frame(self.bottom_frame, bg="#1C2526")  # Match dark gray
        control_frame.pack(pady=5)

        # Color buttons
        tk.Button(
            control_frame, text="Text Color", command=self.change_text_color
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame, text="BG Color", command=self.change_bg_color
        ).pack(side=tk.LEFT, padx=5)

        # Font selection
        self.fonts = list(font.families())
        self.font_var = tk.StringVar(value="Arial")
        font_menu = ttk.Combobox(
            control_frame, textvariable=self.font_var, values=self.fonts, width=15
        )
        font_menu.pack(side=tk.LEFT, padx=5)
        font_menu.bind("<<ComboboxSelected>>", self.change_font)

        # Font size selection
        self.font_size_var = tk.StringVar(value="40")
        font_size_menu = ttk.Combobox(
            control_frame, textvariable=self.font_size_var, values=[10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80], width=5
        )
        font_size_menu.pack(side=tk.LEFT, padx=5)
        font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)

    def update_timer(self):
        if self.running and not self.paused:
            current_time = time.time()
            elapsed = current_time - self.start_time + self.elapsed_time
            hours, rem = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(rem, 60)
            self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        if self.running:
            self.root.after(100, self.update_timer)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()
        elif self.paused:
            self.paused = False
            self.start_time = time.time()
            self.update_timer()

    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            self.elapsed_time += time.time() - self.start_time

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.elapsed_time = 0
        self.time_var.set("00:00:00")

    def change_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.time_label.configure(fg=color)

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.top_frame.configure(bg=color)  # Only change the top frame
            self.time_label.configure(bg=color)

    def change_font(self, event=None):
        self.current_font = self.font_var.get()
        self.time_label.configure(font=(self.current_font, self.current_font_size))

    def change_font_size(self, event=None):
        self.current_font_size = int(self.font_size_var.get())
        self.time_label.configure(font=(self.current_font, self.current_font_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
