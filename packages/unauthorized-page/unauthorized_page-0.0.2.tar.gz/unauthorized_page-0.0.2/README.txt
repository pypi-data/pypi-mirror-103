@unauthenticated_user(func, 'path')

A simple decorator to handle views for authorized sessions.

Sample (Django):

from django.shortcuts import redirect

@unauthenticated_user(redirect, 'home')
def some_view(request):
