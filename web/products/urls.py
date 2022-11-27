from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

router = DefaultRouter()
router.register("", views.ProductViewSet, basename="product")

urlpatterns = [
    path("image/<int:pk>/", views.ProductImageRetrieve.as_view(), name="product_image"),
    path("commit_sold/<str:product_code>/", views.ProuductSoldView.as_view(), name="commit_sold")
]

urlpatterns += router.urls
