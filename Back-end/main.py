from fastapi import FastAPI, UploadFile, File, Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, pipeline
from whisper import transcribe
from textblob import TextBlob
from typing import List
from pytube import YouTube
import speech_recognition as sr
import youtube_dl 
import pafy
import uvicorn
import whisper
import io
import subprocess
import os
import cv2
import pytesseract
import PyPDF2
import docx
import textract

app = FastAPI()
model = whisper.load_model("base")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"hello": "world!"}


@app.get("/welcome")
def get_name(name: str):
    return {"Welcome to my page": f'{name}'}


@app.get("/output")
def predict(summary: str):
    words = summary.split()
    sum = " "
    for i in range(0, len(words), 500):
        word_subset = ' '.join(words[i:i+500])
        
        tokenizer = AutoTokenizer.from_pretrained("Newsletter_summ/tokenizer")
        gen_kwargs = {"length_penalty": 2.0, "num_beams": 4, "max_length": 142}
        pipe = pipeline("summarization",model="Newsletter_summ/checkpoint", tokenizer=tokenizer)
        sum_text = pipe(word_subset, **gen_kwargs)[0]["summary_text"]
        sum = sum + sum_text
        
    original_text_sentiment = TextBlob(summary).sentiment.polarity
    generated_summary_sentiment = TextBlob(sum).sentiment.polarity
    print(sum_text)
    return {
        "Output Text": f'{sum_text}',
        "Original Text Sentiment" : {original_text_sentiment},
        "Generated Summary Sentiment" : {generated_summary_sentiment}
            }


@app.get("/dialogue")
def predict(summary: str):
    words = summary.split()
    word_subsets = []
    sum = " "
    for i in range(0, len(words), 300):
        word_subset = ' '.join(words[i:i+300])
        
        tokenizer = AutoTokenizer.from_pretrained("Dialogue_summ/tokenizer")
        gen_kwargs = {"length_penalty": 2.0, "num_beams": 4, "max_length": 142}
        pipe = pipeline("summarization", model="Dialogue_summ/checkpoint", tokenizer=tokenizer)
        sum_text = pipe(word_subset, **gen_kwargs)[0]["summary_text"]
        sum = sum + sum_text
    
    original_text_sentiment = TextBlob(summary).sentiment.polarity
    generated_summary_sentiment = TextBlob(sum).sentiment.polarity
    print(sum)
    return {
        "Output Text": f'{sum}',    
        "Original Text Sentiment" : {original_text_sentiment},
        "Generated Summary Sentiment" : {generated_summary_sentiment}
           }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not (file.content_type.startswith("audio/") or file.content_type.startswith("video/")):
        raise HTTPException(
            status_code=400, detail="File must be an audio file.")
   
    try:
        filename = file.filename
        with open(filename, "wb") as f:
            f.write(await file.read())
        result = model.transcribe(filename)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to transcribe audio.")
    print(result['text'])
    return result


@app.post("/video")
async def video_file(file: UploadFile = File(...)):
    # Check if the file is an audio file
    if not file.content_type.startswith("video/mp4"):
        raise HTTPException(
            status_code=400, detail="File must be an video file.")

    try:
        # Get the filename of the uploaded file
        filename = file.filename
        print("filename : ", filename)
        # Create a file object with the uploaded file
        with open(filename, "wb") as f:
            f.write(await file.read())

        # Transcribe the audio
        result = model.transcribe(filename)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to transcribe audio.")
    print(result['text'])
    return result


@app.get('/youtubeurl')
async def downloader(link: str):
    try:
        
        yt = YouTube(link)
        video = yt.streams.get_highest_resolution()
        title = yt.title
        filename = title + ".mp4"
        download_path = os.path.join("video", filename)
        video.download("video", filename=filename)
        text = model.transcribe(download_path)
    
    except KeyError as e:
        return {'error': f'Failed to retrieve streaming information: {str(e)}'}

    return {'text' : text}

@app.post('/image')
async def img_to_txt(file: UploadFile = File(...)):

    filename = file.filename
    with open(filename, "wb") as f:
        f.write(await file.read())
    img_cv = cv2.imread(filename)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    result = pytesseract.image_to_string(img_rgb).replace('\n','')
    print(result)
    return {'text': result}


@app.post('/uploadpdf')
async def pdftext(file: UploadFile = File(...)):
    
    filename = file.filename
    print("filename : ", filename)
    
    with open(filename, "wb") as f:
        f.write(await file.read())
    
    file_extension = filename.split(".")[-1]
    
    if file_extension == "pdf":
        with open(filename, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for i in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[i].extract_text()
        

    elif file_extension == "docx":
        with open(filename, 'rb') as f:
            doc = docx.Document(f)
            text = "\n".join([para.text for para in doc.paragraphs])
           
    else:
        with open(filename, 'rb') as f:
            text = textract.process(f).decode("utf-8")
   
    txt =""
    txt = text.replace('\n','')
    return {'text' : txt}

# @app.get('/youtubeurl')
# async def downloader(link: str):
#     video = pafy.new(link)
#     title = video.title
#     filename = title + ".mp4"
#     download_path = os.path.join("video", filename)
#     best = video.getbest()
#     best.download(filepath=download_path)
#     text = model.transcribe(download_path)
#     return {'text' : text}
# if __name__ == '__main__':
#     uvicorn.run(app, port=8081, host='0.0.0.0')

# uvicorn main:app --port 8081  --reload
