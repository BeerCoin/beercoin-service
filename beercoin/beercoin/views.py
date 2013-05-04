# Create your views here.
from beercoin.util import as_json
from django.shortcuts import get_object_or_404
from beercoin.util.models import UserProfile, User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from actstream import action
from actstream.models import following, followers, actor_stream


class BeerCoinTransactionError(Exception):
    pass


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

    return {"success": True, "username": request.user.username}


@login_required
@as_json
def list_profiles(request):
    queryset = UserProfile.objects.get_visible_profiles(request.user)
    return [user_to_dict(x.user, x) for x in queryset]

@login_required
@as_json
def get_profile(request, profile_name):
    user = user_to_dict(get_object_or_404(User, username=profile_name))
    user["following"] = following(request.user)
    user["followers"] = followers(request.user)
    user["actions"] = [dict(verb=x.verb,
                            object=x.action_object and user_to_dict(x.action_object),
                            when=x.timestamp.strftime("%s"),
                            data=x.data)
                        for x in actor_stream(request.user)[:3]]
    return user

@transaction.commit_on_success
@login_required
@as_json
def issue_beercoin(request):
    owner = get_object_or_404(User, username=request.GET.get("owner"))
    comment = request.GET.get("comment", None)
    what_for = request.GET.get("what_for", None)
    issuer = request.user

    if issuer.username == owner.username:
        raise BeerCoinTransactionError("You can owe beers yourself")

    if issuer.profile.balance <= -10:
        raise BeerCoinTransactionError("You already owe a lot. Not acceptable.")   # fixme: make better

    owner.profile.balance += 1
    issuer.profile.balance -= 1

    owner.profile.save()
    issuer.profile.save()

    action.send(issuer, verb="issued", action_object=owner,
            comment=comment, what_for=what_for)

    if owner.profile.balance == -10:
        action.send(issuer, verb="reached limit")

    return {"success": True}


@transaction.commit_on_success
@login_required
@as_json
def redeem_beercoin(request):
    issuer = get_object_or_404(User, username=request.GET.get("issuer"))
    comment = request.GET.get("comment", None)
    owner = request.user

    if issuer.username == owner.username:
        raise BeerCoinTransactionError("You can owe beers yourself")

    if owner.profile.balance <= 0:
        raise BeerCoinTransactionError("You can only redeem if you are in plus.") 

    owner.profile.balance -= 1
    issuer.profile.balance += 1

    owner.profile.save()
    issuer.profile.save()

    action.send(owner, verb="redeemed", action_object=issuer,
            comment=comment)

    if issuer.profile.balance == 0:
        action.send(issuer, verb="freed")

    return {"success": True}