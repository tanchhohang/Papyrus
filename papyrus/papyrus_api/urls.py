from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('users/', views.UserListAPIView.as_view()),
    # path('users/create', views.create_user),
    # path('users/<int:user_id>',views.UserDetailAPIView.as_view()),
    # path('books/info',views.BookInfoAPIView.as_view()),
]

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('books', views.BookViewSet)
router.register('reviews', views.ReviewViewSet)
urlpatterns += router.urls