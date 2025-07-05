import requests
import os

base_url = "https://files.iittp.ac.in/pdfs/syllabus/2022_NewCourses/EE/EE{}L.pdf"
download_folder = "IITTP_Syllabus_PDFs"

# Create the download folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Iterate through the range of numbers from 1 to 600
for i in range(311, 313):
    file_number = f"{i:03d}"  # Format the number with leading zeros to three digits (e.g., 001, 010, 100)
    url = base_url.format(file_number)
    filename = os.path.join(download_folder, f"EE{file_number}L.pdf")

    try:
        print(f"Trying to download: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(filename, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"Downloaded successfully: {filename}\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}\n")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}\n")

print("Download process finished!")