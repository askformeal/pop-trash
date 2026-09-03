from queue import Queue
from threading import Thread
from pathlib import Path
import time
import tkinter as tk
from importlib.resources import files

from tkinterdnd2 import DND_FILES, TkinterDnD
from send2trash import send2trash
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageTk, ImageOps
import pywinctl

from src.config import CONFIG
from src.constants import FULLSCREEN_TOLERANCE, INIT_X, INIT_Y, VISIBILITY_POLL_INTERVAL

class Main:
    def __init__(self):

        self.OPEN_PATH = str(files('res') / 'open.png')
        self.CLOSE_PATH = str(files('res') / 'close.png')
        self.OPEN_ICON = str(files('res') / 'open.ico')
        self.CLOSE_ICON = str(files('res') / 'close.ico')

        self.root = TkinterDnD.Tk()

        self.root.geometry(f'{INIT_X}{INIT_Y}')

        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes("-transparentcolor", "#ffffff")
        self.root.config(bg="#ffffff")

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self._on_drop)
        self.root.dnd_bind('<<DropEnter>>', self._on_enter)
        self.root.dnd_bind('<<DropLeave>>', self._on_leave)

        self.root.bind('<ButtonPress-1>', self._on_lmb_press)
        self.root.bind('<ButtonRelease-1>', self._on_release)
        self.root.bind('<ButtonRelease-3>', self._on_release)

        self.root.bind('<B3-Motion>', self._move)
        self.root.bind('<B1-Motion>', self._move)

        self.root.bind('<Button-3>', self._start_move)

        self.root.bind('<Double-Button-1>', self._reset_pos)
        self.root.bind('<Double-Button-3>', self._reset_pos)

        self.root.bind('<ButtonPress-2>', self._temp_hide)

        self.buffer = Queue()

        self.close_image = Image.open(self.CLOSE_PATH)
        self.open_image = Image.open(self.OPEN_PATH)

        self.close_image_flipped = ImageOps.mirror(self.close_image)
        self.open_image_flipped = ImageOps.mirror(self.open_image)

        self.close_image = ImageTk.PhotoImage(self.close_image)
        self.open_image = ImageTk.PhotoImage(self.open_image)

        self.close_image_flipped = ImageTk.PhotoImage(self.close_image_flipped)
        self.open_image_flipped = ImageTk.PhotoImage(self.open_image_flipped)

        self.mouth_open = False

        self.image_label = tk.Label(self.root,
                            bg="#ffffff",
                            bd=0)
        self.image_label.pack()


        self.show = True
        self.temp_hide_time = 0
        self.root.after(0, self._update_visibility)

        self.x = 0
        self.y = 0
        self.moving = False

        self.close_icon = Image.open(self.CLOSE_ICON)
        self.open_icon = Image.open(self.OPEN_ICON)

        self.close_icon_flipped = ImageOps.mirror(self.close_icon)
        self.open_icon_flipped = ImageOps.mirror(self.open_icon)

        menu = (
            MenuItem('Show/Hide', self._toggle, default=True),
            MenuItem('Hide On Fullscreen', lambda *_: self._toggle_option('fullscreen_hide'), checked=lambda *_: CONFIG.fullscreen_hide),
            MenuItem('LMB Drag', lambda *_: self._toggle_option('lmb_drag'), checked=lambda *_: CONFIG.lmb_drag),
            MenuItem('Flip', self._toggle_flip, checked=lambda *_: CONFIG.flip),
            Menu.SEPARATOR,
            MenuItem('Quit', lambda *_: self.root.after(0, self.root.destroy))
        )
        self.icon = Icon('pop-cat', self.close_icon, 'Meow~', menu=menu)

        self._update_image()

    def _flush_buffer(self):
        while True:
            paths = self.buffer.get()
            paths = list(map(Path, paths))
            try:
                send2trash(paths)
            except Exception:
                ...

    def _toggle(self, *_):
        self.show = not self.show

    def _toggle_flip(self, *_):
        self._toggle_option('flip')
        self._update_image()

    def _toggle_option(self, name):
        setattr(CONFIG, name, not getattr(CONFIG, name))

    def _update_image(self, thread_safe=False):
        if thread_safe:
            if self.mouth_open:
                if CONFIG.flip:
                    self.image_label.config(image=self.open_image_flipped)
                    self.icon.icon = self.open_icon_flipped
                else:
                    self.image_label.config(image=self.open_image)
                    self.icon.icon = self.open_icon
            else:
                if CONFIG.flip:
                    self.image_label.config(image=self.close_image_flipped)
                    self.icon.icon = self.close_icon_flipped
                else:
                    self.image_label.config(image=self.close_image)
                    self.icon.icon = self.close_icon
        else:
            self.root.after(0, self._update_image, thread_safe=True)

    def _open(self):
        self.mouth_open = True
        self._update_image()

    def _close(self):
        self.mouth_open = False
        self._update_image()

    def _on_enter(self, event):
        self._open()
        return event.action

    def _on_leave(self, event):
        self._close()

    def _on_lmb_press(self, event):
        self._open()
        if CONFIG.lmb_drag:
            self._start_move(event)

    def _on_release(self, event):
        if event.num == 1:
            self._close()
        self.moving = False

    def _on_drop(self, event):
        self._close()
        self.buffer.put(self.root.tk.splitlist(event.data))
        return event.action

    def _temp_hide(self, *_):
        self.temp_hide_time = time.time()

    def _is_fullscreen(self):
        try:
            window = pywinctl.getActiveWindow()
            if window is None:
                return False
            else:
                box = window.box
                width, height = pywinctl.getScreenSize()
                return (box.width >= width-FULLSCREEN_TOLERANCE and box.height >= height - FULLSCREEN_TOLERANCE)
        except Exception:
            return False

    def _update_visibility(self):
        if self.show and (not self._is_fullscreen() or not CONFIG.fullscreen_hide) and (time.time() - self.temp_hide_time > CONFIG.temp_hide_time):
            if self.root.state() == 'withdrawn':
                self.root.deiconify()
        else:
            if self.root.state() != 'withdrawn':
                self.root.withdraw()
        self.root.after(VISIBILITY_POLL_INTERVAL, self._update_visibility)

    def _start_move(self, event):
        self.moving = True
        self.x = event.x
        self.y = event.y

    def _move(self, event):
        if self.moving:
            self.root.geometry(f'+{event.x_root-self.x}+{event.y_root-self.y}')

    def _reset_pos(self, event):
        if event.num == 1:
            self._open()
        if event.num != 1 or CONFIG.lmb_drag:
            self.root.geometry(f'{INIT_X}{INIT_Y}')
            self.moving = False

    def run(self):
        Thread(target=self._flush_buffer, daemon=True).start()
        Thread(target=self.icon.run, daemon=True).start()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            ...


def main():
    Main().run()
