import time
import json
from typing import Callable
from pathlib import Path

import psutil
import win32gui
import win32process
import pynput.mouse
import pynput.keyboard
import prometheus_client
from PIL import ImageGrab, ImageStat


存储目录 = Path.home() / '.negate-hypnotic'
存储目录.mkdir(exist_ok=True)


prometheus_client.start_http_server(2333)
_Counters = {}

def _记录(name, *args):
    t = time.time()
    s = json.dumps([t, name, args], ensure_ascii=False, default=_json_default)
    print('记录', s)
    with open(存储目录 / f'{int(t)//3600}.json', 'a', encoding='utf8') as f:
        f.write(s + '\n')
    if name not in _Counters:
        _Counters[name] = prometheus_client.Counter(name, name)
    _Counters[name].inc()

_上次记录 = {}

def _消重记录(name, *args):
    if _上次记录.get(name) == args:
        return
    _上次记录[name] = args
    _记录(name, *args)


def _冷却时间(t: float):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if time.time() - wrapper.last_call_time < t:
                return
            wrapper.last_call_time = time.time()
            return func(*args, **kwargs)
        wrapper.last_call_time = 0
        return wrapper
    return decorator


def _json_default(obj):
    if isinstance(obj, pynput.mouse.Button):
        return obj._name_
    if isinstance(obj, pynput.keyboard.Key):
        return obj._name_
    if isinstance(obj, pynput.keyboard.KeyCode):
        return obj.char
    raise TypeError(f'{obj} is not JSON serializable')

def _回调记录(name):
    def wrapper(*args):
        return _记录(name, *args)
    return wrapper

_pressed = set()

def keyboard_press(key):
    if key in _pressed:
        return
    _pressed.add(key)
    _记录('keyboard_press', key)

def keyboard_release(key):
    if key in _pressed:
        _pressed.remove(key)
    _记录('keyboard_release', key)


@_冷却时间(0.1)
def 窗口():
    hwnd = win32gui.GetForegroundWindow()
    try:
        rect = win32gui.GetWindowRect(hwnd)
    except Exception:
        rect = None
    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        exe = psutil.Process(pid).exe()
    except Exception:
        exe = None
    _消重记录('foreground_window', rect, win32gui.GetWindowText(hwnd), exe)


@_冷却时间(3)
def 截图():     # 似乎会轻微地卡1下，先不要
    screenshot = ImageGrab.grab()
    s = ImageStat.Stat(screenshot)
    _消重记录('screenshot', screenshot.size, s.mean, s.stddev)


if __name__ == '__main__':
    pynput.mouse.Listener(
        on_move=_冷却时间(0.2)(_回调记录('mouse_move')),
        on_click=_回调记录('mouse_click'),
        on_scroll=_冷却时间(0.2)(_回调记录('mouse_scroll')),
    ).start()

    pynput.keyboard.Listener(
        on_press=keyboard_press,
        on_release=keyboard_release,
    ).start()

    while True:
        窗口()
        time.sleep(0.01)
