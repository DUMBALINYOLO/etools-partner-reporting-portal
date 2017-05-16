from django.conf.urls import url

from .views import (
    PartnerDetailsAPIView,
)


urlpatterns = [
    url(r'^partner-details/$', PartnerDetailsAPIView.as_view(), name="partner-details"),
]
