import os, requests, random

def download_pdf(url, save_path):
    """Download a pdf from a url and save it

    @param url: url to the pdf
    @param save_path: path to save the pdf
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("PDF downloaded successfully!")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")


def generate_random_home_automation_pdf():
    # Generate a random number for the PDF
    random_number = random.randint(1000, 9999)
    
    # Create PDF file name
    pdf_file_name = f"home_automation_{random_number}.pdf"
    
    # Generate or save the PDF with the random number
    # (You would implement the PDF generation or saving logic here)
    
    # For demonstration purposes, print the generated PDF file name
    print(f"Generated PDF: {pdf_file_name}")
    
    return pdf_file_name


def delete_files_and_folders(directory):
    # Get list of all files and folders in the directory
    contents = os.listdir(directory)
    
    # Iterate over each item in the directory
    for item in contents:
        # Create full path to the item
        item_path = os.path.join(directory, item)
        
        # Check if item is a file
        if os.path.isfile(item_path):
            # If it's a file, delete it
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        # Check if item is a directory
        elif os.path.isdir(item_path):
            # If it's a directory, recursively call the function to delete its contents
            delete_files_and_folders(item_path)
            # After deleting the contents, remove the directory itself
            os.rmdir(item_path)
            print(f"Deleted directory: {item_path}")


# Usage:
urls: list[str] = [
    "https://www.pdfdrive.com/download.pdf?id=34820119&h=090b23accd028f9055097590e71bd947",
    "https://www.pdfdrive.com/download.pdf?id=199816422&h=bfb14c65857acf294f6419ea19e14ad2",
    "https://www.pdfdrive.com/download.pdf?id=195285588&h=62ac75c2c2620c8a91d6a9c3fc27935c",
    "https://www.pdfdrive.com/download.pdf?id=21026170&h=bcd08430e23df9cee82c857619d12c0b",
    ]

delete_files_and_folders("./ava/resources")

for url in list(set(urls)):
    download_pdf(url, f"./ava/resources/{generate_random_home_automation_pdf()}")
