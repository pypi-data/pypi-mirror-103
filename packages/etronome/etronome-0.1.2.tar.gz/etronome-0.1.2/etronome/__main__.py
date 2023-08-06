from argparse import ArgumentParser
from importlib import resources

from . import assets
from .model import Model
from .sound import play_sound
from .view.top_view import TopView


def get_bpm() -> int:
    parser = ArgumentParser()
    parser.add_argument('bpm', type=float, default=100, nargs='?')
    return parser.parse_args().bpm


def run_metronome(bpm: int) -> None:
    with resources.path(assets, 'click.wav') as path:
        model = Model(bpm=bpm, beat=lambda: play_sound(path))
        with model:
            window = TopView(model=model)
            window.mainloop()


def main() -> None:
    bpm = get_bpm()
    run_metronome(bpm)


if __name__ == '__main__':
    main()
