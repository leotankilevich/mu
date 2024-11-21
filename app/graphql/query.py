from typing import List

import strawberry

from app.service.note import NoteService
from app.schema import NoteType


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"

    @strawberry.field
    async def get_all_notes(self) -> List[NoteType]:
        return await NoteService.get_all_note()
