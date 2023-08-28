from django.shortcuts import render

# Create your views here.


def delete_user_data(request):
    return render(request, 'index.html')
