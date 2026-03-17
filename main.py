import tkinter as tk
from gui import DownloaderGUI

def main():
    root = tk.Tk()
    try:
        style = tk.ttk.Style()
        style.theme_use('clam')
    except:
        pass
    app = DownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()