from django.urls import path , include
from rest_framework.routers import DefaultRouter
from blog_app.views import CountryViewSet, UserViewSet, BlogViewSet ,RegisterView
from blog_app.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'countries' , CountryViewSet , basename='countries')
router.register(r'users', UserViewSet , basename='users')
router.register(r'blogs' , BlogViewSet , basename='blogs')


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh")

]

urlpatterns += router.urls