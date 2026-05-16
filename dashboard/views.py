from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(current_request):
    return render(current_request, 'dashboard/index.html')