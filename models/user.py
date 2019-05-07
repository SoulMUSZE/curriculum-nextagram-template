from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True, null=True)
    hashed_password = pw.CharField(unique=False, null=True)

