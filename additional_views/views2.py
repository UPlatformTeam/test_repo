@login_required
@require_http_methods(['POST'])
def create_hook(request, repo_name):
    
    g = get_github(request.user)
    user = g.get_user()
    repo = user.get_repo(repo_name)

    print(repo)

    config = {
        'url': sensitive_data.WEBHOOK_URL,
        'content_type': 'json',
    }
    try:
        hook = repo.create_hook('web', config, ['pull_request'], True)
        print(hook)
    except:
        # Do nothing
        pass

    return redirect('/repos/')
