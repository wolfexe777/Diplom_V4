from django.urls import path
from .views import home, test, signup, user_login, user_logout, view_results, offer_save_result, enter_email, test_results
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_html_path = os.path.join(BASE_DIR, 'templates', 'base.html')

urlpatterns = [
    path('', home, name='home'),
    path('test/', test, name='test'),
    path('test_results/', test_results, name='test_results'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('view_results/', view_results, name='view_results'),
    path('offer_save_result/', offer_save_result, name='offer_save_result'),
    path('enter_email/', enter_email, name='enter_email'),
]