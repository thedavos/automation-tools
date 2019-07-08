import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
