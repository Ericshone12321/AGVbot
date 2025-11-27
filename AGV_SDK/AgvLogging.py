import logging
import tkinter as tk
import datetime
import os
from typing import Optional

class TkTextHandler(logging.Handler):
    """將 log 輸出到 Tkinter Text 的 Handler"""
    def __init__(self, text_widget: tk.Text):
        super().__init__()
        self.text = text_widget

    def emit(self, record):
        msg = self.format(record)
        # 用 after 確保在主執行緒更新 UI
        self.text.after(0, lambda: self._append(msg + "\n"))

    def _append(self, msg):
        self.text.insert(tk.END, msg)
        self.text.see(tk.END)

def setup_logging(text_widget: Optional[tk.Text] = None):
    """初始化 logging，並將 Tkinter Handler 加入"""
    logger = logging.getLogger("log")
    logger.setLevel(logging.INFO)

    if text_widget:
    # UI Handler
        tk_handler = TkTextHandler(text_widget)
        tk_handler.setLevel(logging.INFO)
        tk_handler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
        logger.addHandler(tk_handler)

    # File Handler
    if not os.path.exists("log\\"):
        os.mkdir("log\\")
    file = logging.FileHandler(f"log\\{datetime.datetime.now().strftime('%Y-%m-%d')}.txt")
    file.setLevel(logging.INFO)
    file.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
    logger.addHandler(file)

    #Stream Handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
    logger.addHandler(console)
    
    logger.propagate = False
    return logger