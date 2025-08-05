import sys
import subprocess
import webbrowser
import os
import signal
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

PROJECT_DIR = r"C:\Users\Administrator\Desktop\guanwang250612"
PORT = 8000

class ServerController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("本地服务启动器")
        self.setFixedSize(300, 180)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()
        self.status_label = QLabel("服务状态：未启动")
        layout.addWidget(self.status_label)

        self.start_button = QPushButton("启动服务")
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("停止服务")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.server_process = None

        # 托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("application-exit"))

        tray_menu = QMenu()
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.showNormal)
        tray_menu.addAction(show_action)

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def start_server(self):
        if self.server_process is None:
            self.server_process = subprocess.Popen(
                ["python", "-m", "http.server", str(PORT)],
                cwd=PROJECT_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.status_label.setText(f"服务状态：运行中（端口 {PORT}）")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            webbrowser.open(f"http://localhost:{PORT}")

    def stop_server(self):
        if self.server_process:
            try:
                parent = psutil.Process(self.server_process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                self.server_process = None
                self.status_label.setText("服务状态：已停止")
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
            except Exception as e:
                self.status_label.setText(f"停止失败：{e}")

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def exit_app(self):
        self.stop_server()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = ServerController()
    window.show()
    sys.exit(app.exec_())
