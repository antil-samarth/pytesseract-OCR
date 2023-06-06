import cv2
import pytesseract
import os
import pdf2image

task_folder = 'Data'

with open('output.txt', 'w') as file:
    file.truncate(0)

def process_pdf(pdf_path):
    # PDF file to list of images.
    images = pdf2image.convert_from_path(pdf_path)

    t = ''
    for i, image in enumerate(images):
        # Save images to a temporary folder.
        image_path = f"Data/Task1/temp/{i}.jpg"
        image.save(image_path, 'JPEG')

        # Load image using OpenCV
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use Pytesseract to extract text from the image
        t += pytesseract.image_to_string(gray)
        
        # Delete the saved image.
        os.remove(image_path)
    return t 

def process_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Gaussian blur to denoise image
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)

    # Use Pytesseract to extract text from the image
    t = pytesseract.image_to_string(denoised)
    return t 
    
for file_name in os.listdir(task_folder):
    
    # Skip the temporary folder
    if file_name == 'temp':
        continue
    
    # Get the file path
    file_path = os.path.join(task_folder, file_name)
    file_path = file_path.replace('\\', '/')
    
    print(f"Processing {file_path}...")

    # Process the file
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        text = process_image(file_path)
    elif file_name.endswith('.pdf'):        
        text = process_pdf(file_path)
    else:
        continue

    # Write the output text to the file
    with open('output.txt', 'a') as f:
        f.write("File Name: " + file_name + "\n")
        f.write(text)
        f.write("\n\n")
    f.close()
    
    print(f"Processed File: " + file_name + "\n")
