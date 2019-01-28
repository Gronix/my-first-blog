from django.shortcuts import redirect


def redirect_to_blog(request):
    return redirect('blog/')
