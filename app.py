import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from main import add_lines_to_pdf  # Assuming add_lines_to_pdf function is in main.py


class PDFInsertionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_pdf_label = None
        self.input_pdf_edit = None
        self.input_pdf_btn = None
        self.output_pdf_label = None
        self.output_pdf_edit = None
        self.lines_file_label = None
        self.lines_file_edit = None
        self.lines_file_btn = None
        self.font_label = None
        self.font_edit = None
        self.font_size_label = None
        self.font_size_edit = None
        self.text_height_label = None
        self.text_height_edit = None
        self.initial_y_label = None
        self.initial_y_edit = None
        self.left_margin_label = None
        self.left_margin_edit = None
        self.right_margin_label = None
        self.right_margin_edit = None
        self.ignore_first_pages_label = None
        self.ignore_first_pages_edit = None
        self.ignore_last_pages_label = None
        self.ignore_last_pages_edit = None
        self.shuffle_lines_checkbox = None
        self.submit_btn = None
        self.pos_x = 500
        self.pos_y = 300
        self.screen_width = 450
        self.screen_height = 400

        self.setWindowTitle("PDF Text Insertion App")
        self.setGeometry(self.pos_x, self.pos_y, self.screen_width, self.screen_height)

        self.initUI()

    def initUI(self):
        # Create widgets
        self.input_pdf_label = QLabel("Input PDF Path:")
        self.input_pdf_edit = QLineEdit()
        self.input_pdf_edit.setMaximumWidth(325)
        self.input_pdf_btn = QPushButton("Browse")
        self.input_pdf_btn.clicked.connect(self.browse_input_pdf)

        self.output_pdf_label = QLabel("Output PDF Name:")
        self.output_pdf_edit = QLineEdit("final_pdf")
        self.output_pdf_edit.setMaximumWidth(325)

        self.lines_file_label = QLabel("Lines File Path:")
        self.lines_file_edit = QLineEdit("assets/lines.csv")
        self.lines_file_edit.setMaximumWidth(325)
        self.lines_file_btn = QPushButton("Browse")
        self.lines_file_btn.clicked.connect(self.browse_lines_file)

        self.font_label = QLabel("Font Name in the System:")
        self.font_edit = QLineEdit("Helvetica-Oblique")

        self.font_size_label = QLabel("Font Size:")
        self.font_size_edit = QLineEdit("12")

        self.text_height_label = QLabel("Text Height:")
        self.text_height_edit = QLineEdit("25")

        self.initial_y_label = QLabel("Initial Y:")
        self.initial_y_edit = QLineEdit("46")

        self.left_margin_label = QLabel("Left Margin:")
        self.left_margin_edit = QLineEdit("40")

        self.right_margin_label = QLabel("Right Margin:")
        self.right_margin_edit = QLineEdit("40")

        self.ignore_first_pages_label = QLabel("Ignore First Pages:")
        self.ignore_first_pages_edit = QLineEdit("2")

        self.ignore_last_pages_label = QLabel("Ignore Last Pages:")
        self.ignore_last_pages_edit = QLineEdit("0")

        self.shuffle_lines_checkbox = QCheckBox("Shuffle Lines", checked=True)

        self.submit_btn = QPushButton("Generate PDF")
        self.submit_btn.clicked.connect(self.generate_pdf)

        # Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_pdf_label)
        hbox = QHBoxLayout()
        hbox.addWidget(self.input_pdf_edit)
        hbox.addWidget(self.input_pdf_btn)
        vbox.addLayout(hbox)

        vbox.addWidget(self.output_pdf_label)
        vbox.addWidget(self.output_pdf_edit)

        vbox.addWidget(self.lines_file_label)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lines_file_edit)
        hbox.addWidget(self.lines_file_btn)
        vbox.addLayout(hbox)

        vbox.addWidget(self.font_label)
        vbox.addWidget(self.font_edit)

        hbox = QHBoxLayout()
        hbox.addWidget(self.font_size_label)
        hbox.addWidget(self.font_size_edit)
        hbox.addWidget(self.text_height_label)
        hbox.addWidget(self.text_height_edit)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.initial_y_label)
        hbox.addWidget(self.initial_y_edit)
        hbox.addWidget(self.left_margin_label)
        hbox.addWidget(self.left_margin_edit)
        hbox.addWidget(self.right_margin_label)
        hbox.addWidget(self.right_margin_edit)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ignore_first_pages_label)
        hbox.addWidget(self.ignore_first_pages_edit)
        hbox.addWidget(self.ignore_last_pages_label)
        hbox.addWidget(self.ignore_last_pages_edit)
        vbox.addLayout(hbox)

        vbox.addWidget(self.shuffle_lines_checkbox)
        vbox.addWidget(self.submit_btn)

        central_widget.setLayout(vbox)

    def browse_input_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filter = "PDF File (*.pdf)"
        filename, _ = QFileDialog.getOpenFileName(self, "Select Input PDF File", "", file_filter, options=options)
        if filename:
            self.input_pdf_edit.setText(filename)

    def browse_lines_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filter = "Text File (*.txt *.csv *.xlsx)"
        filename, _ = QFileDialog.getOpenFileName(self, "Select Lines File", "", file_filter, options=options)
        if filename:
            self.lines_file_edit.setText(filename)

    def generate_pdf(self):
        input_pdf_path = self.input_pdf_edit.text().strip()
        output_pdf_name = self.output_pdf_edit.text().strip()
        lines_file_path = self.lines_file_edit.text().strip()
        font = self.font_edit.text().strip()
        font_size = int(self.font_size_edit.text().strip())
        text_height = int(self.text_height_edit.text().strip())
        initial_y = int(self.initial_y_edit.text().strip())
        left_margin = int(self.left_margin_edit.text().strip())
        right_margin = int(self.right_margin_edit.text().strip())
        ignore_first_pages = int(self.ignore_first_pages_edit.text().strip())
        ignore_last_pages = int(self.ignore_last_pages_edit.text().strip())
        shuffle_lines = self.shuffle_lines_checkbox.isChecked()

        # Process output_pdf_path to be "output/{USER_INPUT}.pdf"
        if not output_pdf_name.endswith(".pdf"):
            output_pdf_name += ".pdf"
        output_pdf_path = f"output/{output_pdf_name}"

        try:
            add_lines_to_pdf(input_pdf_path=input_pdf_path,
                             output_pdf_path=output_pdf_path,
                             lines_file_path=lines_file_path,
                             font_size=font_size,
                             left_margin=left_margin,
                             right_margin=right_margin,
                             text_height=text_height,
                             initial_y=initial_y,
                             font=font,
                             shuffle_lines=shuffle_lines,
                             ignore_first_pages=ignore_first_pages,
                             ignore_last_pages=ignore_last_pages)
            QMessageBox.information(self, "Success", "PDF generated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PDF: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFInsertionApp()
    window.show()
    sys.exit(app.exec_())
