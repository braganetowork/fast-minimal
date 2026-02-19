import languagemodels as lm
from fastapi import FastAPI, UploadFile, File

def search_wikipedia():
    import wikipedia as wk
    wk.set_lang("pt")
    langs = ["Python", "Fortran", "Java (linguagem de programação)", "Cobol", "Javascript", "C (linguagem de programação)", "R (linguagem de programação)" ]
    return [{ "id": i, "summary": wk.summary(i, sentences=6), "url": wk.page(i).url } for i in langs]:
    

DOCUMENTS = search_wikipedia()
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello"}


def to_english( ptg: str): 
    return lm.do(f"Translate to English the sentence: {ptg.capitalize()}") if ptg else "-"


@app.get("/translate")
async def translate_root( msg: str):
    return {"portuguese": msg, "english": to_english(msg)}


@app.get("/answer")
async def answer_root( msg: str):
    # lm.get_wiki does not correct!
    # JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    # Alternative: lib wikipedia
    
    for i in DOCUMENTS:
        lm.store_doc(i['summary'], i['id'])

    answer = lm.get_doc_context(msg).split('\n\n')[0] 
    answer_key = answer.split('document:')[0].replace("From ", "").strip()
    answer_sum = [i for i in DOCUMENTS if answer_key[:12] in i['id']]
    answer_summary = answer_sum[0]['summary'] if len(answer_sum) > 0 else "-"
    return {"portuguese": msg, "answer": answer, "answer_summary": answer_summary ,"docs": DOCUMENTS }


@app.get("/time")
async def time_root( question: str = None):
    question_english = to_english(question) if question else "Good Morning or Good Night? I have no more questions!"
    output = lm.chat(f'''
                System: Respond as a helpful assistant. Your response should take into account the date and time, which is {lm.get_date()}.

                User: {question_english}

                Assistant:
             ''')
    return {"original": question, "english": question_english , "assistant": output }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
