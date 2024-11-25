import self
from PySide6.QtWidgets import QProgressBar

self.progress_bar = QProgressBar(self)
self.progress_bar.setGeometry(0, 0, 300, 25)
self.progress_bar.setMaximum(100)
