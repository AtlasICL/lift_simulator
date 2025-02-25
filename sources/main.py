import tkinter as tk
import os

from gui import LiftSimulatorGUI

CONFIG_FILEPATH: str = os.path.join("sources", "config.json") # filepath for config.json


def main() -> None:
    root = tk.Tk()
    gui = LiftSimulatorGUI(root, CONFIG_FILEPATH)
    root.mainloop()

if __name__ == "__main__":
    main()