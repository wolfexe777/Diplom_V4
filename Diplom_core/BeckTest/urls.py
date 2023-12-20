from django.urls import path
from .views import test, signup, user_login, user_logout, view_results, offer_save_result, registration_or_login, enter_email

urlpatterns = [
    path('test', test, name='test'),
    path('test_results/', test, name='test_results'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('view_results/', view_results, name='view_results'),
    path('offer_save_result/', offer_save_result, name='offer_save_result'),
    path('registration_or_login/', registration_or_login, name='registration_or_login'),
    path('enter_email/', enter_email, name='enter_email'),
]