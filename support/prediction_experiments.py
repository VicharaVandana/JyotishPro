import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QTextBrowser

class DashaTransitTableWindow(QWidget):
    def __init__(self, dasha_transit_table_dict):
        super().__init__()
        self.setWindowTitle("Dasha Transit Table")
        self.setGeometry(200, 200, 600, 400)  # Set window size

        layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        
        # Generate HTML Table from Data
        html_content = self.generate_html_table(dasha_transit_table_dict)
        self.text_browser.setHtml(html_content)

        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def generate_html_table(self, dasha_transit_table_dict):
        html = """
        <html>
        <head>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
        <h2>Dasha Transit Table</h2>
        <table>
            <tr>
                <th>Dasha Level</th>
                <th>Lord</th>
                <th>Impacting Sign Numbers</th>
            </tr>
        """

        for key, value in dasha_transit_table_dict.items():
            lord = value["lord"]
            impacting_sign_nums = ", ".join(map(str, value["impacting_signNum"]))

            html += f"""
            <tr>
                <td>{key}</td>
                <td>{lord}</td>
                <td>{impacting_sign_nums}</td>
            </tr>
            """

        html += """
        </table>
        </body>
        </html>
        """

        return html