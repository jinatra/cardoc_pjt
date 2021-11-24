from django.urls import path

from vehicles.views import TireView

urlpatterns = [
    path('/tires', TireView.as_view()),
]