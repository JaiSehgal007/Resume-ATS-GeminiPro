from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #converting pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # converting to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encoding to base 64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")

st.set_page_config(page_title="ResumeScored")
st.header("ResumeScored")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


col1, col2, col3 = st.columns(3)
submit1 = col1.button("Know About the Resume")  
submit2 = col2.button("How can I improve my skills?")  
submit3 = col3.button("Get your Percentage Match")

input_prompt1 = """
As a seasoned Technical Human Resource Manager, your objective is to meticulously assess the submitted resume vis-à-vis the job description. 
Offer a comprehensive evaluation of whether the candidate's qualifications and experience align with the demands of the role. 
Emphasize both the strengths and weaknesses of the applicant, specifically in relation to the specified job requirements.
"""

input_prompt2 = """
You are a dedicated professional seeking to enhance your skill set and advance your career. Describe the specific skills or areas of expertise you aim to improve upon, 
and provide context regarding your current proficiency level and aspirations. Additionally, outline your preferred learning methods or resources, and any challenges you anticipate 
in the process of skill development. Your insights will assist in formulating personalized recommendations for skill enhancement.
"""

input_prompt3 = """
Imagine yourself as a proficient ATS (Applicant Tracking System) analyst equipped with an in-depth understanding of data science and ATS functionality. 
Your duty is to meticulously scrutinize the resume against the provided job description. First, present the percentage match indicating how well the resume aligns with the job description. 
Subsequently, highlight any keywords missing in the resume. Finally, provide your overall insights and reflections.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Here's what your resume says")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("You need to work on")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Here is ehat the experts suggest")
        st.write(response)
    else:
        st.write("Please upload the resume")


