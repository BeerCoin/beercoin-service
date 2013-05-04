from django.http import HttpResponse
from django.utils import simplejson as json


def as_json(fun):
    def wrapped(request, *args, **kwargs):
        try:
            resp = fun(request, *args, **kwargs)
        except Exception as e:
            if request.GET.get("debug"):
                raise
            resp = {"error": e.__class__.__name__, "message": e.message}
            if hasattr(e, "extras"):
                resp["extras"] = e.extras

        return HttpResponse(json.dumps(resp), content_type="application/json")
    return wrapped
