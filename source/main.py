import tkinter as tk
import os

from source.simulation import LiftSimulatorGUI

CONFIG_FILEPATH: str = os.path.join("source", "config.json") # filepath for config.json


def main():
    root = tk.Tk()
    gui = LiftSimulatorGUI(root, CONFIG_FILEPATH)
    root.mainloop()

if __name__ == "__main__":
    main()