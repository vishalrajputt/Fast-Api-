from fastapi import FastAPI, Request,Header,Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal,engine
import models

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_films = db.query(models.Film).count()
    if num_films==0:
        films = [
               {'name':'Blade runner','Director':'ridely scoot'},
               {'name':'Bahubali','Director':'ridely muppet'},
               {'name':'Batman','Director':'ridely croks'},
               {'name':'Blast','Director':'ridely manag'},
               {'name':'Blitz','Director':'ridely ophera'},
            ]
        for film in films :
            db.add(models.Film(**film))
        db.commit()
    else:
        print(f'{num_films} films already in database')
        db.close()
@app.get('/')
def root():
        return{'message':'Vishal'}

@app.get('/index/',response_class=HTMLResponse)

async def movielist(request: Request,
                    hx_request: str | None = Header(default=None),
                    db: Session = Depends(get_db)):
    
    films = db.query(models.Film).all()
    context = {'request':request,'films':films}

    if hx_request:
        return templates.TemplateResponse("table.html",context)
    return templates.TemplateResponse('index.html',context)

