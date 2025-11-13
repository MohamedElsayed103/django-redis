from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.auth.models import User
from .tasks import process_large_dataset, generate_report
from .models import Product
import time


# LAB 4: Views to trigger background tasks

def trigger_dataset_processing(request):
    """
    Offload heavy dataset processing to background
    """
    size = int(request.GET.get('size', 100))
    
    # Offload to Celery - non-blocking
    task = process_large_dataset.delay(size)
    
    return JsonResponse({
        'message': 'Dataset processing started in background',
        'task_id': task.id,
        'status': 'Task queued successfully',
        'check_status_url': f'/task-status/{task.id}/'
    })


def trigger_report_generation(request):
    """
    Offload heavy report generation to background
    """
    report_type = request.GET.get('type', 'sales')
    user_id = request.GET.get('user_id', 1)
    
    # Offload to Celery - non-blocking
    task = generate_report.delay(report_type, user_id)
    
    return JsonResponse({
        'message': 'Report generation started in background',
        'task_id': task.id,
        'report_type': report_type,
        'status': 'Task queued successfully',
        'check_status_url': f'/task-status/{task.id}/'
    })


def check_task_status(request, task_id):
    """
    Check the status of a Celery task
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    response_data = {
        'task_id': task_id,
        'status': task.status,
        'ready': task.ready(),
    }
    
    if task.ready():
        if task.successful():
            response_data['result'] = task.result
        else:
            response_data['error'] = str(task.info)
    
    return JsonResponse(response_data)


# LAB 6: Caching Examples

def heavy_computation():
    """
    Simulates a heavy function that should be cached
    """
    time.sleep(3)
    result = sum([i ** 2 for i in range(10000)])
    return result


def cached_function_view(request):
    """
    LAB 6: Caching a specific heavy function
    """
    cache_key = 'heavy_computation_result'
    
    # Try to get from cache
    result = cache.get(cache_key)
    
    if result is None:
        # Cache miss - compute and store
        result = heavy_computation()
        cache.set(cache_key, result, 300)  # Cache for 5 minutes
        cache_status = 'MISS - Computed and cached'
    else:
        cache_status = 'HIT - Retrieved from cache'
    
    return JsonResponse({
        'result': result,
        'cache_status': cache_status,
        'message': 'Check Debug Toolbar for cache analysis'
    })


def cached_orm_query_view(request):
    """
    LAB 6: Caching heavy ORM queries
    """
    cache_key = 'all_products_with_high_price'
    
    # Try to get from cache
    products = cache.get(cache_key)
    
    if products is None:
        # Cache miss - query database
        time.sleep(2)  # Simulate slow query
        products = list(Product.objects.filter(price__gte=100).values('name', 'price', 'stock'))
        cache.set(cache_key, products, 600)  # Cache for 10 minutes
        cache_status = 'MISS - Queried database'
        db_hit = True
    else:
        cache_status = 'HIT - Retrieved from cache'
        db_hit = False
    
    return JsonResponse({
        'products': products,
        'count': len(products),
        'cache_status': cache_status,
        'db_queried': db_hit,
        'message': 'Check Debug Toolbar for query analysis'
    })


@cache_page(60 * 5)  # Cache entire view for 5 minutes
def cached_full_view(request):
    """
    LAB 6: Full view caching using decorator
    """
    # Simulate heavy processing
    time.sleep(2)
    
    data = {
        'message': 'This entire view is cached for 5 minutes',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'products_count': Product.objects.count(),
        'users_count': User.objects.count(),
        'cache_info': 'This response is cached. Refresh to see same timestamp for 5 minutes.'
    }
    
    return JsonResponse(data)


def template_fragment_view(request):
    """
    LAB 6: Template with fragment caching
    """
    # Get data for template
    products = Product.objects.all()[:10]
    
    context = {
        'products': products,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    return render(request, 'core/cached_template.html', context)


def clear_cache_view(request):
    """
    Utility view to clear all cache
    """
    cache.clear()
    return JsonResponse({
        'message': 'All cache cleared successfully',
        'status': 'success'
    })


def home(request):
    """
    Home page with links to all lab endpoints
    """
    return render(request, 'core/home.html')
