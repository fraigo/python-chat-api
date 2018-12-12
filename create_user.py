from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_superuser('admin', 'admin@myproject.com', 'Admin.123456')

