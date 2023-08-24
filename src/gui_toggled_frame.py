# https://stackoverflow.com/questions/13141259/expandable-and-contracting-frame-in-tkinter

import tkinter as tk
from tkinter import ttk
from typing import Any, Union


class ToggledFrame(tk.Frame):
    """
    >>> t = ToggledFrame(root, text="always visible text")
    >>> t.grid()
    >>> ttk.Label(t.sub_frame, text="text that can be hidden").grid()
    """

    _showing: tk.IntVar
    _top_frame: ttk.Frame
    _toggle_button: ttk.Checkbutton
    _title_frame: ttk.Frame
    _sub_frame: ttk.Frame

    def __init__(self, parent: Union[tk.Frame, tk.Tk, ttk.Frame], text: str = "", *args: Any, **options: Any):
        super().__init__(parent, *args, **options)

        self._showing = tk.IntVar()
        self._showing.set(0)

        self._top_frame = ttk.Frame(self)
        self._top_frame.pack(fill="x", expand=1)

        self._toggle_button = ttk.Checkbutton(self._top_frame, width=2, text='>', command=self.toggle,
                                              variable=self._showing, style='Toolbutton')
        self._toggle_button.pack(side="left")

        self._title_frame = ttk.Frame(self._top_frame)
        self._title_frame.pack(side="left", fill="x", expand=1)

        if len(text):
            ttk.Label(self._title_frame, text=text).pack(side="left", fill="x", expand=1)

        self._sub_frame = ttk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self) -> None:
        if bool(self._showing.get()):
            self._sub_frame.pack(fill="x", expand=1)
            self._toggle_button.configure(text='V')
        else:
            self._sub_frame.forget()
            self._toggle_button.configure(text='>')

    @property
    def showing(self) -> bool:
        return bool(self._showing.get())

    @property
    def toggle_button(self) -> ttk.Checkbutton:
        return self._toggle_button

    @property
    def title_frame(self) -> ttk.Frame:
        return self._title_frame

    @property
    def sub_frame(self) -> ttk.Frame:
        return self._sub_frame
