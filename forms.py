from typing import List
from typing import Optional

from fastapi import Request


class ShowResultsForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.description = form.get("description")

    def is_valid(self):
        if not self.description or not len(self.description) >= 40:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False