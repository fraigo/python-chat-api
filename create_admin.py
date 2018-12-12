from django.contrib.auth import get_user_model

user_name = 'admin'
user_pass = 'Admin.123456'
user_email = 'admin@example.com'

User = get_user_model()
try:
    admin = User.objects.get(username=user_name)
    print("admin already created")
except:
    User.objects.create_superuser(user_name, user_email, user_pass)
    print("admin created")