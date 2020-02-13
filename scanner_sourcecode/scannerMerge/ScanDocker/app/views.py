from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def aboutus(request):
    return render(request, 'about-us.html')

def services(request):
    return render(request, 'services.html')

def scanner(request):
    return render(request, 'scanner.html')

def scanner_scan(request):
    return render(request, 'scanner-scan.html')

def scanner_forms(request):
    return render(request, 'scanner-forms.html')

def scanner_charts(request):
    return render(request, 'scanner-charts.html')

def scanner_tables(request):
    return render(request, 'scanner-tables.html')

def knowledgegraph(request):
    return render(request, 'knowledgegraph.html')

def blogitem(request):
    return render(request, 'blog-item.html')

def pricing(request):
    return render(request, 'pricing.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

def test(request):
    return render(request, 'test.html')