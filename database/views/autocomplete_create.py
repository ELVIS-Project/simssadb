from database.models import GenreAsInStyle, GenreAsInType, GeographicArea, Instrument, Software
from django.shortcuts import render, redirect
from django.http import JsonResponse

def create_type(request):
    if request.method == 'POST':
        new_type_name = request.POST.get('typeName')
        type_names = [type.name for type in GenreAsInType.objects.all()]
        if new_type_name in type_names or len(new_type_name) < 2:
            return JsonResponse({'error': 'Invalid type input'})
        GenreAsInType.objects.create(name=new_type_name)
        return JsonResponse({'message': 'New type created successfully'})
    
    return JsonResponse({'error': 'Invalid type method'})

def create_style(request):
    if request.method == 'POST':
        new_style_name = request.POST.get('styleName')
        style_names = [style.name for style in GenreAsInStyle.objects.all()]
        if new_style_name in style_names or len(new_style_name) < 2:
            return JsonResponse({'error': 'Invalid style input'})
        GenreAsInStyle.objects.create(name=new_style_name)
        return JsonResponse({'message': 'New style created successfully'})
    
    return JsonResponse({'error': 'Invalid style method'})

def create_geographic_area(request):
    if request.method == 'POST':
        new_geographic_area_name = request.POST.get('geographicAreaName')
        geographic_area_names = [geographic_area.name for geographic_area in GeographicArea.objects.all()]
        if new_geographic_area_name in geographic_area_names or len(new_geographic_area_name) < 2:
            return JsonResponse({'error': 'Invalid geographic area input'})
        GeographicArea.objects.create(name=new_geographic_area_name)
        return JsonResponse({'message': 'New geographic area created successfully'})
    
    return JsonResponse({'error': 'Invalid geographic area method'})

def create_instrument(request):
    if request.method == 'POST':
        new_instrument_name = request.POST.get('instrumentName')
        instrument_names = [instrument.name for instrument in Instrument.objects.all()]
        if new_instrument_name in instrument_names or len(new_instrument_name) < 2:
            return JsonResponse({'error': 'Invalid instrument input'})
        Instrument.objects.create(name=new_instrument_name)
        return JsonResponse({'message': 'New instrument created successfully'})
    
    return JsonResponse({'error': 'Invalid instrument method'})

def create_software(request):
    if request.method == 'POST':
        new_software_name = request.POST.get('softwareName')
        software_names = [software.name for software in Software.objects.all()]
        if new_software_name in software_names or len(new_software_name) < 2:
            return JsonResponse({'error': 'Invalid instrument input'})
        Instrument.objects.create(name=new_software_name)
        return JsonResponse({'message': 'New instrument created successfully'})
    
    return JsonResponse({'error': 'Invalid instrument method'})