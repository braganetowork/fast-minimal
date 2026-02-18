import languagemodels as lm
from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello"}


@app.get("/translate")
async def read_root( msg: str):
    return {"portuguese": msg, "english": lm.do(f"Translate to English: {msg}")}


@app.get("/answer")
async def read_root( msg: str):
    lm.store_doc(lm.get_wiki("Python"), "Python")
    lm.store_doc(lm.get_wiki("Java"), "Java")
    lm.store_doc(lm.get_wiki("Cobol"), "Cobol")
    lm.store_doc(lm.get_wiki("Javascript"), "Javascript")
    lm.store_doc(lm.get_wiki("Pascal"), "Pascal")
    lm.store_doc(lm.get_wiki("Fortran"), "Fortran")
    lm.store_doc(lm.get_wiki("C language"), "C")
    lm.store_doc(lm.get_wiki("R language"), "R")
    msg_english = lm.do(f"Translate to English: {msg.capitalize()}")
    answer = lm.get_doc_context(msg_english)
    return {"portuguese": msg, "english": msg_english, "answer": (answer? str(answer) : "-") }


@app.get("/time")
async def read_root( question: str = None):
    question_english = lm.do(f"Translate to English: {question.capitalize()}") if question else "Good Morning or Good Night? I have no more questions!"
    output = lm.chat(f'''
                System: Respond as a helpful assistant. Your response should take into account the date and time, which is {lm.get_date()}.

                User: {question_english}

                Assistant:
             ''')
    return {"english": question_english , "assistant": output }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
