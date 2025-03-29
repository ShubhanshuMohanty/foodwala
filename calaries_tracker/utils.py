from django.contrib.auth import get_user_model

User = get_user_model()

def get_logged_in_user_email(request):
    if request.user.is_authenticated:  # Agar user logged in hai
        return request.user.email  # Directly email return karo

    # Agar session me user ID stored hai toh
    data = request.session.get('_auth_user_id')
    if data:
        try:
            user = User.objects.get(pk=data)  # ID se user object fetch karo
            print("email wala=",user.email)
            return user.email  # Email return karo
        except User.DoesNotExist:
            print("email wala= ert")
            return None  # User exist nahi karta
        
    print("email wala=efg")

    return None  # User logged in nahi hai
