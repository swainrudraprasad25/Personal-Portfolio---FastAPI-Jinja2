from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Portfolio, base

base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(
    req: Request,
    status: str = None,
):
    theme = req.cookies.get("theme", "light")
    return templates.TemplateResponse(
        req, "index.html", {"theme": theme, "status": status}
    )


@app.get("/set-theme/{theme}")
async def set_theme(theme: str):
    if theme not in ("light", "dark"):
        theme = "light"
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        "theme", theme, max_age=60 * 60 * 24 * 30, httponly=True, samesite="lax"
    )
    return response


@app.post("/contact")
async def contact(
    name: str = Form(""),
    email: str = Form(""),
    message: str = Form(""),
    db: Session = Depends(get_db),
):
    name, email, message = name.strip(), email.strip(), message.strip()
    valid = (
        bool(name)
        and "@" in email
        and "." in email.split("@")[-1]
        and len(message) >= 10
    )
    if valid:
        port = Portfolio(name=name, email=email, message=message)
        db.add(port)
        db.commit()
    return RedirectResponse(
        f"/?status={'success' if valid else 'error'}#contact", status_code=303
    )
@app.get("/message",response_class=HTMLResponse)
def message(req:Request,db:Session = Depends(get_db)):
    result=db.query(Portfolio).order_by(Portfolio.id.desc()).all()
    theme=req.cookies.get("theme","light")
    return templates.TemplateResponse(
        req, "message.html", {"items": result, "theme": theme}
    )
    