from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Experience, Portfolio, Project, Skill, base

base.metadata.create_all(bind=engine)


# ----------------- DATA LISTS -----------------
skills_data = [
    Skill(category="Languages", skills="Python, SQL, HTML, CSS"),
    Skill(
        category="Frameworks & Libraries",
        skills="FastAPI, Jinja2, Pydantic, Requests, mysql-connector-python",
    ),
    Skill(category="Database", skills="MySQL"),
    Skill(
        category="Tools",
        skills="Git, GitHub, VS Code, MySQL Workbench, Uvicorn",
    ),
]

experiences_data = [
    Experience(
        period="May 2024 - June 2024",
        title="Research Intern - DRDO, Chandipur",
        description="Worked with telemetry systems for data collection and monitoring during test-range operations, supporting real-time analysis and operational safety.",
    ),
    Experience(
        period="Feb 2022 - Mar 2022",
        title="IoT & Embedded Systems Intern - Coincent",
        description="Engineered and deployed embedded-system solutions for industrial automation applications.",
    ),
    Experience(
        period="2021 - 2025",
        title="B.Tech, Electronics & Telecommunication",
        description="Veer Surendra Sai University of Technology (VSSUT), Odisha. CGPA: 7.82",
    ),
    Experience(
        period="2018 - 2020",
        title="Intermediate (PCMB)",
        description="Royal Higher Secondary School of Science and Technology. 87.16%",
    ),
    Experience(
        period="2018",
        title="Matriculation",
        description="Madanpur Mohabir Nodal High School. 92%",
    ),
]

projects_data = [
    Project(
        title="Expense Tracker Web App",
        description="Full-stack app using FastAPI and Jinja2 templates with MySQL storage.\nCategory search, date-range filtering, and total/highest expense queries using parameterized SQL.",
        technologies="Python, FastAPI, MySQL, Jinja2, HTML, CSS",
        github_url="https://github.com/swainrudraprasad25/expense-tracker-fastapi.git",
    ),
    Project(
        title="Student Task Manager",
        description="REST API built with FastAPI and MySQL Connector for creating, retrieving, updating, and deleting tasks.\nCRUD endpoints with parameterized queries for secure data handling.",
        technologies="Python, FastAPI, MySQL",
        github_url="https://github.com/swainrudraprasad25/student_task_manager.git",
    ),
    Project(
        title="Weather Forecasting App",
        description="Fetches real-time weather data from WeatherAPI for any city entered in an HTML form.\nStores every search in MySQL and exposes a search-history endpoint.",
        technologies="Python, FastAPI, MySQL, REST API, HTML",
        github_url="https://github.com/swainrudraprasad25/Weather-Forecasting-App-FastAPI-WeatherAPI-MySQL-.git",
    ),
]


def seed_initial_data():
    db = next(get_db())
    try:
        if db.query(Skill).count() == 0:
            db.add_all(skills_data)

        if db.query(Experience).count() == 0:
            db.add_all(experiences_data)

        if db.query(Project).count() == 0:
            db.add_all(projects_data)

        db.commit()
    finally:
        db.close()


seed_initial_data()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(
    req: Request,
    status: str = None,
    db: Session = Depends(get_db),
):
    theme = req.cookies.get("theme", "light")
    skills = db.query(Skill).all()
    experiences = db.query(Experience).all()
    projects = db.query(Project).all()
    return templates.TemplateResponse(
        req,
        "index.html",
        {
            "theme": theme,
            "status": status,
            "skills": skills,
            "experiences": experiences,
            "projects": projects,
        },
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


@app.get("/message", response_class=HTMLResponse)
def message(req: Request, db: Session = Depends(get_db)):
    result = db.query(Portfolio).order_by(Portfolio.id.desc()).all()
    theme = req.cookies.get("theme", "light")
    return templates.TemplateResponse(
        req, "message.html", {"items": result, "theme": theme}
    )
