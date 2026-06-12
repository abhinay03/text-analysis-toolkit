import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from text_analysis_toolkit import TextAnalyzer, Tokenizer

app = FastAPI(title="Text Analysis Toolkit")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/documentation", response_class=HTMLResponse)
async def documentation(request: Request):
    return templates.TemplateResponse(request, "documentation.html", {"request": request})


@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    return templates.TemplateResponse(request, "demo.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {"request": request})


@app.post("/api/analyze")
async def analyze(
    text: str = Form(...),
    remove_stopwords: bool = Form(False),
    ngram_min: int = Form(2),
    ngram_max: int = Form(3),
):
    try:
        ta = TextAnalyzer(
            remove_stopwords=remove_stopwords,
            ngram_range=(ngram_min, ngram_max),
        )
        result = ta.analyze(text)

        tk = Tokenizer(lower=True, remove_punct=True, remove_stopwords=remove_stopwords)
        sentences = tk.sentence_split(text)

        response = {
            "success": True,
            "statistics": result["statistics"],
            "frequencies": {
                "top_words": [
                    {"word": w, "count": c}
                    for w, c in result["frequencies"]["top_words"]
                ],
                "unique_words": result["frequencies"]["unique_words"],
            },
            "sentiment": result["sentiment"],
            "ngrams": {
                n: [{"ngram": g, "count": c} for g, c in items]
                for n, items in result["ngrams"].items()
            },
            "tokens": result["tokens"],
            "sentences": sentences,
            "text_report": ta.report_text(result),
        }
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
