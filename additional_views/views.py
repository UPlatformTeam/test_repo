def get_auth_github(username):
    user = User.objects.get(username=username)
    return get_github(user)


def index(request):
    return render(request, 'index.html')


@login_required
def repos(request):
    g = get_github(request.user)
    repos = g.get_user().get_repos()

    repo_data = []
    for repo in repos:
        repo_data.append({'name': repo.name, 'full_name': repo.full_name})

    return render(request, 'repos.html', {'repos': repo_data})
