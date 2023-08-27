"""A FastAPI server to display and search information about Indian army tribunal judgements."""
import os
import shutil
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated

import dotenv
import uvicorn
from fastapi import FastAPI, Form
from fastapi import Request
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from cosine_search import load_chandigarh_df, FindSimilar
from gpt3_parsing import summarise

dotenv.load_dotenv()

chandigarh_df = load_chandigarh_df('chandigarh.csv')

app = FastAPI(
    title="Army Tribunals",
    version="0.0.1",
    contact={
        "name": "Laurence Cullen",
        "url": "https://www.linkedin.com/in/laurence-cullen/",
        "email": "laurencesimoncullen@gmail.com",
    },
    # servers=[
    #     {"url": "https://api.vanellus.tech"},
    # ]
)
# app.add_middleware(HTTPSRedirectMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve API landing page, not needed to be included in OpenAPI schema
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def similar_to_text(text: str):
    # Find other judgements with similar PDF text
    find_similar = FindSimilar(chandigarh_df)

    # Find the closest judgement to the given text
    similar = find_similar.find_closest(text, K=10)

    # For each similar judgement summarise the PDF text and add it to the dataframe using LegalTextParser,
    # do this in parallel then wait for all threads to complete
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(summarise, row['pdf_text']) for _, row in similar.iterrows()]
        for future, (i, row) in zip(futures, similar.iterrows()):
            # Save result into the similar dataframe
            similar.loc[i, 'summary'] = future.result()

    # Remove the 'embedding' and 'pdf_text' columns
    similar = similar.drop(columns=['embedding', 'pdf_text'])

    return similar


# Search for documents similar to a provided PDF
@app.post("/similar_cases_file", response_class=HTMLResponse)
async def create_file(request: Request, pdf: UploadFile):  # -> RedirectResponse:
    # Write to disk with a randomly generated filename
    filename = f"{uuid.uuid4()}.pdf"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

    # Extract the text from the PDF
    pdf_text = extract_text(filename)

    # Delete the file
    os.remove(filename)

    similar = similar_to_text(pdf_text)
    # return templates.TemplateResponse("results.html", similar.to_dict(orient='records'))
    return templates.TemplateResponse("results.html", context={
        'request': request,
        'results': similar.to_dict(orient='records')
    })


# Search for documents with a similar embedding to the embedding of passed in plain text search query
@app.post("/similar_cases_text", response_class=HTMLResponse)
async def cases_similar_to_text(request: Request, text: Annotated[str, Form()]):  # -> RedirectResponse:
    similar = similar_to_text(text)

    # return templates.TemplateResponse("results.html", similar.to_dict(orient='records'))
    return templates.TemplateResponse("results.html", context={
        'request': request,
        'results': similar.to_dict(orient='records')
    })


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
