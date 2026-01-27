from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.program import Program
from ..schemas.program import ProgramCreate, ProgramUpdate


class ProgramService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Program]:
        return self.db.query(Program).order_by(Program.created_at.desc()).all()

    def get_by_id(self, program_id: int) -> Optional[Program]:
        return self.db.query(Program).filter(Program.id == program_id).first()

    def create(self, data: ProgramCreate) -> Program:
        program = Program(
            title=data.title,
            description=data.description,
            status=data.status,
            image_url=data.image_url
        )
        self.db.add(program)
        self.db.commit()
        self.db.refresh(program)
        return program

    def update(self, program_id: int, data: ProgramUpdate) -> Optional[Program]:
        program = self.get_by_id(program_id)
        if not program:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(program, field, value)
        self.db.commit()
        self.db.refresh(program)
        return program

    def delete(self, program_id: int) -> bool:
        program = self.get_by_id(program_id)
        if not program:
            return False
        self.db.delete(program)
        self.db.commit()
        return True
