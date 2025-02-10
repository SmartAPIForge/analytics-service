from django.views import View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import timezone
from .models import Service, RequestData
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncHour


class BaseAnalyticsView(View):
    def validate_dates(self, start_str, end_str):
        try:
            return parse_datetime(start_str), parse_datetime(end_str)
        except (ValueError, TypeError):
            return None, None


class AverageResponseTimeView(BaseAnalyticsView):
    def get(self, request):
        service_name = request.GET.get('service')
        start_str = request.GET.get('start')
        end_str = request.GET.get('end')

        if not all([service_name, start_str, end_str]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        service = get_object_or_404(Service, name=service_name)
        start_utc, end_utc = self.validate_dates(start_str, end_str)

        if not start_utc or not end_utc:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        queryset = RequestData.objects.filter(
            service=service,
            timestamp__range=(start_utc, end_utc),
            response_time__isnull=False
        )

        hourly_stats = queryset.annotate(
            hour=TruncHour('timestamp', tzinfo=timezone.utc)
        ).values('hour').annotate(
            average_response_time=Avg('response_time')
        ).order_by('hour')

        result = [{
            'hour': stat['hour'].isoformat(),
            'average_response_time': round(stat['average_response_time'], 3)
        } for stat in hourly_stats]

        return JsonResponse({
            'service': service_name,
            'data': result
        })


class ErrorPercentageView(BaseAnalyticsView):
    def get(self, request):
        service_name = request.GET.get('service')
        start_str = request.GET.get('start')
        end_str = request.GET.get('end')

        if not all([service_name, start_str, end_str]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        service = get_object_or_404(Service, name=service_name)
        start_utc, end_utc = self.validate_dates(start_str, end_str)

        if not start_utc or not end_utc:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        queryset = RequestData.objects.filter(
            service=service,
            timestamp__range=(start_utc, end_utc)
        )

        hourly_stats = queryset.annotate(
            hour=TruncHour('timestamp', tzinfo=timezone.utc)
        ).values('hour').annotate(
            total_requests=Count('id'),
            failed_requests=Count('id', filter=Q(success=False))
        ).order_by('hour')

        result = []
        for stat in hourly_stats:
            total = stat['total_requests']
            failed = stat['failed_requests']
            percentage = round((failed / total * 100), 2) if total > 0 else 0.0

            result.append({
                'hour': stat['hour'].isoformat(),
                'error_percentage': percentage
            })

        return JsonResponse({
            'service': service_name,
            'data': result
        })