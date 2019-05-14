from models.base_model import BaseModel
from models.user import User
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from config import AWS_S3_DOMAIN, S3_BUCKET

class Image(BaseModel, UserMixin):
    # name = pw.CharField(unique=False, null=True)
    user = pw.ForeignKeyField(User, backref='images')
    file_path = pw.CharField(unique=False, null=True)
    @hybrid_property
    def url(self):
         return f"{AWS_S3_DOMAIN}/{S3_BUCKET}/{self.file_path}"
    
 

