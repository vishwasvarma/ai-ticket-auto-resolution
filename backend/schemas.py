from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class TicketCreateSchema(BaseModel):
    title: str
    description: str