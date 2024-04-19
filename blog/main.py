from fastapi import FastAPI,Depends
from . import schema,model
from blog.configure import Base,engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(engine)
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@app.post('/blog')
def create(request:schema.Blog,db:Session=Depends(get_db)):
    new_blog = model.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@app.get('/blog/{id}')
def show(id,db:Session=Depends(get_db)):
    blogs = db.query(model.Blog).filter(model.Blog.id == id).first()
    return blogs
@app.put('/blog/{id}')
def update(id,request:schema.Blog,db:Session = Depends(get_db)):
    blogs = db.query(model.Blog).filter(model.Blog.id == id).update({"title":request.title,"body":request.body})
    db.commit()
    return "updated"
@app.delete('/blog/{id}')
def destruct(id,db:Session=Depends(get_db)):
    blogs=db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()


