from fastapi import APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session
from app import model, schemas
from app.utils.auth import get_current_user, oauth2_scheme
from app.database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post('/')
def post_note(note: schemas.Post, current_user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    new_post=model.Posts (
        content=note.note,
        owner_id=current_user["id"]
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/")
def get_all_notes(current_user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    notes=db.query(model.Posts).filter(model.Posts.owner_id == current_user["id"]).all()
    return notes

@router.get("/{id}")
def get_note(id:int, current_user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    notes = db.query(model.Posts).filter(model.Posts.id==id).first()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note does not exist")
    if notes.owner_id != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this note")
    
    return notes

@router.put("/{id}")
def update_note(notes: schemas.Post ,id:int, current_user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    current_post=db.query(model.Posts).filter(model.Posts.id==id).first()
    
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    if current_post.owner_id != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this note")
    
    current_post.content = notes.note
    db.commit()
    db.refresh(current_post)
    return current_post

@router.delete("/{id}")
def delete_note(id:int,current_user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    post_to_delete = db.query(model.Posts).filter(model.Posts.id == id).first()
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    if post_to_delete.owner_id != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this note")
    db.delete(post_to_delete)
    db.commit()
    return {"message":"Post was deleted", "Post deleted":post_to_delete}
