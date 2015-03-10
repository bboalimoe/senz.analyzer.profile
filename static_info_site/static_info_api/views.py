import json
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from learner import Learner
from predictor import Predictor

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
def Learn(request):
    if request.method == 'POST':
        body = json.loads(request.body)  #body is deprecated
    else:
        return errorResponses("Error!")

    hypothesis_type = body["hypothesisType"]
    param_m         = body["paramM"]
    param_p         = body["paramP"]
    learner = Learner(hypothesis_type)
    learner.train(param_m, param_p)

    successResponses("Learning successfully!")

def Predict(request):
    if request.method == 'POST':
        body = json.loads(request.body)  #body is deprecated
    else:
        return errorResponses("Error!")

    user_mac        = body["userMac"]
    hypothesis_type = body["hypothesisType"]
    predictor = Predictor(user_mac)
    successResponses(predictor.predict(hypothesis_type))


