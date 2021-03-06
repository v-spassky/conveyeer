import os
import dotenv
import boto3
from flask import Flask
from adiutor.celery_init import make_celery
from flask_dropzone import Dropzone


"""
Initializes web application instance and Celery instance.
"""

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = f"{os.getcwd()}/tmp"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CELERY_BROKER_URL"] = os.getenv("REDIS_URL")
app.config["CELERY_RESULT_BACKEND"] = os.getenv("REDIS_URL")
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pdf, .txt, .csv, .json, .yaml'
app.config["DROPZONE_DEFAULT_MESSAGE"] = """

Drop your file in here. It may be a set of electrical items 
in a .txt, .csv, .json or .yaml file.
Alternatively, you can use initial .pdf file as an input.

"""

celery = make_celery(app)

aws_session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
s3 = aws_session.resource('s3')
BUCKET_NAME = os.getenv("BUCKET_NAME")

dropzone = Dropzone(app)

app.app_context().push()

# To dodge circular import issues this has to be imported
# after app instance is initialized
if True:
    from adiutor import routes
