from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import APIConnection
from .forms import APIConnectionForm
from .client import ClientAPI

def manage_api_connections(request):
    if request.method == 'POST':
        form = APIConnectionForm(request.POST)
        if 'create' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'API Connection created successfully.')
                return redirect('manage_api_connections')
        elif 'update' in request.POST:
            instance = APIConnection.objects.get(pk=request.POST.get('api_id'))
            form = APIConnectionForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'API Connection updated successfully.')
                return redirect('manage_api_connections')
        elif 'delete' in request.POST:
            api_id = request.POST.get('api_id')
            APIConnection.objects.filter(id=api_id).delete()
            messages.success(request, 'API Connection deleted successfully.')
            return redirect('manage_api_connections')
        elif 'test_connection' in request.POST:
            pass
        elif 'set_active' in request.POST:
            APIConnection.objects.update(active=False) 
            api_id = request.POST.get('api_id')
            api = APIConnection.objects.get(id=api_id)
            api.active = True
            api.save()
            messages.success(request, 'API Connection set as active successfully.')
            return redirect('manage_api_connections') 

    form = APIConnectionForm()
    api_connections = APIConnection.objects.all()
    return render(request, 'api_client/manage_api_connections.html', {
        'form': form,
        'api_connections': api_connections
    })

def edit_api_connection(request, pk):
    api_connection = get_object_or_404(APIConnection, pk=pk)
    if request.method == 'POST':
        form = APIConnectionForm(request.POST, instance=api_connection)
        if form.is_valid():
            form.save()
            return redirect('manage_api_connections')
    else:
        form = APIConnectionForm(instance=api_connection)
    
    context = {
        'form': form,
        'api_client_name': api_connection.name,
    }
    return render(request, 'api_client/edit_api_connection.html', context)