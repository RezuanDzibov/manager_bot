from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.ProductViewSet, basename="product")

urlpatterns = [
    path("image/<str:code>/", views.ProductImageAddView.as_view(), name="product_image_add"),
    path("image/<int:pk>/", views.ProductImageRetrieve.as_view(), name="product_image"),
    path("commit_sold/<str:product_code>/", views.ProuductSoldView.as_view(), name="commit_sold"),
    path("", views.ProductCreateView.as_view(), name="product_add"),
]

urlpatterns += router.urls
