# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplainViewSet, ComplainOutcomeByCustomerID
# from .views import get_complain_outcomes_by_customer_id
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
# Create a router and register our viewset with it.


router = DefaultRouter()
router.register(r'complains', ComplainViewSet)
urlpatterns = [
    path("login/", obtain_auth_token, name="obtain-auth-token"),
    path('', include(router.urls)),
    path('complain-outcomes/<int:customer_id>/',
         ComplainOutcomeByCustomerID.as_view(), name='complain-outcomes-by-customer'),
    path('complain-outcomes/create/', ComplainOutcomeByCustomerID.as_view(),
         name='complain-outcomes-create'),
]
