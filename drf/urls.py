from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from article.views import PostListView, CreateOrUpdateRatingView
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view settings
schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
      description="API documentation for your project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token), # to get the token by providing username and password
    path('posts/', PostListView.as_view(), name='post-list'), # api that are related to get the posts
    path('rate/', CreateOrUpdateRatingView.as_view(), name='rate-post'), # api for rating a post,
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # swagger api
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # swagger api
]


