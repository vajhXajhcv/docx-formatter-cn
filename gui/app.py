"""
PySide6 GUI for docx-formatter-cn.

Features:
- Template selection
- Input file picker (Markdown or existing docx)
- Output file picker
- Progress bar and status log
- Drag-and-drop support
"""

import sys
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog,
    QProgressBar, QTextEdit, QMessageBox, QGroupBox, QSplitter,
)
from PySide6.QtCore import Qt, QThread, Signal, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent

# Add src to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from docx_formatter.config import get_preset
from docx_formatter.converter.markdown_parser import parse_markdown
from docx_formatter.converter.docx_builder import build_docx
from docx_formatter.cli import main as cli_main


class WorkerThread(QThread):
    progress = Signal(int, str)
    finished_ok = Signal(str)
    finished_error = Signal(str)

    def __init__(self, mode: str, input_path: str, output_path: str, template: str):
        super().__init__()
        self.mode = mode
        self.input_path = input_path
        self.output_path = output_path
        self.template = template

    def run(self):
        try:
            self.progress.emit(10, "正在加载配置...")
            config = get_preset(self.template)

            if self.mode == "convert":
                self.progress.emit(30, "正在解析 Markdown...")
                md_text = Path(self.input_path).read_text(encoding="utf-8")
                blocks = parse_markdown(md_text)

                self.progress.emit(60, "正在构建文档...")
                image_dir = str(Path(self.input_path).parent)
                build_docx(blocks, config, self.output_path, image_base_dir=image_dir)

            elif self.mode == "format":
                self.progress.emit(30, "正在加载文档...")
                from docx_formatter.formatter import format_existing_docx
                self.progress.emit(50, "正在应用模板格式...")
                format_existing_docx(self.input_path, self.output_path, config, add_toc=False)
                self.progress.emit(80, "正在保存...")

            self.progress.emit(100, "完成")
            self.finished_ok.emit(self.output_path)
        except Exception as e:
            self.finished_error.emit(str(e))


class DropArea(QGroupBox):
    file_dropped = Signal(str)

    def __init__(self, title="拖拽文件到此处"):
        super().__init__(title)
        self.setAcceptDrops(True)
        self.setMinimumHeight(80)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QGroupBox {
                border: 2px dashed #888;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #666;
            }
        """)
        layout = QVBoxLayout(self)
        self.label = QLabel("支持 .md / .docx 文件")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.lower().endswith((".md", ".docx")):
                self.file_dropped.emit(path)
            else:
                QMessageBox.warning(self, "格式不支持", "仅支持 .md 和 .docx 文件")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("docx-formatter-cn 文档排版工具")
        self.setMinimumSize(700, 500)
        self.worker = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("操作模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Markdown 转 Word", "修正现有 Word 格式"])
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # Template selection
        tmpl_layout = QHBoxLayout()
        tmpl_layout.addWidget(QLabel("模板预设:"))
        self.tmpl_combo = QComboBox()
        self.tmpl_combo.addItems(["课程论文", "毕业论文", "数学建模", "公文"])
        tmpl_layout.addWidget(self.tmpl_combo)
        tmpl_layout.addStretch()
        layout.addLayout(tmpl_layout)

        # Drop area
        self.drop_area = DropArea()
        self.drop_area.file_dropped.connect(self._on_file_dropped)
        layout.addWidget(self.drop_area)

        # Input file
        input_group = QGroupBox("输入文件")
        input_layout = QHBoxLayout(input_group)
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("选择 Markdown 或 docx 文件...")
        input_layout.addWidget(self.input_edit)
        btn_input = QPushButton("浏览...")
        btn_input.clicked.connect(self._pick_input)
        input_layout.addWidget(btn_input)
        layout.addWidget(input_group)

        # Output file
        output_group = QGroupBox("输出文件")
        output_layout = QHBoxLayout(output_group)
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("选择输出路径...")
        output_layout.addWidget(self.output_edit)
        btn_output = QPushButton("浏览...")
        btn_output.clicked.connect(self._pick_output)
        output_layout.addWidget(btn_output)
        layout.addWidget(output_group)

        # Execute button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.run_btn = QPushButton("开始处理")
        self.run_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 32px;
                font-size: 15px;
                font-weight: bold;
                background-color: #2d8cf0;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #1a7ae0; }
            QPushButton:disabled { background-color: #aaa; }
        """)
        self.run_btn.clicked.connect(self._run)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Log
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("状态日志...")
        self.log.setMaximumHeight(120)
        layout.addWidget(self.log)

        self._on_mode_changed(0)

    def _on_mode_changed(self, idx: int):
        self.drop_area.setTitle("拖拽文件到此处" if idx == 0 else "拖拽 .docx 文件到此处")

    def _on_file_dropped(self, path: str):
        self.input_edit.setText(path)
        self._auto_set_output(path)

    def _pick_input(self):
        mode = self.mode_combo.currentIndex()
        if mode == 0:
            path, _ = QFileDialog.getOpenFileName(self, "选择 Markdown 文件", "", "Markdown (*.md);;All Files (*)")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择 Word 文件", "", "Word (*.docx);;All Files (*)")
        if path:
            self.input_edit.setText(path)
            self._auto_set_output(path)

    def _auto_set_output(self, input_path: str):
        if not self.output_edit.text():
            p = Path(input_path)
            self.output_edit.setText(str(p.parent / f"{p.stem}_formatted.docx"))

    def _pick_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存为", "", "Word (*.docx)")
        if path:
            self.output_edit.setText(path)

    def _log(self, msg: str):
        self.log.append(msg)

    def _run(self):
        input_path = self.input_edit.text().strip()
        output_path = self.output_edit.text().strip()
        template = self.tmpl_combo.currentText()
        mode = "convert" if self.mode_combo.currentIndex() == 0 else "format"

        if not input_path or not Path(input_path).exists():
            QMessageBox.warning(self, "错误", "请选择有效的输入文件")
            return
        if not output_path:
            QMessageBox.warning(self, "错误", "请指定输出文件路径")
            return

        self.run_btn.setEnabled(False)
        self.progress.setValue(0)
        self.log.clear()
        self._log(f"开始处理: {input_path}")
        self._log(f"模板: {template}")

        self.worker = WorkerThread(mode, input_path, output_path, template)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self._on_success)
        self.worker.finished_error.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, value: int, msg: str):
        self.progress.setValue(value)
        self._log(msg)

    def _on_success(self, path: str):
        self.run_btn.setEnabled(True)
        self._log(f"完成: {path}")
        QMessageBox.information(self, "完成", f"文档已保存到:\n{path}")

    def _on_error(self, msg: str):
        self.run_btn.setEnabled(True)
        self._log(f"错误: {msg}")
        QMessageBox.critical(self, "错误", msg)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
