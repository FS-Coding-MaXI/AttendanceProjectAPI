from pydantic import BaseModel


class StudentBase(BaseModel):
    id: int
    name: str
    email: str


class StudentForClass(BaseModel):
    id: int
    name: str
    email: str
    present_n_times: int
