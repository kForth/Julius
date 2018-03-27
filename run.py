import os
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

from julius import JuliusMonitor
from runners import Runner


def set_icon(enabled):
    global icon
    img = Image.new('RGB', (128, 128), (0, 0, 0))
    fill = (250, 250, 250) if enabled else (125, 125, 125)
    ImageDraw.Draw(img).rectangle((128 // 4, 128 // 4, (128 // 4) * 3, (128 // 4) * 3), fill=fill)
    icon.icon = img


def start_stop():
    global running
    print("Stopping" if running else "Starting")
    if running:
        running = False
    else:
        running = True
        monitor_runner.run()
    set_icon(running)


def quit():
    global running
    running = False
    os._exit(1)


def run():
    monitor.run(lambda: running, lambda: False)

if __name__ == "__main__":
    running = True
    monitor = JuliusMonitor()
    monitor_runner = Runner("Monitor", lambda: run())

    menu = Menu(
            MenuItem(lambda text: 'Start' if not running else 'Stop', start_stop),
            MenuItem(lambda text: 'Running' if running else 'Stopped', lambda e: e),
            MenuItem('Quit', quit)
    )
    icon = Icon('Julius', menu=menu)
    set_icon(True)

    def setup(icon):
        icon.visible = True

    monitor_runner.run()
    icon.run(setup)
