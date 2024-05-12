import requests, random

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


# Usage:
urls: list[str] = [
    "https://www.pdfdrive.com/download.pdf?id=34820119&h=090b23accd028f9055097590e71bd947&u=cache&ext=pdf",
    ]

for url in urls:
    download_pdf(url, f"./ava/resources/{generate_random_home_automation_pdf()}")
