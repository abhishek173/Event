from django.urls import path,include
from .views import RegisterView,LoginView,PrivateEventViewSet,PublicEventViewSet,BookViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('private/event',PrivateEventViewSet,basename='private-event')
router.register('public/event',PublicEventViewSet,basename='public-event')
router.register('booking',BookViewSet,basename='booking')

urlpatterns = [
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path('',include(router.urls))
]
