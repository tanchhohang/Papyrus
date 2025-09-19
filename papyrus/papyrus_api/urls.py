from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [

]

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('books', views.BookViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('user-reviews', views.UserReviewViewSet, basename='user-reviews')
urlpatterns += router.urls