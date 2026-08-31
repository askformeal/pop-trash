from threading import Thread
from pathlib import Path
import tkinter as tk
from importlib.resources import files

from tkinterdnd2 import DND_FILES, TkinterDnD
from send2trash import send2trash
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageTk


class Main:
    def __init__(self):

        self.OPEN_PATH = str(files('res') / 'open.png')
        self.CLOSE_PATH = str(files('res') / 'close.png')
        self.OPEN_ICON = str(files('res') / 'open.ico')
        self.CLOSE_ICON = str(files('res') / 'close.ico')

        self.root = TkinterDnD.Tk()

        self.root.geometry('-100-100')

        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes("-transparentcolor", "#ffffff")
        self.root.config(bg="#ffffff")

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self._on_drop)
        self.root.dnd_bind('<<DropEnter>>', self._on_enter)
        self.root.dnd_bind('<<DropLeave>>', self._on_leave)

        self.root.bind('<ButtonPress-1>', lambda e: self._open())
        self.root.bind('<ButtonRelease-1>', lambda e: self._close())

        self.close_image = ImageTk.PhotoImage(Image.open(self.CLOSE_PATH))
        self.open_image = ImageTk.PhotoImage(Image.open(self.OPEN_PATH))

        self.image_label = tk.Label(self.root,
                            image=self.close_image,
                            bg="#ffffff",
                            bd=0)
        self.image_label.pack()


        self.close_icon = Image.open(self.CLOSE_ICON)
        self.open_icon = Image.open(self.OPEN_ICON)

        menu = (
            MenuItem('Show/Hide', self._toggle, default=True),
            Menu.SEPARATOR,
            MenuItem('Quit', self.root.destroy)
        )
        self.icon = Icon('pop-cat', self.close_icon, 'Meow~', menu=menu)

    def _toggle(self, *_):
        if self.root.state() == 'withdrawn':
            self.root.deiconify()
        else:
            self.root.withdraw()

    def _open(self):
        self.image_label.config(image=self.open_image)
        self.icon.icon = self.open_icon

    def _close(self):
        self.image_label.config(image=self.close_image)
        self.icon.icon = self.close_icon

    def _on_enter(self, event):
        self._open()
        return event.action

    def _on_leave(self, event):
        self._close()

    def _on_drop(self, event):
        self._close()
        paths = []
        for path in self.root.tk.splitlist(event.data):
            paths.append(Path(path))

        send2trash(paths)
        return event.action

    def run(self):
        Thread(target=self.icon.run, daemon=True).start()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            ...
