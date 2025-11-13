from celery import shared_task
import time
import random
from django.core.mail import send_mail


# LAB 4: Heavy Background Tasks

@shared_task
def process_large_dataset(size):
    """
    Simulates processing a large dataset
    Heavy CPU-bound task that takes time
    """
    result = []
    for i in range(size):
        # Simulate complex calculations
        value = sum([random.randint(1, 100) for _ in range(1000)])
        result.append(value)
        time.sleep(0.1)  # Simulate processing time
    
    return {
        'status': 'completed',
        'processed_items': len(result),
        'total_sum': sum(result)
    }


@shared_task
def generate_report(report_type, user_id):
    """
    Simulates generating a complex report
    Heavy I/O and computation task
    """
    time.sleep(5)  # Simulate report generation time
    
    # Simulate report data generation
    report_data = {
        'report_type': report_type,
        'user_id': user_id,
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'rows': random.randint(1000, 5000),
        'status': 'success'
    }
    
    # Simulate some heavy processing
    for i in range(10):
        _ = sum([random.randint(1, 1000) for _ in range(10000)])
        time.sleep(0.3)
    
    return report_data


# LAB 5: Scheduled Tasks

@shared_task
def cleanup_old_data():
    """
    Scheduled task to run every 3 minutes
    Cleans up old data from the system
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running cleanup_old_data task...")
    time.sleep(2)
    
    # Simulate cleanup
    deleted_count = random.randint(10, 100)
    
    return {
        'task': 'cleanup_old_data',
        'deleted_items': deleted_count,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }


@shared_task
def send_daily_summary():
    """
    Task to be scheduled at specific time via Django admin
    Sends daily summary email
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sending daily summary...")
    time.sleep(3)
    
    return {
        'task': 'send_daily_summary',
        'emails_sent': random.randint(50, 200),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }


@shared_task
def backup_database():
    """
    Task to be scheduled at specific interval via Django admin
    Performs database backup
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting database backup...")
    time.sleep(4)
    
    return {
        'task': 'backup_database',
        'backup_size_mb': random.randint(100, 500),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }


# Helper task for testing
@shared_task
def add_numbers(x, y):
    time.sleep(3)
    return x + y
