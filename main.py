import streamlit as st
from PIL import Image
import fitz 
import os
import io
import cv2
import numpy as np
import pytesseract

def extract_text_from_image(image):
    img_array = np.array(image)
    if len(img_array.shape) == 2:
        img_gray = img_array
    else:
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY) 
    threshold_value = 200
    _, mask = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_and(img_gray, mask)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(pdf_file):
    with st.spinner("Extracting text from PDF..."):
        temp_pdf_path = "temp.pdf"
        with open(temp_pdf_path, "wb") as temp_pdf:
            temp_pdf.write(pdf_file.read())
        doc = fitz.open(temp_pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
    os.remove(temp_pdf_path)
    return text

def main():
    st.title("Online Text Exractor")


    uploaded_file = st.file_uploader("Choose a file to upload", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        if uploaded_file.type.startswith('image'):
            image = Image.open(uploaded_file)
            print(type(image))
            st.image(image, caption="Uploaded Image", use_column_width=True)
            text = extract_text_from_image(image)
        elif uploaded_file.type == 'application/pdf':
            text = extract_text_from_pdf(uploaded_file)
        else:
            st.warning("Unsupported file type. Please upload an image or PDF.")
            return

        if st.button("Extract Text"):
            st.subheader("Extracted Text:")
            st.text(text)

if __name__ == "__main__":
    main()
