from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # LAB 4: Background Immediate Tasks
    path('process-dataset/', views.trigger_dataset_processing, name='process_dataset'),
    path('generate-report/', views.trigger_report_generation, name='generate_report'),
    path('task-status/<str:task_id>/', views.check_task_status, name='task_status'),
    
    # LAB 6: Caching Examples
    path('cache/function/', views.cached_function_view, name='cached_function'),
    path('cache/orm/', views.cached_orm_query_view, name='cached_orm'),
    path('cache/full-view/', views.cached_full_view, name='cached_full_view'),
    path('cache/template/', views.template_fragment_view, name='template_fragment'),
    path('cache/clear/', views.clear_cache_view, name='clear_cache'),
]
