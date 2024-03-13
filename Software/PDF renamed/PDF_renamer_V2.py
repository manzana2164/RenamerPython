import os
import fitz
import sys
import shutil
import tempfile
from tqdm import tqdm

# Get the absolute path of the directory containing the script or PyInstaller app
# and change the working directory to that directory
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    app_dir = sys._MEIPASS
else:
    # If the application is not frozen, get the absolute path of the directory
    # containing the script
    app_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

# Change the current working directory to the directory containing the script
os.chdir(app_dir)

# Construct the relative paths to the input and output folders
pdf_folder = os.path.join("PDF files")
output_folder = os.path.join("PDF renamed")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Create the imput folder
os.makedirs(pdf_folder, exist_ok=True)

# Create a temporary directory for the text files
temp_dir = tempfile.mkdtemp()

# Get the list of PDF files in the input folder
pdf_files = [pdf_filename for pdf_filename in os.listdir(
    pdf_folder) if pdf_filename.endswith(".pdf")]

# Set the total number of PDF files for the progress bar
total_files = len(pdf_files)

# Iterate over all PDF files in the input folder
with tqdm(total=total_files, leave=True, desc="Renaming") as pbar:
    for pdf_filename in pdf_files:

        # Construct the relative path to the PDF file
        pdf_path = os.path.join(pdf_folder, pdf_filename)

        # Construct the relative path to the output text file
        text_filename = f"{os.path.splitext(pdf_filename)[0]}.txt"
        text_path = os.path.join(temp_dir, text_filename)

        # Open the PDF file
        doc = fitz.open(pdf_path)

        # Create a new text file in the temporary directory
        with open(text_path, "w") as text_file:
            # Iterate over the pages of the document
            for page in doc:
                # Extract the text from the page
                text = page.get_text()
                # Write the extracted text to the file
                text_file.write(text)

        # Close the PDF file
        doc.close()

        # Open the text file and read its contents into a list of strings
        with open(text_path, "r") as text_file:
            lines = text_file.readlines()

        # Get the value of a specific line (line CUIL in this example)
        line_number = 13
        if line_number < len(lines):
            cuil_value = lines[line_number].rstrip().replace(
                '-', '')  # Remove dash character
        else:
            print(f"Error: line {
                  line_number} does not exist in the file {pdf_filename}")
            continue

        # Build the new filename using the extracted value
        new_filename = f"{cuil_value}.pdf"

        # Construct the relative path to the new PDF file
        new_path = os.path.join(output_folder, new_filename)

        try:
            # Check if the new name already exists
            if not os.path.exists(new_path):
                # Rename the file
                shutil.move(pdf_path, new_path)
            else:
                print(f"Error: a file with the name {
                      new_filename} already exists")
                continue
        except Exception as e:
            print(f"Error renaming {pdf_filename}: {e}")
            continue

        # Delete the text file
        # os.remove(text_path)

        # Update the progress bar description with the filename and new name of the file that is being processed
        pbar.set_description(f"Renaming {pdf_filename} to {new_filename}...")

        # Update the progress bar
        pbar.update()

# Remove the temporary directory
shutil.rmtree(temp_dir)

# Add a screen pause at the end of the script
input("Press Enter to close the program...Thanks for use a Labtech Software Dev")
