# Create your views here.
from beercoin.util import as_json

@as_json
def check_login(request):
    if not request.user.is_authenticated():
        return {"success": False}

    return {"success": True, "username": request.user.username}