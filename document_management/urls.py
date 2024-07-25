# company_intranet/documents/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/update/', views.document_update, name='document_update'),
]