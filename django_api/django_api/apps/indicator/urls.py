from django.conf.urls import url

from .views import (
    PDReportsAPIView,
    IndicatorListCreateAPIView,
)


urlpatterns = [
    url(r'^programme-document/details/(?P<pd_id>\d+)/reports/', PDReportsAPIView.as_view(), name="programme-document-reports"),
    # below url (r'^') have to be last - he will override all others reports !!!
    url(r'^', IndicatorListCreateAPIView.as_view(), name='indicator-list-create-api'),
]
