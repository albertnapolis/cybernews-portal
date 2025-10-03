from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import Source
from app.models.database import get_db
from app.schemas import Source as SourceSchema, SourceCreate

router = APIRouter()

@router.get("/", response_model=List[SourceSchema])
def get_sources(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all news sources"""
    query = db.query(Source)
    if active_only:
        query = query.filter(Source.is_active == 1)
    sources = query.offset(skip).limit(limit).all()
    return sources

@router.get("/{source_id}", response_model=SourceSchema)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get a specific source by ID"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@router.post("/", response_model=SourceSchema)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """Create a new source"""
    # Check if source already exists
    existing = db.query(Source).filter(Source.feed_url == source.feed_url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source with this feed URL already exists")

    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.put("/{source_id}/toggle")
def toggle_source_status(source_id: int, db: Session = Depends(get_db)):
    """Toggle source active status"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source.is_active = 1 if source.is_active == 0 else 0
    db.commit()
    return {"message": f"Source {'activated' if source.is_active else 'deactivated'}"}