import os
import shutil
import re

def get_year_group(year, comm_type):
    year = int(year)
    if comm_type == "Incoming Communication":
        if 1990 <= year <= 1999:
            return "1990-1999"
        elif 2000 <= year <= 2004:
            return "2000-2004"
        elif 2005 <= year <= 2010:
            return "2005-2010"
        elif 2011 <= year <= 2015:
            return "2011-2015"
        else:
            return f"{year}"
    elif comm_type == "Outgoing Communication":
        if 1970 <= year <= 1975:
            return "1970-1975"
        elif 1976 <= year <= 1980:
            return "1976-1980"
        elif 1981 <= year <= 1985:
            return "1981-1985"
        elif 1986 <= year <= 1990:
            return "1986-1900"
        elif 1991 <= year <= 1994:
            return "1991-1994"
        elif 1995 <= year <= 1999:
            return "1995-1999"
        elif 2000 <= year <= 2005:
            return "2000-2005"
        elif 2006 <= year <= 2010:
            return "2006-2010"
        elif 2011 <= year <= 2015:
            return "2011-2015"
        elif 2016 <= year <= 2020:
            return "2016-2020"
        elif 2021 <= year <= 2025:
            return "2021-2025"
        elif 2026 <= year <= 2030:
            return "2026-2030"
        else:
            return f"{year}"
    else:
        # For "Unsorted Communication" use Incoming Communication year group
        if 2010 <= year <= 2020:
            return "2010-2020"
        elif 2000 <= year <= 2005:
            return "2000-2005"
        else:
            return f"{year}"

def sort_pdfs_by_type_and_date(folder_path):
    # Define a regular expression pattern to extract type and date
    pattern = re.compile(r'_(Letter(?:\([^\)]*\))?)_.*(\d{2}\.\d{2}\.\d{4})\.pdf', re.IGNORECASE)
    keywords = ["Chevron", "Oxy", "Occidental", "Unocal"]

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                match = pattern.search(file)
                if match:
                    file_type = "Letter"  # Normalize the type to "Letter"
                    date = match.group(2)
                    year = date.split('.')[-1]

                    # Find the position of the first underscore
                    first_underscore_pos = file.find('_')
                    if first_underscore_pos != -1:
                        prefix = file[:first_underscore_pos]
                        suffix = file[first_underscore_pos+1:]

                        # Check the position of keywords
                        if any(keyword in prefix for keyword in keywords):
                            comm_type = "Outgoing Communication"
                        elif any(keyword in suffix for keyword in keywords):
                            comm_type = "Incoming Communication"
                        else:
                            comm_type = "Unsorted Communication"

                        type_folder = os.path.join(folder_path, file_type, comm_type)
                    else:
                        # If there's no underscore, consider it unsorted
                        type_folder = os.path.join(folder_path, file_type, "Unsorted Communication")

                    # Get the year group based on communication type
                    year_group = get_year_group(year, comm_type)

                    # Define the new folder paths
                    year_folder = os.path.join(type_folder, year_group)

                    # Create the directories if they don't exist
                    os.makedirs(year_folder, exist_ok=True)

                    # Move the file to the new directory
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(year_folder, file)
                    shutil.move(old_path, new_path)
                    print(f"Moved {file} to {new_path}")
                else:
                    # Ignore files that do not match the pattern
                    continue

# Example usage
folder_path = 'C:\CAB07_Letters'  # Replace with your folder path
sort_pdfs_by_type_and_date(folder_path)
