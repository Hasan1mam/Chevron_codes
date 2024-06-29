
import os
import shutil
import PyPDF2

def select_pdf_file(folder_path):
    # List all PDF files in the specified folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return None

    # Display available PDF files for selection
    print("Available PDF files:")
    for i, pdf_file in enumerate(pdf_files):
        print(f"{i + 1}. {pdf_file}")

    # Ask user to select a PDF file by index
    selection = int(input("Enter the number of the PDF file you want to rename (1, 2, ...): ")) - 1

    if selection < 0 or selection >= len(pdf_files):
        print("Invalid selection.")
        return None

    return os.path.join(folder_path, pdf_files[selection])

def extract_file_type(pdf_file_path):
    # Open the PDF file and extract the first page's text to determine if it's an order or petition
    file_type = None
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            first_page_text = pdf_reader.getPage(0).extractText()
            if 'order' in first_page_text.lower():
                file_type = 'order'
            elif 'petition' in first_page_text.lower():
                file_type = 'petition'
    except Exception as e:
        print(f"Error occurred while extracting PDF content: {e}")

    return file_type

def rename_and_move_pdf(pdf_file_path, writ_number, year, file_type):
    # Construct the new file name based on the naming convention
    file_type_str = 'Order' if file_type == 'o' else 'Petition'
    new_file_name = f"Writ Petition No. {writ_number} of {year}_{file_type_str}.pdf"

    # Create destination folder name based on the writ number and year
    destination_folder_name = f"Writ Petition No. {writ_number} of {year}"

    # Get the directory path of the PDF file
    pdf_directory = os.path.dirname(pdf_file_path)

    # Move the PDF file to the destination folder
    destination_folder_path = os.path.join(pdf_directory, destination_folder_name)
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    new_file_path = os.path.join(destination_folder_path, new_file_name)

    if os.path.exists(new_file_path):
        print(f"A file named '{new_file_name}' already exists in '{destination_folder_name}'.")
        action = input("Choose action (enter 'o' to overwrite, 's' to skip, 'r' to rename): ").lower()

        if action == 'o':
            try:
                os.remove(new_file_path)  # Remove existing file
                shutil.move(pdf_file_path, new_file_path)
                print(f"File '{os.path.basename(pdf_file_path)}' renamed and moved successfully to '{destination_folder_name}'.")
            except Exception as e:
                print(f"Error occurred while moving file: {e}")
        elif action == 'r':
            # Prompt user to enter a new file name
            new_file_name = input("Enter a new file name: ")
            new_file_path = os.path.join(destination_folder_path, new_file_name)
            try:
                shutil.move(pdf_file_path, new_file_path)
                print(f"File '{os.path.basename(pdf_file_path)}' renamed and moved successfully to '{destination_folder_name}' as '{new_file_name}'.")
            except Exception as e:
                print(f"Error occurred while moving file: {e}")
        else:
            print(f"File '{os.path.basename(pdf_file_path)}' was not moved.")

    else:
        try:
            shutil.move(pdf_file_path, new_file_path)
            print(f"File '{os.path.basename(pdf_file_path)}' renamed and moved successfully to '{destination_folder_name}'.")
        except Exception as e:
            print(f"Error occurred while moving file: {e}")


if __name__ == "__main__":
    # Specify the folder path where the PDF files are located
    folder_path = r'C:\Users\zgrd\Downloads\Scans\Writ Petition\13.06'

    # Select a PDF file from the specified folder
    selected_pdf_file = select_pdf_file(folder_path)

    if selected_pdf_file:
        # Ask user for writ number, year, and file type (order/petition)
        writ_number = input("Enter writ number: ")
        year = input("Enter year: ")

        file_type = input("Enter file type ('o' for order, 'p' for petition): ").lower()

        # Validate file type
        if file_type != 'o' and file_type != 'p':
            print("Invalid file type. Please enter 'o' for order or 'p' for petition.")
        else:
            # Rename and move the selected PDF file
            rename_and_move_pdf(selected_pdf_file, writ_number, year, file_type)
