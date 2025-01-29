from django.http import HttpResponse


def index(request):
    return HttpResponse('''
        <h1>Welcome to the Kissan Connect Apis</h1>
        <a href="/admin/">Go to Admin Page</a>
    ''')
