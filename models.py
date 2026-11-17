from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

base = declarative_base()

class Portfolio(base):
    __tablename__ = "port"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    message = Column(String(200))

class Skill(base):
    __tablename__ = "skills"
    id = Column(Integer, autoincrement=True, primary_key=True)
    category = Column(String(100), nullable=False)
    skills = Column(String(200), nullable=False)

class Experience(base):
    __tablename__ = "experiences"
    id = Column(Integer, autoincrement=True, primary_key=True)
    period = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)

class Project(base):
    __tablename__ = "projects"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    technologies = Column(String(200), nullable=False)
    github_url = Column(String(300))
