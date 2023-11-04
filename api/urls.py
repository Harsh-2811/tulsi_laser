# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplainViewSet, ComplainOutcomeByCustomerID, ComplainOutcomeViewSet, ComplainOutcomeByMchindID, UserLogin ,ChangePasswordView, SaveFCMToken
from django.urls import path

# Create a router and register our viewset with it.


router = DefaultRouter()
router.register(r'complains', ComplainViewSet)
router.register(r'complain-outcomes', ComplainOutcomeViewSet)
urlpatterns = [
    path("login/", UserLogin.as_view(), name='user-login'),
    path("changepassword/", ChangePasswordView.as_view(), name='change-password'),
    path('', include(router.urls)),
    path('complain-outcomes/<int:customer_id>/',
         ComplainOutcomeByCustomerID.as_view(), name='complain-outcomes-by-customer'),
    path('complain-outcomes/ByMachine/<int:machine_id>/',
         ComplainOutcomeByMchindID.as_view(), name='complain-outcomes-by-customer'),
    path("saveFCMToken/",SaveFCMToken.as_view(),name="saveFCMToken")

]
