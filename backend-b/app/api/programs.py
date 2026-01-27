from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.program import ProgramCreate, ProgramUpdate, ProgramResponse
from ..services.program_service import ProgramService

router = APIRouter()


@router.get("/programs", response_model=List[ProgramResponse], summary="프로그램 목록 조회")
async def get_programs(db: Session = Depends(get_db)):
    service = ProgramService(db)
    return service.get_all()


@router.get("/programs/{program_id}", response_model=ProgramResponse, summary="프로그램 상세 조회")
async def get_program(program_id: int, db: Session = Depends(get_db)):
    service = ProgramService(db)
    program = service.get_by_id(program_id)
    if not program:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    return program


@router.post("/programs", response_model=ProgramResponse, status_code=201, summary="프로그램 생성")
async def create_program(data: ProgramCreate, db: Session = Depends(get_db)):
    service = ProgramService(db)
    return service.create(data)


@router.patch("/programs/{program_id}", response_model=ProgramResponse, summary="프로그램 수정")
async def update_program(program_id: int, data: ProgramUpdate, db: Session = Depends(get_db)):
    service = ProgramService(db)
    program = service.update(program_id, data)
    if not program:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    return program


@router.delete("/programs/{program_id}", summary="프로그램 삭제")
async def delete_program(program_id: int, db: Session = Depends(get_db)):
    service = ProgramService(db)
    if not service.delete(program_id):
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")
    return {"success": True, "message": "프로그램이 삭제되었습니다"}
