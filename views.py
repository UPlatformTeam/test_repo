from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from social_django.models import UserSocialAuth
from github import Github


def get_github(user):
    # Todo: may be not found
    user_social_auth = UserSocialAuth.objects.get(user=user)
    access_token = user_social_auth.extra_data['access_token']
    return Github(user_social_auth.user.username, access_token)
