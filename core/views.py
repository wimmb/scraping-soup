from django.shortcuts import render

from services import IMDBService
from django.http import JsonResponse


def index(request):

    context = {
        'active_page': 'home'
    }

    return render(request, 'core/index.html', context=context)


def scrape_data(request):
    category = request.GET['category']
    service = IMDBService.get_service(category=category)
    objects = service.get_objects()
    data = service.persist_objects(objects)
    return JsonResponse({'data': data})
