import languagemodels as lm
from fastapi import FastAPI, UploadFile, File
app = FastAPI()

def search_wikipedia():
    import wikipedia as wk
    wk.set_lang("pt")
    documents = []
    for i in ["Python", "Fortran", "Java", "Cobol", "Javascript", "C", "R" ]:
        k = f"{i} (linguagem de programação)"
        summary, page = wk.summary(k, sentences=3), wk.page(k)
        dip = { "key": i, "title": page.title, "summary": summary, "url": page.url, "content": page.content }
        documents.append(dip)
    
    return documents


def to_english( ptg: str): 
    return lm.do(f"Translate to English the sentence: {ptg.capitalize()}") if ptg else "-"

@app.get("/")
async def read_root():
    return {"message": "hello"}


@app.get("/translate")
async def read_root( msg: str):
    return {"portuguese": msg, "english": to_english(msg)}


@app.get("/answer")
async def read_root( msg: str):
    docs = search_wikipedia()
    for i in docs:
        lm.store_doc(i.summary, i.key)

    msg_english = to_english(msg)
    answer = lm.get_doc_context(msg) 
    return {"portuguese": msg, "english": msg_english, "answer": answer, "docs": docs }


@app.get("/time")
async def read_root( question: str = None):
    question_english = to_english(question) if question else "Good Morning or Good Night? I have no more questions!"
    output = lm.chat(f'''
                System: Respond as a helpful assistant. Your response should take into account the date and time, which is {lm.get_date()}.

                User: {question_english}

                Assistant:
             ''')
    return {"english": question_english , "assistant": output }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
