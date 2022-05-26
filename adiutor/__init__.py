import os
import dotenv
from flask import Flask
from adiutor.celery_init import make_celery
from flask_dropzone import Dropzone


"""
Initializes web application instance and Celery instance.
"""

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = f"{os.getcwd()}/adiutor/static/uploads"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CELERY_BROKER_URL"] = os.getenv("REDIS_URL")
app.config["CELERY_RESULT_BACKEND"] = os.getenv("REDIS_URL")
app.config["DROPZONE_DEFAULT_MESSAGE"] = """

Drop your file in here. It may be a set of electrical items 
in a .txt, .csv, .json or .yaml file.
Alternatively, you can use initial .pdf file as an input.

"""

celery = make_celery(app)

dropzone = Dropzone(app)

app.app_context().push()

# To dodge circular import issues this has to be imported
# after app instance is initialized
if True:
    from adiutor import routes
