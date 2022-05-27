import os
from flask import (
    current_app as app,
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
    session,
    Response,
)
from werkzeug.utils import secure_filename
from adiutor import (
    s3,
    BUCKET_NAME,
)
from .utils import (
    process_incoming_file,
    format_is_valid,
)

"""
Maps URL paths to their corresponding handlers.
"""


@app.route("/")
def home():
    """
    Renders the dashboard page.
    """

    return render_template("home.html")


@app.route("/about")
def about():
    """
    Renders the 'about' page.
    """

    return render_template("about.html")


@app.route("/author")
def author():
    """
    Renders the page with author info.
    """

    return render_template("author.html")


@app.route("/favicon.ico")
def favicon():
    """
    Serves the favicon.ico file.
    """

    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(404)
def page_not_found(e):
    """
    Renders custom 'Not found' if any route
    throws response with the 404 status code.
    """

    return render_template("404.html"), 404


@app.route("/something_went_wrong")
def something_went_wrong():
    """
    Renders error page if anyting went wrong when working on Celery task.
    """

    return render_template("something_went_wrong.html")


@app.route("/work_in_progress")
def work_in_progress():
    """
    Renders loading animation page.
    """

    return render_template("work_in_progress.html")


@app.route("/upload_file", methods=['POST'])
def upload_file():
    """
    Uploads given file to the server.
    """

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and format_is_valid(file.filename):
        filename = secure_filename(file.filename)
#        path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#        file.save(path_to_file)

        file_object = s3.Object(BUCKET_NAME, filename)
        file_object.put(Body=file)

        task = process_incoming_file.delay(path_to_file=filename)
        session['task_id'] = task.id
        # redirect path is set on the template:
        # {{ dropzone.config(redirect_url=url_for('work_in_progress')) }}

    return redirect(request.url)


@app.route("/done")
def done():
    """
    Renders success page.
    """

    return render_template("done.html")


@app.route("/is_the_task_ready/<task_id>")
def is_the_task_ready(task_id):
    """
    Handles AJAX polling request: checks if specified Celery task is done.
    If it is, instructs frontend to redirect to success page.
    """

    task = process_incoming_file.AsyncResult(task_id)

    if task.ready():
        response = Response()
        response.headers['HX-Redirect'] = url_for('done')
        return response
    else:
        return 'Not yet...'


@app.route("/download/<filename>")
def download(filename):
    """
    Serves the generated marking file.
    """

    s3.Bucket(BUCKET_NAME).download_file(
        filename,
        f'tmp/{filename}',
    )

    del session['task_id']

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True,
    )
