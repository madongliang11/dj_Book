from django.shortcuts import HttpResponse
import json

def test_param(request, art_pk):
	result = dict(
		data = int(art_pk) + 100,
		msg = 'ok',
		status = 200
	)

	return HttpResponse(json.dumps(result))