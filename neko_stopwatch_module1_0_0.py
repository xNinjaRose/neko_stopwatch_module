import tkinter as tk
from tkinter import ttk, font, colorchooser
import time
import configparser
import os

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neko Stopwatch Module")
        self.root.geometry("400x320")  # Slightly increased height for status label

        # Timer variables
        self.running = False
        self.paused = False
        self.start_time = 0
        self.elapsed_time = 0
        self.initial_time = 0
        self.current_font = "Arial"
        self.current_font_size = 40
        self.text_color = "black"
        self.bg_color = "#00FF00"

        # Load settings from INI file
        self.config_file = "neko_stopwatch.ini"
        self.load_settings()

        # Top frame for timer
        self.top_frame = tk.Frame(root, bg=self.bg_color)
        self.top_frame.pack(fill="both", expand=True)

        # Bottom frame for buttons
        self.bottom_frame = tk.Frame(root, bg="#1C2526")
        self.bottom_frame.pack(fill="both", expand=True)

        # Timer display
        self.time_var = tk.StringVar(value="00:00:00")
        self.time_label = tk.Label(
            self.top_frame,
            textvariable=self.time_var,
            font=(self.current_font, self.current_font_size),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.time_label.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.bottom_frame, bg="#1C2526")
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

        # Manual time input frame
        time_input_frame = tk.Frame(self.bottom_frame, bg="#1C2526")
        time_input_frame.pack(pady=5)

        # Validation setup
        vcmd = (root.register(self.validate_time_input), '%P', '%W')
        invalidcmd = (root.register(self.on_invalid_input), '%W')

        # Hours, Minutes, Seconds entry fields
        tk.Label(time_input_frame, text="Set Time:", bg="#1C2526", fg="white").pack(side=tk.LEFT, padx=5)
        self.hours_entry = tk.Entry(time_input_frame, width=3, bg="#3C4C4D", fg="white", validate="key", validatecommand=vcmd, invalidcommand=invalidcmd)
        self.hours_entry.insert(0, "00")
        self.hours_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(time_input_frame, text=":", bg="#1C2526", fg="white").pack(side=tk.LEFT)
        self.minutes_entry = tk.Entry(time_input_frame, width=3, bg="#3C4C4D", fg="white", validate="key", validatecommand=vcmd, invalidcommand=invalidcmd)
        self.minutes_entry.insert(0, "00")
        self.minutes_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(time_input_frame, text=":", bg="#1C2526", fg="white").pack(side=tk.LEFT)
        self.seconds_entry = tk.Entry(time_input_frame, width=3, bg="#3C4C4D", fg="white", validate="key", validatecommand=vcmd, invalidcommand=invalidcmd)
        self.seconds_entry.insert(0, "00")
        self.seconds_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(
            time_input_frame, text="Set Time", command=self.set_manual_time
        ).pack(side=tk.LEFT, padx=5)

        # Status label for validation feedback
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            self.bottom_frame, textvariable=self.status_var, bg="#1C2526", fg="white"
        )
        self.status_label.pack(pady=2)

        # Color, font, and font-size controls
        control_frame = tk.Frame(self.bottom_frame, bg="#1C2526")
        control_frame.pack(pady=5)

        tk.Button(
            control_frame, text="Text Color", command=self.change_text_color
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame, text="BG Color", command=self.change_bg_color
        ).pack(side=tk.LEFT, padx=5)

        self.fonts = list(font.families())
        self.font_var = tk.StringVar(value=self.current_font)
        font_menu = ttk.Combobox(
            control_frame, textvariable=self.font_var, values=self.fonts, width=15
        )
        font_menu.pack(side=tk.LEFT, padx=5)
        font_menu.bind("<<ComboboxSelected>>", self.change_font)

        self.font_size_var = tk.StringVar(value=str(self.current_font_size))
        font_size_menu = ttk.Combobox(
            control_frame, textvariable=self.font_size_var, values=[10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80], width=5
        )
        font_size_menu.pack(side=tk.LEFT, padx=5)
        font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)

    def validate_time_input(self, value, widget_name):
        if not value:
            self.status_var.set("")
            self.reset_entry_color(self.root.nametowidget(widget_name))
            return True
        try:
            num = int(value)
            if "hours" in widget_name:
                self.reset_entry_color(self.root.nametowidget(widget_name))
                self.status_var.set("")
                return True
            elif "minutes" in widget_name or "seconds" in widget_name:
                if 0 <= num < 60:
                    self.reset_entry_color(self.root.nametowidget(widget_name))
                    self.status_var.set("")
                    return True
                else:
                    self.status_var.set("Minutes/Seconds must be 0-59")
                    return False
        except ValueError:
            self.status_var.set("Enter numbers only")
            return False

    def on_invalid_input(self, widget_name):
        entry = self.root.nametowidget(widget_name)
        entry.configure(bg="#FF4D4D")  # Red for invalid input

    def reset_entry_color(self, entry):
        entry.configure(bg="#3C4C4D")  # Default dark gray

    def load_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            if "Settings" in config:
                self.current_font = config["Settings"].get("font", "Arial")
                self.current_font_size = config["Settings"].getint("font_size", 40)
                self.text_color = config["Settings"].get("text_color", "black")
                self.bg_color = config["Settings"].get("bg_color", "#00FF00")
        else:
            # Create INI file with defaults
            config["Settings"] = {
                "font": self.current_font,
                "font_size": self.current_font_size,
                "text_color": self.text_color,
                "bg_color": self.bg_color
            }
            with open(self.config_file, "w") as f:
                config.write(f)

    def save_settings(self):
        config = configparser.ConfigParser()
        config["Settings"] = {
            "font": self.current_font,
            "font_size": self.current_font_size,
            "text_color": self.text_color,
            "bg_color": self.bg_color
        }
        with open(self.config_file, "w") as f:
            config.write(f)

    def update_timer(self):
        if self.running and not self.paused:
            current_time = time.time()
            elapsed = current_time - self.start_time + self.elapsed_time + self.initial_time
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
        self.initial_time = 0
        self.time_var.set("00:00:00")
        self.hours_entry.delete(0, tk.END)
        self.hours_entry.insert(0, "00")
        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "00")
        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, "00")
        self.status_var.set("")
        self.reset_entry_color(self.hours_entry)
        self.reset_entry_color(self.minutes_entry)
        self.reset_entry_color(self.seconds_entry)

    def set_manual_time(self):
        try:
            hours = int(self.hours_entry.get()) if self.hours_entry.get() else 0
            minutes = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
            seconds = int(self.seconds_entry.get()) if self.seconds_entry.get() else 0
            if minutes >= 60 or seconds >= 60:
                raise ValueError("Minutes and seconds must be less than 60")
            self.initial_time = hours * 3600 + minutes * 60 + seconds
            self.elapsed_time = 0
            self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.status_var.set("Time set successfully")
            self.root.after(2000, lambda: self.status_var.set(""))
        except ValueError:
            self.status_var.set("Invalid input")
            self.root.after(2000, lambda: self.status_var.set(""))

    def change_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_color = color
            self.time_label.configure(fg=color)
            self.save_settings()

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color = color
            self.top_frame.configure(bg=color)
            self.time_label.configure(bg=color)
            self.save_settings()

    def change_font(self, event=None):
        self.current_font = self.font_var.get()
        self.time_label.configure(font=(self.current_font, self.current_font_size))
        self.save_settings()

    def change_font_size(self, event=None):
        self.current_font_size = int(self.font_size_var.get())
        self.time_label.configure(font=(self.current_font, self.current_font_size))
        self.save_settings()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
