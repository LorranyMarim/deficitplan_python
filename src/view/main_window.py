import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tw = None

    def show(self, text):
        if self.tw:
            return
        x, y, cx, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=text, justify='left',
                         background="#ffcccc", foreground="#990000",
                         relief='solid', borderwidth=1,
                         font=("Helvetica", "9", "bold"))
        label.pack(ipadx=4, ipady=2)
        self.widget.after(3000, self.hide) 

    def hide(self):
        if self.tw:
            self.tw.destroy()
            self.tw = None

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='gray', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color

    def foc_in(self, *args):
        if self['foreground'] == self.placeholder_color:
            self.delete('0', 'end')
            self['foreground'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def get_value(self):
        val = self.get()
        return "" if val == self.placeholder else val

    def reset(self):
        self.delete(0, tk.END)
        self.put_placeholder()


class CalorieCalculatorApp(ThemedTk):
    def __init__(self, controller):
        super().__init__(theme="arco")
        self.controller = controller
        
        self.title("DeficitPlan - Calorie Deficit Calculator and Weight Loss Plan")
        self.geometry("1100x720")
        self.resizable(False, False) 
        self.configure(padx=20, pady=20)
        
        try:
            icon_path = os.path.join(ROOT_DIR, "img", "icon-escala.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error loading main icon: {e}")

        self.style = ttk.Style(self)
        self.style.configure("TLabelframe.Label", font=("Helvetica", 14, "bold"), foreground="#333333")
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        
        self.build_interface()
        self.tooltips = {}

    def build_interface(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        self.frame_form = ttk.Frame(self)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.frame_form.columnconfigure(0, weight=1) 
        self.frame_form.rowconfigure(2, weight=1) 

        self.build_form()
        
        self.frame_result = ttk.LabelFrame(self, text="Results & Analysis", padding=20)
        self.frame_result.grid(row=0, column=1, sticky="nsew")
        
        self.build_results()

    def build_form(self):
        # Body Metrics
        frame_metrics = ttk.LabelFrame(self.frame_form, text="Body Metrics", padding=15)
        frame_metrics.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        frame_metrics.columnconfigure(1, weight=1)

        ttk.Label(frame_metrics, text="Weight (kg):").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_weight = PlaceholderEntry(frame_metrics, placeholder="e.g., 70.5")
        self.entry_weight.grid(row=0, column=1, sticky="ew", pady=8, padx=(10, 0))
        
        ttk.Label(frame_metrics, text="Height (cm):").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_height = PlaceholderEntry(frame_metrics, placeholder="e.g., 175")
        self.entry_height.grid(row=1, column=1, sticky="ew", pady=8, padx=(10, 0))
        
        ttk.Label(frame_metrics, text="Age:").grid(row=2, column=0, sticky="w", pady=8)
        self.entry_age = PlaceholderEntry(frame_metrics, placeholder="e.g., 28")
        self.entry_age.grid(row=2, column=1, sticky="ew", pady=8, padx=(10, 0))
        
        ttk.Label(frame_metrics, text="Sex:").grid(row=3, column=0, sticky="w", pady=8)
        self.select_sex = ttk.Combobox(frame_metrics, values=["Female", "Male"], state="readonly")
        self.select_sex.set("Select an option")
        self.select_sex.grid(row=3, column=1, sticky="ew", pady=8, padx=(10, 0))

        ttk.Label(frame_metrics, text="Activity Level:").grid(row=4, column=0, sticky="w", pady=8)
        self.level_activity_list = [
            "Sedentary (Little to no exercise)",
            "Lightly active (Exercise 1–3 days/week)",
            "Moderately active (Exercise 3–5 days/week)",
            "Very active (Exercise 6–7 days/week)",
            "Extremely active (Athlete or heavy physical job)"
        ]
        self.select_level = ttk.Combobox(frame_metrics, values=self.level_activity_list, state="readonly")
        self.select_level.set("Select an option")
        self.select_level.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # Weight Loss Plan
        frame_plan = ttk.LabelFrame(self.frame_form, text="Weight Loss Plan", padding=15)
        frame_plan.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        frame_plan.columnconfigure(1, weight=1)

        ttk.Label(frame_plan, text="Total Weight to Lose (kg):").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_total_loss = PlaceholderEntry(frame_plan, placeholder="e.g., 10")
        self.entry_total_loss.grid(row=0, column=1, sticky="ew", pady=8, padx=(10, 0))

        ttk.Label(frame_plan, text="Goal Weight Loss (kg):").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_goal = PlaceholderEntry(frame_plan, placeholder="e.g., 0.5 - 1.5")
        self.entry_goal.grid(row=1, column=1, sticky="ew", pady=8, padx=(10, 0))

        ttk.Label(frame_plan, text="Plan Activity Level:").grid(row=2, column=0, sticky="w", pady=8)
        self.plan_activity_list = [
            "light-level activity – 2 days per week",
            "basic-level activity – 3 days per week",
            "moderate-level activity – 4 days per week",
            "advanced-level activity – 5 days per week",
            "high-level activity – 6 days per week",
            "extreme-level activity – 7 days per week"
        ]
        self.select_plan_activity = ttk.Combobox(frame_plan, values=self.plan_activity_list, state="readonly")
        self.select_plan_activity.set("Select an option")
        self.select_plan_activity.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # Buttons
        frame_buttons = ttk.Frame(self.frame_form)
        frame_buttons.grid(row=2, column=0, sticky="s", pady=10)

        try:
            path_clear = os.path.join(ROOT_DIR, "img", "icon-clear.ico")
            path_ok = os.path.join(ROOT_DIR, "img", "icon-ok.ico")
            self.icon_clear = ImageTk.PhotoImage(Image.open(path_clear).resize((18, 18), Image.Resampling.LANCZOS))
            self.icon_ok = ImageTk.PhotoImage(Image.open(path_ok).resize((18, 18), Image.Resampling.LANCZOS))
        except Exception:
            self.icon_clear, self.icon_ok = None, None

        self.btn_clear = ttk.Button(frame_buttons, text="Clear Fields", image=self.icon_clear, compound=tk.LEFT, command=self.controller.clear_fields)
        self.btn_clear.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=2)

        self.btn_execute = ttk.Button(frame_buttons, text="Calculate Plan", image=self.icon_ok, compound=tk.LEFT, command=self.controller.calculate_plan)
        self.btn_execute.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=2)

    def build_results(self):
        self.frame_result.columnconfigure(0, weight=1)
        self.frame_result.columnconfigure(1, weight=2)
        self.frame_result.rowconfigure(0, weight=1)

        self.subframe_img = ttk.Frame(self.frame_result)
        self.subframe_img.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        try:
            path_body = os.path.join(ROOT_DIR, "img", "vector_default.png")
            img = Image.open(path_body)
            img.thumbnail((250, 500), Image.Resampling.LANCZOS) 
            self.body_image = ImageTk.PhotoImage(img)
            self.lbl_body_image = ttk.Label(self.subframe_img, image=self.body_image)
            self.lbl_body_image.pack(expand=True)
        except Exception:
            self.lbl_body_image = ttk.Label(self.subframe_img, text="[ Body Image Missing ]", foreground="gray")
            self.lbl_body_image.pack(expand=True)

        self.subframe_data = ttk.Frame(self.frame_result)
        self.subframe_data.grid(row=0, column=1, sticky="nsew")
        self.subframe_data.columnconfigure(1, weight=1)

        results_fields = [
            "Body Mass Index:", "Category:", "Base Metabolic Rate:",
            "Total Daily Energy Expenditure:", "Daily Caloric Deficit:",
            "Daily Caloric Intake:", "Total Weight to Lose:",
            "Weekly Weight Loss Goal:", "Physical Activity Level:",
            "Total Weeks to Complete:"
        ]

        self.result_vars = {}
        self.result_labels = {}

        for idx, field in enumerate(results_fields):
            ttk.Label(self.subframe_data, text=field, font=("Helvetica", 10)).grid(row=idx, column=0, sticky="e", pady=8, padx=(0, 10))
            var = tk.StringVar(value="--")
            self.result_vars[field] = var
            lbl_data = tk.Label(self.subframe_data, textvariable=var, bg="#f9f9f9", fg="black", anchor="center", relief="flat", pady=5)
            lbl_data.grid(row=idx, column=1, sticky="ew", pady=8)
            self.result_labels[field] = lbl_data

        frame_profile_header = ttk.Frame(self.subframe_data)
        frame_profile_header.grid(row=len(results_fields), column=0, columnspan=2, sticky="ew", pady=(20, 5))
        
        ttk.Label(frame_profile_header, text="Exercise Profile:", font=("Helvetica", 11, "bold")).pack(side=tk.LEFT)

        try:
            path_copy = os.path.join(ROOT_DIR, "img", "icon-copy.ico")
            self.icon_copy = ImageTk.PhotoImage(Image.open(path_copy).resize((16, 16), Image.Resampling.LANCZOS))
        except Exception:
            self.icon_copy = None

        self.btn_copy = ttk.Button(frame_profile_header, image=self.icon_copy, command=self.copy_profile)
        self.btn_copy.pack(side=tk.RIGHT)

        self.text_profile = tk.Text(self.subframe_data, height=8, width=40, state=tk.DISABLED, font=("Consolas", 9), bg="#f9f9f9", relief="solid", borderwidth=1)
        self.text_profile.grid(row=len(results_fields)+1, column=0, columnspan=2, sticky="ew")

    def show_tooltip(self, widget, message):
        if widget not in self.tooltips:
            self.tooltips[widget] = ToolTip(widget)
        self.tooltips[widget].show(message)

    def get_form_data(self):
        return {
            "weight": self.entry_weight.get_value(),
            "height": self.entry_height.get_value(),
            "age": self.entry_age.get_value(),
            "sex": self.select_sex.get(),
            "activity_level": self.select_level.get(),
            "total_loss": self.entry_total_loss.get_value(), 
            "weekly_loss": self.entry_goal.get_value(),      
            "plan_activity": self.select_plan_activity.get()
        }

    def reset_ui(self):
        self.entry_weight.reset()
        self.entry_height.reset()
        self.entry_age.reset()
        self.entry_total_loss.reset()
        self.entry_goal.reset()
        
        self.select_sex.set("Select an option")
        self.select_level.set("Select an option")
        self.select_plan_activity.set("Select an option")

        for key in self.result_vars:
            self.set_result(key, "--", "#f9f9f9", "black")
            
        self.update_exercise_profile("")

    def set_result(self, field_name, value, bg_color="#f9f9f9", fg_color="black"):
        if field_name in self.result_vars:
            self.result_vars[field_name].set(value) 
        if field_name in self.result_labels:
            self.result_labels[field_name].configure(bg=bg_color, fg=fg_color) 

    def update_body_image(self, filename):
        try:
            path_body = os.path.join(ROOT_DIR, "img", filename)
            img = Image.open(path_body)
            img.thumbnail((250, 500), Image.Resampling.LANCZOS)
            self.body_image = ImageTk.PhotoImage(img)
            self.lbl_body_image.configure(image=self.body_image)
        except Exception as e:
            print(f"Error loading body image: {e}")

    def update_exercise_profile(self, text):
        self.text_profile.config(state=tk.NORMAL)
        self.text_profile.delete(1.0, tk.END)
        self.text_profile.insert(tk.END, text)
        self.text_profile.config(state=tk.DISABLED)

    def copy_profile(self):
        content = self.text_profile.get(1.0, tk.END).strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("Copied", "Exercise profile copied to clipboard!")