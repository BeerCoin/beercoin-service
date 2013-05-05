# Create your views here.
from beercoin.util import as_json
from django.shortcuts import get_object_or_404
from beercoin.util.models import UserProfile, User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from actstream import action
from actstream.models import following, followers, actor_stream

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render

site = Site.objects.get_current()

import pusher
pusher.app_id = settings.PUSHER_APP_ID
pusher.key = settings.PUSHER_APP_KEY
pusher.secret = settings.PUSHER_APP_SECRET

pushy = pusher.Pusher()


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

    return {"success": True, "username": request.user.username, "user": user_to_dict(request.user)}


@login_required
@as_json
def list_profiles(request):
    queryset = UserProfile.objects.get_visible_profiles(request.user)
    return [user_to_dict(x.user, x) for x in queryset]

@login_required
@as_json
def get_profile(request, profile_name):
    user = get_object_or_404(User, username=profile_name)
    user_d = user_to_dict(get_object_or_404(User, username=profile_name))
    user_d["following"] = following(user)
    user_d["followers"] = followers(user)
    user_d["actions"] = [dict(verb=x.verb,
                              object=x.action_object and user_to_dict(x.action_object),
                              when=int(x.timestamp.strftime("%s")) * 1000,
                              data=x.data)
                         for x in actor_stream(user)[:3]]
    return user_d

@transaction.commit_on_success
@login_required
@as_json
def issue_beercoin(request):
    owner = get_object_or_404(User, username=request.GET.get("owner"))
    comment = request.GET.get("comment", None)
    what_for = request.GET.get("what_for", None)
    issuer = request.user

    if issuer.username == owner.username:
        raise BeerCoinTransactionError("You can't owe beers yourself")

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


@login_required
@as_json
def ask_out(request):
    issuer = request.user
    user = get_object_or_404(User, username=request.GET.get("user"))
    comment = request.GET.get("comment", None)

    text_template = get_template('emails/ask_to_go_for_beer.txt')
    #html_template = get_template('emails/request_beercoin_redemption.html')

    context_vars = Context({ 'user': user, 'issuer': issuer, 'comment': comment})

    text_content = text_template.render(context_vars)
    #html_content = html_template.render(context_vars)
    msg = EmailMultiAlternatives("Let's go out for a beer", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    #msg.attach_alternative(html_content, "text/html")
    msg.send()

    try:
        pushy["user_" + user.username].trigger("msg", {
                "type": "ask_out",
                "message": "Let's go out for a beer.",
                "comment": request.GET.get("comment"),
                "from": user_to_dict(issuer)
            });
    except Exception:
        pass

    return {"success": True}


@transaction.commit_on_success
@login_required
@as_json
def redeem_beercoin(request):
    issuer = get_object_or_404(User, username=request.GET.get("issuer"))
    comment = request.GET.get("comment", None)
    owner = request.user

    if issuer.username == owner.username:
        raise BeerCoinTransactionError("You can't owe beers yourself")

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

@login_required
@as_json
def request_beercoin_redemption(request):
    issuer = request.user
    owner = get_object_or_404(User, username=request.GET.get("owner"))
    comment = request.GET.get("comment", None)

    text_template = get_template('emails/request_beercoin_redemption.txt')
    #html_template = get_template('emails/request_beercoin_redemption.html')

    context_vars = Context({ 'owner': owner, 'issuer': issuer, 'site': site, 'comment': comment})

    text_content = text_template.render(context_vars)
    #html_content = html_template.render(context_vars)
    msg = EmailMultiAlternatives('You owe me a beer', text_content, settings.DEFAULT_FROM_EMAIL, [owner.email])
    #msg.attach_alternative(html_content, "text/html")
    msg.send()


    try:
        pushy["user_" + owner.username].trigger("msg", {
                "type": "owe",
                "message": "Hey, you owe me a beer",
                "comment": comment,
                "from": user_to_dict(issuer)
            });
    except Exception:
        pass

    return {"success": True}

@login_required
def grant_beercoin_redemption(request):
    owner = request.user
    issuer = get_object_or_404(User, username=request.GET.get("issuer"))

    return render(request, 'grant_redemption.html', locals())
