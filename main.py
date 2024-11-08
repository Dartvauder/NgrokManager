import tkinter as tk
from configparser import ConfigParser
from ui import NgrokApp

config = ConfigParser()
config.read('config.ini')

language = config.get('general', 'language', fallback='en')

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = NgrokApp(root, language)
        root.mainloop()

    except(TypeError):
        pass
