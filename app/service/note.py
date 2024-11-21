from typing import List

from app.model.note import Note
from app.repository.note import NoteRepository

from app.schema import NoteInput, NoteType


class NoteService:
    @staticmethod
    async def add_note(note_input: NoteInput) -> NoteType:
        note = Note()
        note.name = note_input.name
        note.description = note_input.description

        await NoteRepository.create(note)

        return NoteType(id=note.id, name=note.name, description=note.description)

    @staticmethod
    async def get_all_note() -> List[NoteType]:
        list_note = await NoteRepository.get_all()
        return [
            NoteType(id=note.id, name=note.name, description=note.description)
            for note in list_note
        ]
