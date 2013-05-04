# Create your views here.
from beercoin.util import as_json
from django.shortcuts import get_object_or_404
from beercoin.util.models import UserProfile, User


def user_to_dict(user, profile=None):
    if not profile:
        profile = user.profile
    return dict(username=user.username,
                name=user.get_full_name() or user.username,
                balance=profile.balance,
                icon=profile.get_mugshot_url(),
                location=profile.location)


@as_json
def check_login(request):
    if not request.user.is_authenticated():
        return {"success": False}

    return {"success": True, "username": request.user.username, "user": user_to_dict(request.user)}


@as_json
def list_profiles(request):
    queryset = UserProfile.objects.get_visible_profiles(request.user)
    return [user_to_dict(x.user, x) for x in queryset]


@as_json
def get_profile(request, profile_name):
    print profile_name
    user = get_object_or_404(User, username=profile_name)
    return user_to_dict(user)
