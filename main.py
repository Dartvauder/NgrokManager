import tkinter as tk
from configparser import ConfigParser
from TechicalFiles.ui import NgrokApp

config = ConfigParser()
config.read('TechicalFiles/config.ini')

language = config.get('general', 'language', fallback='en')

if __name__ == "__main__":
    root = tk.Tk()
    app = NgrokApp(root)
    root.mainloop()
