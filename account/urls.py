from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('signup/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
 ]

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
