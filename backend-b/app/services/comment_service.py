from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.comment import Comment
from ..schemas.comment import CommentCreate


class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_topic(self, topic_id: int) -> List[Comment]:
        return self.db.query(Comment).join(
            Comment.vote
        ).filter(
            Comment.vote.has(topic_id=topic_id)
        ).order_by(Comment.created_at.desc()).all()

    def create(self, vote_id: int, data: CommentCreate) -> Comment:
        comment = Comment(
            vote_id=vote_id,
            content=data.content,
            comment_user_name=data.comment_user_name,
            comment_password=data.comment_password
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment_id: int, password: str) -> Optional[str]:
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return "COMMENT_NOT_FOUND"
        if comment.comment_password != password:
            return "WRONG_PASSWORD"
        self.db.delete(comment)
        self.db.commit()
        return None
