import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader


# PDF Report Class
class PDFReport:
    def __init__(self, results):
        self.results = results

    def create_pdf(self, pdf_filename="backtest_results.pdf"):
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        for index, (strategy_name, output, plot_filename) in enumerate(self.results):
            c.drawString(30, height - 40, f"Strategy {index + 1}: {strategy_name}")
            c.drawString(30, height - 60, str(output))

            # Draw the plot image
            if os.path.exists(plot_filename):
                image = ImageReader(plot_filename)
                c.drawImage(image, 30, height - 500, width=550, preserveAspectRatio=True, mask='auto')

            c.showPage()  # Create a new page for each strategy

        c.save()
        print(f"PDF report saved as {pdf_filename}")
