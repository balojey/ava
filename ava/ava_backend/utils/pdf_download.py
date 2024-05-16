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


def generate_random_sui_research_pdf():
    # Generate a random number for the PDF
    random_number = random.randint(1000, 9999)
    
    # Create PDF file name
    pdf_file_name = f"sui_research_paper_{random_number}.pdf"
    
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
    "https://developers.diem.com/papers/diem-move-a-language-with-programmable-resources/2019-06-18.pdf",
    "https://arxiv.org/pdf/2110.05043",
    "https://arxiv.org/pdf/2205.05181",
    "https://arxiv.org/pdf/2004.05106",
    "https://arxiv.org/pdf/2110.08362",
    "https://research.facebook.com/file/168513165302305/The-Move-Prover.pdf",
    "https://ethz.ch/content/dam/ethz/special-interest/infk/chair-program-method/pm/documents/Education/Theses/Constantin_M%C3%BCller_MS_Report.pdf",
    "https://research.facebook.com/file/1070966526770512/Exact-and-Linear-Time-Gas-Cost-Analysis.pdf",
    ]

delete_files_and_folders("./ava/ava_backend/resources/pdfs")

for url in list(set(urls)):
    download_pdf(url, f"./ava/ava_backend/resources/pdfs/{generate_random_sui_research_pdf()}")
