from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from events.orm import Event


class EventQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, event_id: UUID) -> Optional[Event]:
        """Get a single event by ID"""
        stmt = select(Event).where(and_(Event.id == event_id, Event.is_active == True))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Event]:
        """Get all active events with pagination"""
        stmt = (
            select(Event)
            .where(Event.is_active == True)
            .order_by(Event.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_total_count(self) -> int:
        """Get total count of active events"""
        stmt = select(func.count(Event.id)).where(Event.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def search_events(
        self, 
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 100, 
        offset: int = 0
    ) -> List[Event]:
        """Search events by name, description, or location"""
        stmt = select(Event).where(Event.is_active == True)
        
        if search_term:
            search_filter = or_(
                Event.name.ilike(f"%{search_term}%"),
                Event.description.ilike(f"%{search_term}%")
            )
            stmt = stmt.where(search_filter)
        
        if location:
            stmt = stmt.where(Event.location.ilike(f"%{location}%"))
        
        stmt = stmt.order_by(Event.created_at.desc()).limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_search_count(
        self, 
        search_term: Optional[str] = None,
        location: Optional[str] = None
    ) -> int:
        """Get count of search results"""
        stmt = select(func.count(Event.id)).where(Event.is_active == True)
        
        if search_term:
            search_filter = or_(
                Event.name.ilike(f"%{search_term}%"),
                Event.description.ilike(f"%{search_term}%")
            )
            stmt = stmt.where(search_filter)
        
        if location:
            stmt = stmt.where(Event.location.ilike(f"%{location}%"))
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0
