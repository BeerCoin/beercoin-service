# Create your views here.
from beercoin.util import as_json
from beercoin.util.models import UserProfile

def user_to_dict(user, profile):
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

    return {"success": True, "username": request.user.username}


@as_json
def get_profiles(request):
    queryset = UserProfile.objects.get_visible_profiles(request.user)
    return [user_to_dict(x.user, x) for x in queryset]
