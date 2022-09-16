'''ROUTER FOR POST-RELATED PATH OPERATORS'''
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# return all posts in postgresql database
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 10, # limit the number of returned posts
    skip: int = 0, # to skip a number of messages from the beginning
    search: Optional[str] = "" # title search function
    ):

    # olver version - kept for reference
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # if you want to return posts only from the current user

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


# create new posts and store in the databse
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # /posts for best practice as per CRUD
def createposts(post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)): # checks user authentication

    # SCRIPT FOR QUERYING SQL DIRECTLY - NOT NEEDED IF USING SQLALCHEMY
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #     (
    #         post.title, post.content, post.published
    #     )
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# return a single post from postgresql
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post ID {id} was not found"
        )
    
    # check whether owner owns the requested post - turned off for now
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"not authorised to perform requested action"
    #     )

    return post



# delete post from postgresql
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = f"Post with id: {id} does not exist"
            )
    
    # check that a user can only delete own posts
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorised to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update existing post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *""",
    #  (
    #     post.title, post.content, post.published, (str(id))
    #     )
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = f"Post with {id} does not exist"
            )
    
    # check that a user can only update own posts
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorised to perform requested action"
        )


    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()