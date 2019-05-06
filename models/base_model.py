import os
import peewee as pw
import datetime
from database import db



class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    # def validate(self):
    #     print(
    #         f"Warning validation method not implemented for {str(type(self))}")
    #     return True

    def validate(self):
        from models.user import User
        duplicate_username = User.get_or_none(User.username == self.username)
        if duplicate_username:
            self.errors.append('Username already taken. Pick another username!')

        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_email:
            self.errors.append('Email already registered. Use a different email!')

    # user.User.create(email="email@example.com", password="123456", username="ironrock")
    
    class Meta:
        database = db
        legacy_table_names = False
