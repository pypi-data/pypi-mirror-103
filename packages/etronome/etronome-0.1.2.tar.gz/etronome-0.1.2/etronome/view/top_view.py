import tkinter as tk

from .controls import Controls
from .display import Display
from .play_pause import PlayPause
from .tapper import Tapper
from ..model import Model


class TopView(tk.Tk):
    def __init__(self, model: Model) -> None:
        super().__init__()

        self.title('etronome')

        frame = tk.Frame(master=self)

        top_frame = tk.Frame(master=frame)
        left_frame = tk.Frame(master=top_frame)
        display = Display(master=left_frame, model=model)
        display.pack(side=tk.TOP)

        play_pause = PlayPause(master=left_frame, model=model)
        play_pause.pack(side=tk.BOTTOM)

        left_frame.pack(side=tk.LEFT)

        controls = Controls(master=top_frame, model=model)
        controls.pack(side=tk.RIGHT)
        top_frame.pack(side=tk.TOP)

        tapper = Tapper(master=frame, model=model)
        tapper.pack(side=tk.BOTTOM)

        frame.pack()
