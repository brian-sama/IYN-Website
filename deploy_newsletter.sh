#!/bin/bash

echo "========================================"
echo "   IYN NEWSLETTER SYSTEM DEPLOYMENT"
echo "========================================"
echo

echo "[1/4] Creating newsletter archive template..."

cat > templates/newsletter_archive.html << 'EOF'
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Newsletters - International Youth Network</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <header>
        <nav>
            <a href="{% url 'index' %}">Home</a>
            <a href="{% url 'newsletters' %}">Newsletters</a>
        </nav>
    </header>
    
    <main style="padding: 2rem;">
        <h1>Newsletters</h1>
        <p>Download our latest newsletters and updates</p>
        
        {% if newsletters %}
            {% for newsletter in newsletters %}
            <div style="border: 1px solid #ccc; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
                <h3>{{ newsletter.title }}</h3>
                <p>{{ newsletter.description }}</p>
                <a href="{% url 'newsletter_download' newsletter.slug %}" class="btn">
                    <i class="fas fa-download"></i> Download PDF
                </a>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">
                    <i class="fas fa-calendar"></i> {{ newsletter.issue_date|date:"F Y" }}
                    <span style="margin-left: 1rem;">
                        <i class="fas fa-download"></i> {{ newsletter.download_count }} downloads
                    </span>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <p>No newsletters available yet. Check back soon!</p>
        {% endif %}
    </main>
</body>
</html>
EOF

echo "✓ Created newsletter archive template"
echo

echo "[2/4] Creating management commands directory..."
mkdir -p core/management/commands
touch core/management/__init__.py
touch core/management/commands/__init__.py

cat > core/management/commands/load_countries.py << 'EOF'
from django.core.management.base import BaseCommand
from core.models import Country

class Command(BaseCommand):
    def handle(self, *args, **options):
        countries = [
            {"name": "Zimbabwe", "code": "ZW"},
            {"name": "South Africa", "code": "ZA"},
            {"name": "Tanzania", "code": "TZ"},
            {"name": "Mozambique", "code": "MZ"},
            {"name": "Nicaragua", "code": "NI"},
            {"name": "El Salvador", "code": "SV"},
            {"name": "Switzerland", "code": "CH"}
        ]
        for data in countries:
            Country.objects.get_or_create(code=data["code"], defaults=data)
        print("Loaded 7 countries")
EOF

echo "✓ Created management commands"
echo

echo "[3/4] Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✓ Database migrations completed"
echo

echo "[4/4] Loading sample data..."
python manage.py load_countries
echo "✓ Sample data loaded"
echo

echo "========================================"
echo "          DEPLOYMENT COMPLETE!"
echo "========================================"
echo
echo "✅ What was created:"
echo "   - templates/newsletter_archive.html"
echo "   - Management commands for countries"
echo "   - Database migrations applied"
echo "   - Sample countries data loaded"
echo
echo "📋 MANUAL STEPS REQUIRED:"
echo
echo "1. Add to core/views.py:"
echo
echo "   def newsletter_archive(request):"
echo "       newsletters = Newsletter.objects.filter(is_published=True).order_by('-issue_date')"
echo "       context = {'newsletters': newsletters}"
echo "       return render(request, 'newsletter_archive.html', context)"
echo
echo "   def newsletter_download(request, slug):"
echo "       from django.http import FileResponse"
echo "       from django.shortcuts import get_object_or_404"
echo "       newsletter = get_object_or_404(Newsletter, slug=slug, is_published=True)"
echo "       newsletter.increment_downloads()"
echo "       response = FileResponse(newsletter.file.open(), as_attachment=True, filename=newsletter.file.name)"
echo "       return response"
echo
echo "2. Add to iyn_project/urls.py in urlpatterns:"
echo "   path('newsletters/', views.newsletter_archive, name='newsletters'),"
echo "   path('newsletters/download/<slug:slug>/', views.newsletter_download, name='newsletter_download'),"
echo
echo "3. Restart server and test:"
echo "   python manage.py runserver"
echo "   Then visit: http://127.0.0.1:8000/newsletters/"
echo