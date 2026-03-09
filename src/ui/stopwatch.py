from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.events import Timer
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header


def get_time() -> float:
    return float(monotonic())


class TimeDisplay(Digits):
    """Custom time display widget"""

    start_time: reactive[float] = reactive(monotonic)  # type: ignore
    time: reactive[float] = reactive(0.0)
    total: reactive[float] = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer: Timer = self.set_interval(
            interval=1 / 60, callback=self.update_time, pause=True
        )
        # calls the function `update_time` 60 times per second

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)
        # updates the reactive attribute time when called
        # this implicitly calls `watch_time`

    # begins with `watch_` followed by the name of a reactive attribute
    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handle called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)

        if event.button.id == "start":
            time_display.start()
            self.add_class("started")
        elif event.button.id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        yield Button(label="Start", id="start", variant="success")
        yield Button(label="Stop", id="stop", variant="error")
        yield Button(label="Reset", id="reset")
        yield TimeDisplay()


class StopwatchApp(App):
    """a stopwatch app with textual"""

    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [("d", "toggle_dark_mode", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.dark = True
        self.dark_theme: str = "tokyo-night"
        self.light_theme: str = "textual-light"
        self.theme: str = self.dark_theme

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch())

    def action_toggle_dark_mode(self) -> None:
        self.dark = not self.dark
        self.theme = self.dark_theme if self.dark else self.light_theme


if __name__ == "__main__":
    StopwatchApp().run()
