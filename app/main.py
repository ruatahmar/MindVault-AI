from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import model
from . import schemas
from app.utils.password_hash import hash_pwd, verify_pwd
from app.utils.jwt import create_JWT
from app.utils.auth import get_current_user, oauth2_scheme

#this basically creates all the tables that are imported in this file 
model.Base.metadata.create_all(bind=engine) 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MindVault API is working"}

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    hashed_pw = hash_pwd(user.password)
    created_user = model.User(username=user.username, email=user.email, password=hashed_pw)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return {"new user added": {
    "id": created_user.id,
    "username": created_user.username,
    "email": created_user.email
}}

@app.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = user.username
    user_exists = db.query(model.User).filter(model.User.email == email).first()
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")

    if not verify_pwd(user.password, user_exists.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")    
    access_token = create_JWT({"id":user_exists.id})
    return {"access_token" : access_token, "token_type": "bearer"}




@app.post('/notes')
def post_note(note: schemas.Post, current_user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    new_post=model.Posts (
        content=note.note,
        owner_id=current_user["id"]
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/notes")
def get_all_notes(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    notes=db.query(model.Posts).all()
    return notes

@app.get("/notes/{id}")
def get_note(id:int, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    notes = db.query(model.Posts).filter(model.Posts.id==id).first()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note does not exist")
    return notes

@app.put("/notes/{id}")
def update_note(notes: schemas.Post ,id:int, current_user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    current_post=db.query(model.Posts).filter(model.Posts.id==id).first()
    
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    current_post.content = notes.note
    db.commit()
    db.refresh(current_post)
    return current_post

@app.delete("/notes/{id}")
def delete_note(id:int, token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    post_to_delete = db.query(model.Posts).filter(model.Posts.id == id).first()
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    db.delete(post_to_delete)
    db.commit()
    return {"message":"Post was deleted", "Post deleted":post_to_delete}