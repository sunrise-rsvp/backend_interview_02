import os
from celery import Celery

# Set default Django settings module for 'celery' program.
celery_app = None

def create_celery_app():
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get Redis connection info from environment
    redis_host = os.getenv('REDIS_HOST', 'interview-redis')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_password = os.getenv('REDIS_PASSWORD', 'redispw')
    
    redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
    
    celery_app = Celery(
        'interview_tasks',
        broker=redis_url,
        backend=redis_url,
        include=['tasks']  # Include task modules here
    )
    
    # Optional configuration, see the application user guide.
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    return celery_app

# Create the app when this module is imported
celery_app = create_celery_app()

if __name__ == '__main__':
    celery_app.start()
