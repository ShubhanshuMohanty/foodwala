from django.shortcuts import render
from chat.models import Mychats
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  # ✅ Use this instead of importing User directly

User = get_user_model()  # ✅ get the correct User model

@login_required
def index(request):
    frnd_name = request.GET.get('user', None)
    mychats_data = None
    if frnd_name:
        try:
            frnd_ = User.objects.get(username=frnd_name)
            mychats_obj = Mychats.objects.filter(me=request.user, frnd=frnd_).first()
            if mychats_obj:
                mychats_data = mychats_obj.chats
        except User.DoesNotExist:
            pass
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request, 'chat.html', {'my': mychats_data, 'chats': mychats_data, 'frnds': frnds})
