from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="bloggHome"),
    path('bloggPost/<int:id>/',views.bloggPost, name="bloggPost"),
]

