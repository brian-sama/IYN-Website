# 1. Add to urls.py
$urlsContent = Get-Content "iyn_project\urls.py" -Raw
$newUrlsContent = $urlsContent -replace "path\('join/', views\.join, name='join'\),", "path('join/', views.join, name='join'),`n    path('newsletters/', views.newsletters, name='newsletters'),"
Set-Content "iyn_project\urls.py" -Value $newUrlsContent -Encoding UTF8
Write-Host "Updated urls.py" -ForegroundColor Green

# 2. Add to views.py
$newslettersView = @"

def newsletters(request):
    context = {
        'title': 'Newsletters',
        'page': 'newsletters',
    }
    return render(request, 'newsletters.html', context)
"@

Add-Content "core\views.py" -Value "`n`n$newslettersView" -Encoding UTF8
Write-Host "Updated views.py" -ForegroundColor Green

# 3. Create template
$templateContent = @'
{% extends 'base.html' %}
{% load static %}

{% block title %}Newsletters{% endblock %}

{% block content %}
<h1>Newsletters</h1>
<p>This is the newsletters page.</p>
{% endblock %}
'@

Set-Content "templates\newsletters.html" -Value $templateContent -Encoding UTF8
Write-Host "Created newsletters template" -ForegroundColor Green

Write-Host "`nAll done! Restart your server with: python manage.py runserver" -ForegroundColor Cyan