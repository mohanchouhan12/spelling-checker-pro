import tkinter as tk
from textblob import TextBlob
from textblob import Word


# ---------- Theme Colors ----------
light_theme = {
    "bg": "#f0f4f8",
    "fg": "#2c3e50",
    "frame": "#ffffff",
    "border": "#3498db",
    "entry_bg": "#ffffff",
    "entry_fg": "black",
    "button_bg": "#3498db",
    "button_fg": "white",
    "result_fg": "#2c3e50",
    "shadow": "#e0e0e0"
}


dark_theme = {
    "bg": "#1a1a2e",
    "fg": "#00d4ff",
    "frame": "#16213e",
    "border": "#00d4ff",
    "entry_bg": "#0f3460",
    "entry_fg": "#eaf0f7",
    "button_bg": "linear",  # Will use gradient
    "button_fg": "white",
    "result_fg": "#eaf0f7",
    "shadow": "#0a0a15",
    "accent": "#e94560"
}


current_theme = dark_theme  # start with dark mode



# ---------- Gradient Button Class ----------
class GradientButton(tk.Canvas):
    def __init__(self, parent, text, command=None, colors=("#667eea", "#764ba2"), **kwargs):
        tk.Canvas.__init__(self, parent, highlightthickness=0, **kwargs)
        self.command = command
        self.colors = colors
        self.text = text
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._draw)
        
    def _draw(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Create gradient
        r1, g1, b1 = self.winfo_rgb(self.colors[0])
        r2, g2, b2 = self.winfo_rgb(self.colors[1])
        r1, g1, b1 = r1/256, g1/256, b1/256
        r2, g2, b2 = r2/256, g2/256, b2/256
        
        for i in range(width):
            r = r1 + (r2 - r1) * i / width
            g = g1 + (g2 - g1) * i / width
            b = b1 + (b2 - b1) * i / width
            color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
            self.create_line(i, 0, i, height, fill=color, tags="gradient")
        
        # Rounded corners effect
        self.create_rectangle(0, 0, width, height, outline=self.colors[0], width=2, tags="border")
        
        # Text
        self.create_text(width/2, height/2, text=self.text, 
                        fill="white", font=("Arial", 16, "bold"), tags="text")
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.config(cursor="hand2")
        self.itemconfig("text", font=("Arial", 17, "bold"))
        
    def _on_leave(self, event):
        self.itemconfig("text", font=("Arial", 16, "bold"))



# ---------- Apply Theme ----------
def apply_theme():
    root.config(bg=current_theme["bg"])
    heading.config(bg=current_theme["bg"], fg=current_theme["fg"])
    
    # Update main frame with shadow effect
    frame.config(bg=current_theme["frame"])
    border.config(bg=current_theme["border"])
    
    enter_text.config(
        bg=current_theme["entry_bg"], 
        fg=current_theme["entry_fg"],
        insertbackground=current_theme["fg"],
        highlightbackground=current_theme["border"], 
        highlightcolor=current_theme["border"]
    )
    
    result_label.config(bg=current_theme["frame"], fg=current_theme["result_fg"])
    suggestion_label.config(bg=current_theme["frame"], fg=current_theme["result_fg"])
    
    # Update toggle button
    if current_theme == dark_theme:
        toggle_btn.config(text="☀️ Light Mode", bg="#e94560", fg="white")
    else:
        toggle_btn.config(text="🌙 Dark Mode", bg="#3498db", fg="white")



# ---------- Spelling Check Function ----------
def check_spelling(event=None):
    word = enter_text.get().strip()
    if word == "":
        result_label.config(text="⚠️ Please enter a word!", fg="#e74c3c")
        suggestion_label.config(text="")
        return


    a = TextBlob(word)
    corrected_word = str(a.correct())


    if corrected_word.lower() == word.lower():
        result_label.config(text=f"✅ Correct spelling: {corrected_word}", fg="#27ae60")
        suggestion_label.config(text="🎉 Perfect! No corrections needed.")
    else:
        result_label.config(text=f"❌ Did you mean: {corrected_word}?", fg="#f39c12")


        # Suggestions from Word.spellcheck()
        w = Word(word)
        suggestions = [sug[0] for sug in w.spellcheck()[:5]]
        if suggestions:
            suggestion_label.config(
                text="💡 Suggestions: " + ", ".join(suggestions),
                fg=current_theme["result_fg"]
            )



# ---------- Toggle Theme ----------
def toggle_theme():
    global current_theme
    current_theme = light_theme if current_theme == dark_theme else dark_theme
    apply_theme()
    
    # Recreate gradient button with new theme colors
    check_button.destroy()
    create_check_button()



# ---------- Create Gradient Check Button ----------
def create_check_button():
    global check_button
    if current_theme == dark_theme:
        colors = ("#00d4ff", "#e94560")
    else:
        colors = ("#3498db", "#2980b9")
    
    check_button = GradientButton(
        frame, 
        text="🔍 Check Spelling",
        command=check_spelling,
        colors=colors,
        width=250,
        height=50,
        bg=current_theme["frame"]
    )
    check_button.pack(pady=20)



# ---------- Root Window ----------
root = tk.Tk()
root.title("✨ Enhanced Spelling Checker")
root.geometry("850x650")
root.resizable(True, True)


# Add a subtle shadow effect by layering frames
shadow_frame = tk.Frame(root, bg=current_theme.get("shadow", "#e0e0e0"))
shadow_frame.place(relx=0.5, rely=0.55, anchor="center", width=665, height=385)


# ---------- Heading ----------
heading = tk.Label(
    root, 
    text="✨ Spelling Checker Pro ✨",
    font=("Trebuchet MS", 38, "bold")
)
heading.pack(pady=(50, 25))


# Subtitle
subtitle = tk.Label(
    root,
    text="Check your spelling instantly with AI-powered suggestions",
    font=("Segoe UI", 12, "italic"),
    bg=current_theme["bg"],
    fg=current_theme["fg"]
)
subtitle.pack(pady=(0, 15))


# ---------- Container Frame (Card Style with 3D effect) ----------
frame = tk.Frame(root, bd=0, relief="flat")
frame.place(relx=0.5, rely=0.55, anchor="center", width=660, height=380)


border = tk.Frame(frame, bd=3, relief="solid")
border.place(x=-3, y=-3, relwidth=1.015, relheight=1.02)


# ---------- Entry with placeholder effect ----------
enter_text = tk.Entry(
    frame, 
    justify="center",
    width=18, 
    font=("Poppins", 26, "bold"),
    relief="flat", 
    highlightthickness=3,
    bd=10
)
enter_text.pack(pady=35)
enter_text.focus()
enter_text.bind("<Return>", check_spelling)


# Placeholder text
placeholder = "Type a word..."
def on_entry_click(event):
    if enter_text.get() == placeholder:
        enter_text.delete(0, "end")
        enter_text.config(fg=current_theme["entry_fg"])

def on_focus_out(event):
    if enter_text.get() == "":
        enter_text.insert(0, placeholder)
        enter_text.config(fg="gray")

enter_text.insert(0, placeholder)
enter_text.config(fg="gray")
enter_text.bind('<FocusIn>', on_entry_click)
enter_text.bind('<FocusOut>', on_focus_out)


# ---------- Gradient Button ----------
check_button = None
create_check_button()


# ---------- Result ----------
result_label = tk.Label(
    frame, 
    text="",
    font=("Poppins", 18, "bold"),
    wraplength=600
)
result_label.pack(pady=15)


# ---------- Suggestions ----------
suggestion_label = tk.Label(
    frame, 
    text="",
    font=("Segoe UI", 14, "italic"),
    wraplength=600
)
suggestion_label.pack(pady=10)


# ---------- Toggle Button with better styling ----------
toggle_btn = tk.Button(
    root, 
    text="☀️ Light Mode",
    font=("Arial", 13, "bold"),
    cursor="hand2", 
    relief="flat",
    padx=20, 
    pady=10,
    command=toggle_theme,
    bd=0,
    activebackground="#c0392b",
    activeforeground="white"
)
toggle_btn.pack(side="bottom", pady=20)


# Add hover effect to toggle button
def on_toggle_enter(e):
    toggle_btn.config(relief="raised")

def on_toggle_leave(e):
    toggle_btn.config(relief="flat")

toggle_btn.bind("<Enter>", on_toggle_enter)
toggle_btn.bind("<Leave>", on_toggle_leave)


# ---------- Apply Initial Theme ----------
apply_theme()


# ---------- Run ----------
root.mainloop()