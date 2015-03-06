import json
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def errorInfo():
    import sys
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])  # todo log the exception info
    print info
    return info

def errorResponses(error=None):
    if not error:
        info = errorInfo()
    else:
        info = error

    return JsonResponse({"status": 0}, {"errors": info})


def successResponses(results):

    return JsonResponse({"status": 1, "results": results})

@csrf_exempt
def StaticInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)  #body is deprecated
    else:
        return errorResponses("Error!")

    successResponses("Ok!")


