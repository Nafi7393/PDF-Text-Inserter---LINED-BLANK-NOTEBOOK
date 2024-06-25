import textwrap
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import random
import os
import pandas as pd


def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        data = pd.read_csv(file_path)
    elif file_extension == '.xlsx':
        data = pd.read_excel(file_path, engine='openpyxl')
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]  # Remove any leading/trailing whitespace
        return lines
    else:
        raise ValueError("Unsupported file format")

    # Assuming the lines are in the first column (A) for CSV and XLSX files
    lines = data.iloc[:, 0].tolist()
    return lines


def add_lines_to_pdf(input_pdf_path, output_pdf_path, lines_file_path,
                     font_size=12, left_margin=40, right_margin=40, text_height=25, initial_y=46,
                     font="Helvetica-Oblique", shuffle_lines=True):
    lines = read_file(lines_file_path)
    print(lines)
    print(len(lines))

    # Randomize the list
    if shuffle_lines:
        random.shuffle(lines)

    # Open the existing PDF
    existing_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # Add the first few pages as they are
    for page in existing_pdf.pages[:2]:
        output_pdf.add_page(page)

    # Get the page size dynamically
    page_size = (float(existing_pdf.pages[0].mediabox[2]), float(existing_pdf.pages[0].mediabox[3]))

    # Calculate the available width for text
    available_width = page_size[0] - left_margin - right_margin

    line_count = len(lines)
    page_count = len(existing_pdf.pages) - 2  # Number of pages where we can place lines

    # Distribute the lines proportionally across the pages
    pages_with_lines = sorted(random.sample(range(page_count), line_count))

    # Iterate through each page and add lines
    line_index = 0
    for i, page in enumerate(existing_pdf.pages[2:]):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=page_size)

        if i in pages_with_lines and line_index < line_count:
            text = lines[line_index].strip()
            line_index += 1
            can.setFont(font, font_size)

            # Calculate the text width
            text_width = can.stringWidth(text, font, font_size)

            # If the text is wider than the available width, wrap it to the next line
            if text_width > available_width:
                lines_to_draw = []
                words = text.split()
                current_line = []

                if text_width > 550:
                    width = 70
                else:
                    width = 55

                para = textwrap.wrap(text, width=width)

                for word in words:
                    if can.stringWidth(' '.join(current_line + [word]), font, font_size) <= available_width:
                        current_line.append(word)
                    else:
                        lines_to_draw.append(' '.join(current_line))
                        current_line = [word]

                lines_to_draw.append(' '.join(current_line))

                # Calculate the height of wrapped text
                text_height = len(lines_to_draw) * text_height / 2

                # Calculate the starting y coordinate for the first line
                y = initial_y + initial_y - 21

                for line in para:
                    x = (page_size[0] - can.stringWidth(line, font, font_size)) / 2
                    can.setFillColorRGB(0, 0, 0, alpha=0.3)
                    can.drawString(x, y, line)
                    y -= text_height
            else:
                # Calculate the coordinates to center the text
                x = (page_size[0] - text_width) / 2
                y = initial_y

                can.setFillColorRGB(0, 0, 0, alpha=0.3)
                can.drawString(x, y, text)

        can.save()
        packet.seek(0)

        overlay = PdfReader(packet)
        if len(overlay.pages) > 0:
            page.merge_page(overlay.pages[0])
        else:
            pass

        output_pdf.add_page(page)

    output_stream = io.BytesIO()
    output_pdf.write(output_stream)

    # Write the combined PDF to a file
    with open(output_pdf_path, 'wb') as f:
        f.write(output_stream.getvalue())


# Example usage
add_lines_to_pdf(input_pdf_path='assets/line_page_pdf.pdf',
                 output_pdf_path='output/Final - INTERIOR.pdf',
                 lines_file_path='lines.csv',
                 font_size=12, left_margin=40, right_margin=40,
                 text_height=25, initial_y=46, font="Helvetica-Oblique",
                 shuffle_lines=True)
