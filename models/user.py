from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    hashed_password = pw.CharField(unique=False, null=False)

