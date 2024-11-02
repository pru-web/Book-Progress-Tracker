from django.apps import AppConfig

class TrackerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'progress_tracker.tracker_app'  # Note the full path
