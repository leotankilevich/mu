from app.model.note import Note
from app.core.db import get_session
from sqlmodel import select, update, delete


class NoteRepository:
    @staticmethod
    async def create(note_data: Note):
        async with get_session() as session:
            session.add(note_data)
            await session.commit()

    @staticmethod
    async def get_by_id(note_id: int) -> Note:
        async with get_session() as session:
            stmt = select(Note).where(Note.id == note_id)
            result = await session.execute(stmt)
            note = result.scalars().first()

            return note

    @staticmethod
    async def get_all():
        async with get_session() as session:
            query = select(Note)
            result = await session.execute(query)

            return result.scalars().all()
