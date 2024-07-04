import cv2
import os
from tkinter import Tk, Label, Button, filedialog

# Function to check the Haar Cascade file existence
def check_haar_cascade(path):
    if os.path.exists(path):
        cascade = cv2.CascadeClassifier(path)
        if not cascade.empty():
            print(f"Haar Cascade loaded successfully from {path}")
            return cascade
        else:
            print(f"Error loading Haar Cascade from {path}")
            return None
    else:
        print(f"Haar Cascade file not found at {path}")
        return None

# Function to set the Haar Cascade path
def select_haar_cascade():
    cascade_path = filedialog.askopenfilename(title="Select Haar Cascade XML File", filetypes=[("XML files", "*.xml")])
    return cascade_path

# Prompt user to select Haar Cascade files
print("Select the Haar Cascade file for number plates.")
plate_cascade_path = select_haar_cascade()
plate_cascade = check_haar_cascade(plate_cascade_path)

print("Select the Haar Cascade file for faces.")
face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = check_haar_cascade(face_cascade_path)

if not plate_cascade or not face_cascade:
    print("Error: Unable to load one or more Haar Cascade files. Exiting...")
    exit()

def process_image(image_path, output_path, plate_cascade, face_cascade):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
        return
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect number plates
    plates = plate_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    print(f"Found {len(plates)} plates")

    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = image[y:y + h, x:x + w]
        blur = cv2.GaussianBlur(roi, (25, 25), 31)
        image[y:y + h, x:x + w] = blur

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    print(f"Found {len(faces)} faces")

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi = image[y:y + h, x:x + w]
        blur = cv2.GaussianBlur(roi, (25, 25), 31)
        image[y:y + h, x:x + w] = blur

    cv2.imwrite(output_path, image)

def process_images(input_dir, output_dir, plate_cascade, face_cascade):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"Processing image: {image_path}")
            process_image(image_path, output_path, plate_cascade, face_cascade)

def select_input_dir():
    input_dir = filedialog.askdirectory(title="Select Input Directory")
    input_label.config(text=f"Input Directory: {input_dir}")
    root.input_dir = input_dir

def select_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_label.config(text=f"Output Directory: {output_dir}")
    root.output_dir = output_dir

def start_processing():
    input_dir = getattr(root, 'input_dir', None)
    output_dir = getattr(root, 'output_dir', None)
    
    if not input_dir or not output_dir:
        print("Please select both input and output directories.")
        return

    process_images(input_dir, output_dir, plate_cascade, face_cascade)

# Tkinter setup
root = Tk()
root.title("Number Plate and Face Blurring")

input_label = Label(root, text="Input Directory: Not selected")
input_label.pack(pady=10)

input_button = Button(root, text="Select Input Directory", command=select_input_dir)
input_button.pack(pady=5)

output_label = Label(root, text="Output Directory: Not selected")
output_label.pack(pady=10)

output_button = Button(root, text="Select Output Directory", command=select_output_dir)
output_button.pack(pady=5)

start_button = Button(root, text="Start Processing", command=start_processing)
start_button.pack(pady=20)

root.mainloop()



