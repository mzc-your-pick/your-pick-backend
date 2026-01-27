from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from ..models.topic import Topic
from ..models.participant_image import ParticipantImage
from ..schemas.topic import TopicCreate, TopicUpdate, ParticipantImageCreate


class TopicService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, program_id: Optional[int] = None, episode: Optional[int] = None) -> List[Topic]:
        query = self.db.query(Topic).options(joinedload(Topic.participant_images))
        if program_id:
            query = query.filter(Topic.program_id == program_id)
        if episode:
            query = query.filter(Topic.episode == episode)
        return query.order_by(Topic.created_at.desc()).all()

    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        return self.db.query(Topic).options(
            joinedload(Topic.participant_images)
        ).filter(Topic.id == topic_id).first()

    def create(self, data: TopicCreate) -> Topic:
        topic = Topic(
            program_id=data.program_id,
            topic_title=data.topic_title,
            episode=data.episode,
            match_type=data.match_type,
            participants=data.participants,
            video_url=data.video_url,
            vote_type=data.vote_type,
            actual_result=data.actual_result
        )
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def update(self, topic_id: int, data: TopicUpdate) -> Optional[Topic]:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(topic, field, value)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def delete(self, topic_id: int) -> bool:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return False
        self.db.delete(topic)
        self.db.commit()
        return True

    def add_participant_image(self, data: ParticipantImageCreate) -> ParticipantImage:
        image = ParticipantImage(
            topic_id=data.topic_id,
            participant_name=data.participant_name,
            image_url=data.image_url
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
