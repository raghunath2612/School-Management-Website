from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect

def check_if_username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    else:
        return False

def create_student_account(un):
    if check_if_username_exists(un):
        pass
    else:
        user = User.objects.create_user(username=un,password='Welcome@123')
        group = Group.objects.get(name="student")
        group.user_set.add(user) 

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                if group=="admin":
                    return HttpResponseRedirect("/home")
                elif group=="student":
                    return HttpResponseRedirect("/student")
        return wrapper_func
    return decorator


