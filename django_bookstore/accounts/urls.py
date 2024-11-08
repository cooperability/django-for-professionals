#this file is no longer being actively used by the project, but preserved for reference
from django.urls import path
from .views import SignupPageView

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
]
