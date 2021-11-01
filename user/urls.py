from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user', views.UserRegisterViewSet, 'user_register')

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('activate_account/', views.CodeApiView.as_view(), name='activate_account'),
    path('', include(router.urls))
]
