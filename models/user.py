from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from config import AWS_S3_DOMAIN, S3_BUCKET

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    hashed_password = pw.CharField(unique=False, null=False)
    description = pw.CharField(unique=False, null=True)
    profile_photo_path = pw.CharField(unique=False, null=True)
    
    @hybrid_property
    def profile_image_url(self):
        return f"{AWS_S3_DOMAIN}/{S3_BUCKET}/{self.profile_photo_path}"

