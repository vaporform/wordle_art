import tkinter as tk
from tkinter import messagebox

COLS, ROWS = 5, 6
CELL = 60
COLOR_MAP = {"green": "G", "yellow": "Y", "grey": "B"}
DISPLAY = {"green": "#4caf50", "yellow": "#ffeb3b", "grey": "#9e9e9e"}

grid = [["grey"] * COLS for _ in range(ROWS)]
current_color = ["green"]

root = tk.Tk()
root.title("Grid Painter")
root.resizable(False, False)

# --- Top: color picker ---
top = tk.Frame(root, pady=6)
top.pack()

color_buttons = {}
for color in ["green", "yellow", "grey"]:
    btn = tk.Button(top,text= color, width=8, bg=DISPLAY[color],
                    relief="flat", bd=2,
                    command=lambda c=color: select(c))
    btn.pack(side="left", padx=6)
    color_buttons[color] = btn

def select(c):
    current_color[0] = c
    for name, b in color_buttons.items():
        b.config(relief="sunken" if name == c else "flat")

select("green")

# --- Canvas ---
canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg="#222")
canvas.pack(padx=10, pady=4)

rects = {}
for r in range(ROWS):
    for c in range(COLS):
        x0, y0 = c*CELL, r*CELL
        rid = canvas.create_rectangle(x0, y0, x0+CELL, y0+CELL,
                                      fill=DISPLAY["grey"], outline="#333", width=1)
        rects[(r, c)] = rid

def paint(event):
    c = event.x // CELL
    r = event.y // CELL
    if 0 <= r < ROWS and 0 <= c < COLS:
        grid[r][c] = current_color[0]
        canvas.itemconfig(rects[(r, c)], fill=DISPLAY[current_color[0]])

canvas.bind("<Button-1>", paint)
canvas.bind("<B1-Motion>", paint)

# --- Bottom buttons ---
bot = tk.Frame(root, pady=6)
bot.pack()

def export():
    lines = ['lines = [']
    for row in grid:
        s = "".join(COLOR_MAP[cell] for cell in row)
        lines.append(f'    "{s}",')
    lines.append("]")
    result = "\n".join(lines)
    print("\n" + result + "\n")
    # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(result)
    messagebox.showinfo("Exported", "Output printed to terminal and copied to clipboard!")

def paste_import():
    raw = root.clipboard_get()
    # Parse lines = [...] format
    rows = []
    for line in raw.splitlines():
        line = line.strip().strip('",').strip()
        if len(line) == COLS and all(ch in "GYB" for ch in line):
            rows.append(line)
    if len(rows) != ROWS:
        messagebox.showerror("Paste Error",
            f"Expected {ROWS} valid rows of {COLS} chars (G/Y/B), got {len(rows)}.")
        return
    rev = {"G": "green", "Y": "yellow", "B": "grey"}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            grid[r][c] = rev[ch]
            canvas.itemconfig(rects[(r, c)], fill=DISPLAY[rev[ch]])

def clear_all():
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = "grey"
            canvas.itemconfig(rects[(r, c)], fill=DISPLAY["grey"])

tk.Button(bot, text="Export", width=10, command=export).pack(side="left", padx=6)
tk.Button(bot, text="Paste", width=10, command=paste_import).pack(side="left", padx=6)
tk.Button(bot, text="Clear", width=10, command=clear_all).pack(side="left", padx=6)

root.mainloop()