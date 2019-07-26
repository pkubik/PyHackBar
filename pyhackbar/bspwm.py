import io
import json
import subprocess
from threading import Thread
from typing import Iterable

SUBSCRIBE_COMMAND = ["bspc", "subscribe", "desktop"]
DUMP_STATE_COMMAND = ["bspc", "wm", "--dump-state"]


class Desktop:
    def __init__(self, state: dict, parent: 'Monitor'):
        self.parent = parent

        self.id = state["id"]
        self.name = state["name"]
        self.focused = self.id == self.parent.focused_desktop_id
        self.occupied = state["root"] is not None


class Monitor:
    def __init__(self, state, parent: 'State'):
        self.state = state
        self.parent = parent

        self.id = state["id"]
        self.geo_id = f'{state["rectangle"]["x"]},{state["rectangle"]["y"]}'
        self.focused = self.id == parent.focused_monitor_id
        self.focused_desktop_id = state['focusedDesktopId']

    def desktops(self) -> Iterable[Desktop]:
        return (
            Desktop(d, self) for d in self.state["desktops"]
        )


class State:
    def __init__(self):
        self.state = json.loads(subprocess.check_output(DUMP_STATE_COMMAND))
        self.focused_monitor_id = self.state["focusedMonitorId"]

    def monitors(self) -> Iterable[Monitor]:
        return (
            Monitor(m, self) for m in self.state["monitors"]
        )

    def monitor_by_geo_id(self, geo_id: str):
        for m in self.monitors():
            if m.geo_id == geo_id:
                return m
        raise KeyError("No monitor with specified geo id")

    @classmethod
    def subscribe(cls, callback):
        subscribe_command = subprocess.Popen(
            SUBSCRIBE_COMMAND, stdout=subprocess.PIPE)
        for _ in io.TextIOWrapper(subscribe_command.stdout, encoding="utf-8"):
            callback(State())

    @classmethod
    def subscribe_in_new_thread(cls, callback):
        thread = Thread(
            target=cls.subscribe, name='bspwm-subscribtion', args=[callback])
        thread.start()


def next_workspace():
    subprocess.Popen("bspc desktop -f next".split())


def prev_workspace():
    subprocess.Popen("bspc desktop -f prev".split())
