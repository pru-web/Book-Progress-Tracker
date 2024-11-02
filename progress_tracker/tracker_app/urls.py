#URL routing specific to the tracker app, separating the concerns of the global urls.py
from django.urls import path
from progress_tracker.tracker_app import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('user_main/', views.user_main, name='user_main'),
    path('admin_main/', views.admin_main, name='admin_main'),
    path('admin_user_management/', views.admin_user_management_view, name='admin_user_management'),
    path('admin_book_management/', views.admin_book_management_view, name='admin_book_management'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('user_menu/<int:user_id>', views.user_menu, name='user_menu'),
    path('view_books/', views.view_books, name='view_books'),
    path('search_books/<int:user_id>/', views.search_books, name='search_books'),
    path("progress_tracker_page/<int:user_id>/", views.progress_tracker_page_view, name="progress_tracker_page"),
    path('user_profile/<int:user_id>/', views.user_profile_view, name='user_profile'),

]
