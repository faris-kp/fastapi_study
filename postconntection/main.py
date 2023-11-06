from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing  import List,Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choices_text : str
    is_correct : bool

class QustionBase(BaseModel):
    qustion_text : str
    choices : list[ChoiceBase]
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session,Depends(get_db)]


@app.post('/qustions/',tags=['qustions'])
async def create_qustions(question:QustionBase,db:db_dependency):
    db_question = models.Qustions(question_text=question.qustion_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text = choice.choices_text,is_correct=choice.is_correct,question_id = db_question.id)
        db.add(db_choice)
    db.commit()
    
@app.get('/qustions/{question_id}',tags=['Fetch'])
async def read_questions(question_id:int,db:db_dependency):
    result = db.query(models.Qustions).filter(models.Qustions.id == question_id ).first()
    if not result:
        raise HTTPException(status_code=404,detail="qustion does't exicst")
    return result
        
@app.get('/choices/{question_id}',tags=['Fetch'])
async def read_choices(question_id:int,db:db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404,detail="choices does't exicst")
    return result