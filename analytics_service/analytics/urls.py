from django.urls import path
from .views import AverageResponseTimeView, ErrorPercentageView

urlpatterns = [
    path('analytics/average-response/', AverageResponseTimeView.as_view(), name='average-response'),
    path('analytics/error-percentage/', ErrorPercentageView.as_view(), name='error-percentage'),
]