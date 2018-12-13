import random
from django.contrib.auth import get_user_model

user_name = 'admin'
user_pass = "Admin.%s" % random.randint(10000000, 100000000)
user_email = 'admin@example.com'

User = get_user_model()
try:
    admin = User.objects.get(username=user_name)
    print("Admin already created")
except:
    User.objects.create_superuser(user_name, user_email, user_pass)
    print("Admin created with pass [%s] " % user_pass)
