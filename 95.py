import tkinter as tk
from tkinter import font as tkfont
import time
import random

class Win95Desktop:
    """Main desktop window (overrideredirect, no title bar)."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")  # No title
        self.root.geometry("600x400")
        self.root.configure(bg='#008080')  # Teal background (classic Win95)
        self.root.overrideredirect(True)    # Remove window decorations

        # Allow moving the main window via Alt+drag (optional)
        self.root.bind('<Alt-Button-1>', self.start_move)
        self.root.bind('<Alt-B1-Motion>', self.do_move)

        # Desktop frame for icons
        self.desktop_frame = tk.Frame(self.root, bg='#008080')
        self.desktop_frame.pack(fill=tk.BOTH, expand=True)

        # Icons
        self.create_desktop_icon("My Computer", 20, 20, self.open_mycomputer)
        self.create_desktop_icon("Recycle Bin", 20, 100, self.open_recyclebin)
        self.create_desktop_icon("Network Neighborhood", 20, 180, self.open_network)

        # Taskbar
        self.taskbar = tk.Frame(self.root, bg='#c0c0c0', height=30, relief=tk.RAISED, bd=2)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Start button — black with blue text
        self.start_btn = tk.Button(self.taskbar, text=" Start ", bg='black', fg='blue',
                                    relief=tk.RAISED, font=('MS Sans Serif', 9, 'bold'),
                                    command=self.toggle_start_menu)
        self.start_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Quick launch (dummy)
        self.quick_launch = tk.Frame(self.taskbar, bg='#c0c0c0')
        self.quick_launch.pack(side=tk.LEFT, padx=5)
        tk.Label(self.quick_launch, text="  ", bg='#c0c0c0').pack(side=tk.LEFT)

        # System tray
        self.tray = tk.Frame(self.taskbar, bg='#c0c0c0')
        self.tray.pack(side=tk.RIGHT, padx=5)
        self.clock_label = tk.Label(self.tray, bg='#c0c0c0', font=('MS Sans Serif', 8))
        self.clock_label.pack()
        self.update_clock()

        # Start menu (initially hidden)
        self.start_menu = None

        # Keep track of open windows
        self.open_windows = []

        self.root.mainloop()

    def create_desktop_icon(self, name, x, y, command):
        """Place an icon label on the desktop."""
        icon_frame = tk.Frame(self.desktop_frame, bg='#008080')
        icon_frame.place(x=x, y=y)
        # Icon (simulated with a colored square)
        icon_canvas = tk.Canvas(icon_frame, width=32, height=32, bg='#008080', highlightthickness=0)
        icon_canvas.create_rectangle(2,2,30,30, fill='#ffffff', outline='black')
        icon_canvas.create_text(16,16, text=name[0], font=('MS Sans Serif', 14))
        icon_canvas.pack()
        # Label
        lbl = tk.Label(icon_frame, text=name, bg='#008080', fg='white',
                       font=('MS Sans Serif', 8))
        lbl.pack()
        # Bind double-click
        icon_canvas.bind('<Double-Button-1>', lambda e: command())
        lbl.bind('<Double-Button-1>', lambda e: command())

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_clock(self):
        """Update the taskbar clock every second."""
        current = time.strftime('%I:%M %p').lstrip('0')
        self.clock_label.config(text=current)
        self.root.after(1000, self.update_clock)

    def toggle_start_menu(self):
        """Show or hide the classic start menu."""
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
        else:
            self.show_start_menu()

    def show_start_menu(self):
        """Create a popup start menu above the Start button."""
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.overrideredirect(True)
        self.start_menu.configure(bg='#c0c0c0')
        # Position above start button
        x = self.root.winfo_rootx() + self.start_btn.winfo_x()
        y = self.root.winfo_rooty() - 200
        self.start_menu.geometry(f"180x200+{x}+{y}")

        # Menu items — black with blue text
        items = [
            ("Programs", None),
            ("Documents", None),
            ("Settings", None),
            ("Find", None),
            ("Help", None),
            ("Run...", None),
            ("Shut Down...", self.shut_down)
        ]
        for text, cmd in items:
            btn = tk.Button(self.start_menu, text=text, bg='black', fg='blue',
                            relief=tk.FLAT, anchor='w', padx=10,
                            font=('MS Sans Serif', 9), command=cmd if cmd else lambda t=text: None)
            btn.pack(fill=tk.X)

    def shut_down(self):
        """Close the entire simulation."""
        self.root.quit()

    # ----- Window opening methods -----
    def open_mycomputer(self):
        win = Win95Window(self.root, "My Computer", self.close_callback)
        # Add some dummy content
        tk.Label(win.content, text="Hard drives:", bg='white', anchor='w').pack(fill=tk.X, padx=5, pady=5)
        tk.Label(win.content, text="Local Disk (C:)", bg='white').pack(anchor='w', padx=20)
        self.open_windows.append(win)

    def open_recyclebin(self):
        win = Win95Window(self.root, "Recycle Bin", self.close_callback)
        tk.Label(win.content, text="Empty", bg='white', font=('MS Sans Serif', 10)).pack(padx=10, pady=10)
        self.open_windows.append(win)

    def open_network(self):
        win = Win95Window(self.root, "Network Neighborhood", self.close_callback)
        tk.Label(win.content, text="Entire Network", bg='white').pack(padx=10, pady=10)
        self.open_windows.append(win)

    def close_callback(self, win):
        if win in self.open_windows:
            self.open_windows.remove(win)


class Win95Window:
    """A custom window with classic Win95 title bar and close button."""
    def __init__(self, parent, title, close_callback):
        self.parent = parent
        self.title = title
        self.close_callback = close_callback

        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.configure(bg='#c0c0c0')
        self.window.geometry("300x200+{}+{}".format(
            parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Title bar
        self.title_bar = tk.Frame(self.window, bg='#000080', height=22, relief=tk.RAISED, bd=2)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)

        # Title text
        lbl_title = tk.Label(self.title_bar, text=title, bg='#000080', fg='white',
                              font=('MS Sans Serif', 9, 'bold'))
        lbl_title.pack(side=tk.LEFT, padx=5)
        lbl_title.bind('<Button-1>', self.start_move)
        lbl_title.bind('<B1-Motion>', self.do_move)

        # Close button — black with blue text
        close_btn = tk.Button(self.title_bar, text='X', bg='black', fg='blue', width=2,
                               command=self.close, font=('MS Sans Serif', 8, 'bold'))
        close_btn.pack(side=tk.RIGHT, padx=2, pady=1)

        # Content area
        self.content = tk.Frame(self.window, bg='white', relief=tk.SUNKEN, bd=2)
        self.content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Bind focus
        self.window.bind('<Button-1>', self.focus)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")

    def focus(self, event):
        self.window.lift()

    def close(self):
        self.window.destroy()
        self.close_callback(self)


if __name__ == "__main__":
    Win95Desktop()
