import gradio as gr
import markdown2
import pdfkit
import os
from tempfile import NamedTemporaryFile

# Function to convert markdown files to a single PDF and return HTML content
def convert_to_pdf_and_display_html(markdown_files):
    all_html_content = []

    for markdown_file_path in markdown_files:
        # Extract the base name of the file (without extension) for the header
        file_title = os.path.splitext(os.path.basename(markdown_file_path))[0]

        header = f"# {file_title} Section\n"
        footer = f"\n\n# {file_title} Section End\n"

        # Read the content of each file
        with open(markdown_file_path, "r", encoding="utf-8") as file:
            markdown_text = file.read()

            # Combine header, file content, and footer
            combined_text = header + markdown_text + footer
            html_content = markdown2.markdown(combined_text)
            all_html_content.append(html_content)

    combined_html = "".join(all_html_content)

    # Convert combined HTML content to PDF
    pdf = pdfkit.from_string(combined_html, False)

    with NamedTemporaryFile(delete=False, suffix=".pdf", mode='wb') as temp_pdf:
        temp_pdf.write(pdf)
        pdf_path = temp_pdf.name

    return pdf_path, combined_html

# Define the Gradio interface
iface = gr.Interface(
    fn=convert_to_pdf_and_display_html,
    inputs=gr.File(label="Select Markdown Files", file_count="multiple"),
    outputs=[
        gr.File(label="Download Combined PDF"),
        gr.HTML(label="Combined HTML Content")
    ],
    title="Markdown to PDF Converter",
    description="Select multiple Markdown files to combine them into a single PDF file and display the combined HTML."
)

# Run the Gradio app
iface.launch()


