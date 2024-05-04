from pydantic import BaseModel


class StudentForClass(BaseModel):
    id: int
    name: str
    email: str
    present_n_times: int

    def __init__(self, id: int, name: str, email: str, present_n_times: int):
        super().__init__(id=id, name=name, email=email, present_n_times=present_n_times)
