#ignore
import os
import shutil

def move_file(src, dest):
    """ Move file from src to dest, creating directories if needed. """
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)

# Define file locations and their correct destinations
files_to_move = {
    # Root files
    'db.sqlite3': 'progress_tracker_project/db.sqlite3',
    'README.md': 'progress_tracker_project/README.md',
    'requirements.txt': 'progress_tracker_project/requirements.txt',

    # Progress tracker project files
    'progress_tracker/directory_structure.txt': 'progress_tracker_project/progress_tracker/directory_structure.txt',
    'progress_tracker/dir_structure.py': 'progress_tracker_project/progress_tracker/dir_structure.py',
    'progress_tracker/manage.py': 'progress_tracker_project/manage.py',
    'progress_tracker/progress_tracker.db': 'progress_tracker_project/db/progress_tracker.db',
    'progress_tracker/settings.py': 'progress_tracker_project/progress_tracker/settings.py',
    'progress_tracker/structure.txt': 'progress_tracker_project/progress_tracker/structure.txt',

    # DB folder and files
    'progress_tracker/db/database.py': 'progress_tracker_project/db/database.py',
    'progress_tracker/db/schema.sql': 'progress_tracker_project/db/schema.sql',
    'progress_tracker/db/seed_data.sql': 'progress_tracker_project/db/seed_data.sql',

    # progress_tracker directory inside the project
    'progress_tracker/progress_tracker/asgi.py': 'progress_tracker_project/progress_tracker/asgi.py',
    'progress_tracker/progress_tracker/settings.py': 'progress_tracker_project/progress_tracker/settings.py',
    'progress_tracker/progress_tracker/urls.py': 'progress_tracker_project/progress_tracker/urls.py',
    'progress_tracker/progress_tracker/wsgi.py': 'progress_tracker_project/progress_tracker/wsgi.py',
    'progress_tracker/progress_tracker/__init__.py': 'progress_tracker_project/progress_tracker/__init__.py',

    # Tracker app files
    'tracker_app/admin.py': 'progress_tracker_project/tracker_app/admin.py',
    'tracker_app/apps.py': 'progress_tracker_project/tracker_app/apps.py',
    'tracker_app/forms.py': 'progress_tracker_project/tracker_app/forms.py',
    'tracker_app/models.py': 'progress_tracker_project/tracker_app/models.py',
    'tracker_app/urls.py': 'progress_tracker_project/tracker_app/urls.py',
    'tracker_app/views.py': 'progress_tracker_project/tracker_app/views.py',
    'tracker_app/__init__.py': 'progress_tracker_project/tracker_app/__init__.py',

    # Migrations folder
    'tracker_app/migrations/': 'progress_tracker_project/tracker_app/migrations/',

    # Static and CSS files
    'tracker_app/static/css/': 'progress_tracker_project/tracker_app/static/css/',
    'tracker_app/css/': 'progress_tracker_project/tracker_app/static/css/',  # Combining all css into static folder

    # Templates
    'tracker_app/templates/': 'progress_tracker_project/tracker_app/templates/',

    # Duplicate/miscellaneous migrations, static, css, templates in the root should be moved to tracker_app
    'migrations/': 'progress_tracker_project/tracker_app/migrations/',
    'static/css/': 'progress_tracker_project/tracker_app/static/css/',
    'css/': 'progress_tracker_project/tracker_app/static/css/',
    'templates/': 'progress_tracker_project/tracker_app/templates/',
}

# Loop through the files and move them to the correct location
for src, dest in files_to_move.items():
    if os.path.exists(src):
        move_file(src, dest)
        print(f"Moved {src} to {dest}")
    else:
        print(f"File {src} not found!")

