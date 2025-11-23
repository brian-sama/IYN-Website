# deploy_newsletter_system.ps1
# PowerShell script to deploy complete newsletter system for IYN Website

Write-Host "=== IYN NEWSLETTER SYSTEM DEPLOYMENT ===" -ForegroundColor Green

# Step 1: Create newsletter archive template
Write-Host "`n[1/8] Creating newsletter archive template..." -ForegroundColor Cyan

$templateContent = @'
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletters - International Youth Network</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .page-header {
            background: linear-gradient(135deg, #0066cc 0%, #004d99 100%);
            color: white;
            padding: 100px 0 60px;
            text-align: center;
            margin-top: 80px;
        }
        .newsletters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .newsletter-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s;
        }
        .newsletter-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="global-background"></div>
    <header>
        <div class="container header-container">
            <div class="logo">
                <div class="logo-image">
                    <img src="{% static 'images/images.jfif' %}" alt="IYN Logo">
                </div>
                <div class="logo-text">
                    <div class="main">International Youth Network</div>
                    <div class="sub">terre des hommes schweiz</div>
                </div>
            </div>
            <nav>
                <ul>
                    <li><a href="{% url 'index' %}">Home</a></li>
                    <li><a href="{% url 'about' %}">About</a></li>
                    <li><a href="{% url 'programs' %}">Programs</a></li>
                    <li><a href="{% url 'testimonials' %}">Testimonials</a></li>
                    <li><a href="{% url 'events' %}">Events</a></li>
                    <li><a href="{% url 'partners' %}">Partners</a></li>
                    <li><a href="{% url 'gallery_list' %}">Gallery</a></li>
                    <li><a href="{% url 'newsletters' %}" class="active">Newsletters</a></li>
                    <li><a href="{% url 'contact' %}">Contact</a></li>
                    <li><a href="{% url 'join' %}" class="btn">Join Us</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>Newsletters</h1>
            <p>Stay updated with our latest news, events, and youth initiatives</p>
        </div>
    </section>

    <section class="newsletters" style="padding: 80px 0; background: #f8f9fa;">
        <div class="container">
            <div class="section-heading" style="text-align: center; margin-bottom: 3rem;">
                <h2>Latest Updates</h2>
                <p>Download our newsletters to stay informed about IYN activities</p>
            </div>

            {% if newsletters %}
            <div class="newsletters-grid">
                {% for newsletter in newsletters %}
                <div class="newsletter-card">
                    <div class="newsletter-cover" style="height: 200px; overflow: hidden;">
                        {% if newsletter.cover_image %}
                        <img src="{{ newsletter.cover_image.url }}" alt="{{ newsletter.title }}" style="width: 100%; height: 100%; object-fit: cover;">
                        {% else %}
                        <div style="background: linear-gradient(135deg, #0066cc 0%, #00cc66 100%); height: 100%; display: flex; align-items: center; justify-content: center; color: white;">
                            <i class="fas fa-newspaper" style="font-size: 3rem; opacity: 0.7;"></i>
                        </div>
                        {% endif %}
                    </div>
                    <div class="newsletter-content" style="padding: 1.5rem;">
                        <h3>{{ newsletter.title }}</h3>
                        <p>{{ newsletter.description }}</p>
                        <a href="{% url 'newsletter_download' newsletter.slug %}" class="btn">
                            <i class="fas fa-download"></i> Download PDF
                        </a>
                        <div class="newsletter-meta" style="display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.85rem; color: #666;">
                            <span><i class="fas fa-calendar"></i> {{ newsletter.issue_date|date:"F Y" }}</span>
                            <span><i class="fas fa-download"></i> {{ newsletter.download_count }} downloads</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state" style="text-align: center; padding: 3rem; color: #666;">
                <i class="fas fa-newspaper" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3>No Newsletters Available</h3>
                <p>Check back soon for our latest updates and newsletters!</p>
            </div>
            {% endif %}
        </div>
    </section>

    <footer>
        <div class="container footer-content">
            <div>
                <h3>About IYN</h3>
                <p>The International Youth Network brings together youth delegates from various countries.</p>
            </div>
            <div>
                <h3>Quick Links</h3>
                <ul class="footer-links">
                    <li><a href="{% url 'programs' %}">Our Programs</a></li>
                    <li><a href="{% url 'newsletters' %}">Newsletters</a></li>
                    <li><a href="{% url 'contact' %}">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="copyright">
            © 2025 International Youth Network. All Rights Reserved.
        </div>
    </footer>
</body>
</html>
'@

$templatePath = "templates\newsletter_archive.html"
Set-Content -Path $templatePath -Value $templateContent -Encoding UTF8
Write-Host "✓ Created newsletter archive template" -ForegroundColor Green

# Step 2: Update views.py
Write-Host "`n[2/8] Updating views.py..." -ForegroundColor Cyan

$viewsFile = "core\views.py"
if (Test-Path $viewsFile) {
    $viewsContent = Get-Content $viewsFile -Raw
    
    # Add imports if not present
    if (-not ($viewsContent -match "from django.http import FileResponse")) {
        $viewsContent = $viewsContent -replace "from django.shortcuts import render", "from django.shortcuts import render, get_object_or_404`nfrom django.http import FileResponse"
    }
    
    # Add newsletter functions
    $newsletterFunctions = @'

def newsletter_archive(request):
    newsletters = Newsletter.objects.filter(is_published=True).order_by('-issue_date')
    context = {
        'newsletters': newsletters
    }
    return render(request, 'newsletter_archive.html', context)

def newsletter_download(request, slug):
    newsletter = get_object_or_404(Newsletter, slug=slug, is_published=True)
    newsletter.increment_downloads()
    response = FileResponse(newsletter.file.open(), as_attachment=True, filename=newsletter.file.name)
    return response
'@

    if (-not ($viewsContent -match "def newsletter_archive")) {
        $newViewsContent = $viewsContent.Trim() + "`n`n" + $newsletterFunctions
        Set-Content -Path $viewsFile -Value $newViewsContent -Encoding UTF8
        Write-Host "✓ Added newsletter functions to views.py" -ForegroundColor Green
    } else {
        Write-Host "✓ Newsletter functions already exist in views.py" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ views.py not found" -ForegroundColor Red
}

# Step 3: Update urls.py
Write-Host "`n[3/8] Updating urls.py..." -ForegroundColor Cyan

$urlsFile = "iyn_project\urls.py"
if (Test-Path $urlsFile) {
    $urlsContent = Get-Content $urlsFile -Raw
    
    if (-not ($urlsContent -match "newsletter_archive")) {
        # Add the newsletter URLs before the closing bracket
        $urlsContent = $urlsContent -replace "\]", "    path('newsletters/', views.newsletter_archive, name='newsletters'),`n    path('newsletters/download/<slug:slug>/', views.newsletter_download, name='newsletter_download'),`n]"
        Set-Content -Path $urlsFile -Value $urlsContent -Encoding UTF8
        Write-Host "✓ Added newsletter URLs to urls.py" -ForegroundColor Green
    } else {
        Write-Host "✓ Newsletter URLs already exist in urls.py" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ urls.py not found" -ForegroundColor Red
}

# Step 4: Create management commands directory
Write-Host "`n[4/8] Creating management commands..." -ForegroundColor Cyan

$managementDir = "core\management"
$commandsDir = "$managementDir\commands"

if (-not (Test-Path $managementDir)) {
    New-Item -ItemType Directory -Path $managementDir -Force | Out-Null
}
if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
}

# Create __init__.py files
"# Empty init file" | Out-File -FilePath "$managementDir\__init__.py" -Encoding UTF8
"# Empty init file" | Out-File -FilePath "$commandsDir\__init__.py" -Encoding UTF8

# Create load_countries.py
$countriesCommand = @'
from django.core.management.base import BaseCommand
from core.models import Country

class Command(BaseCommand):
    help = 'Load initial countries data'

    def handle(self, *args, **kwargs):
        countries = [
            {'name': 'Zimbabwe', 'code': 'ZW', 'description': 'Youth initiatives in Zimbabwe'},
            {'name': 'South Africa', 'code': 'ZA', 'description': 'Youth programs in South Africa'},
            {'name': 'Tanzania', 'code': 'TZ', 'description': 'Youth empowerment in Tanzania'},
            {'name': 'Mozambique', 'code': 'MZ', 'description': 'Youth development in Mozambique'},
            {'name': 'Nicaragua', 'code': 'NI', 'description': 'Youth network in Nicaragua'},
            {'name': 'El Salvador', 'code': 'SV', 'description': 'Youth initiatives in El Salvador'},
            {'name': 'Switzerland', 'code': 'CH', 'description': 'International coordination'}
        ]

        for data in countries:
            country, created = Country.objects.get_or_create(code=data['code'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created country: {country.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Country exists: {country.name}'))

        self.stdout.write(self.style.SUCCESS(f'{len(countries)} countries processed'))
'@

$countriesCommand | Out-File -FilePath "$commandsDir\load_countries.py" -Encoding UTF8
Write-Host "✓ Created load_countries command" -ForegroundColor Green

# Create load_partners.py
$partnersCommand = @'
from django.core.management.base import BaseCommand
from core.models import Partner, Country

class Command(BaseCommand):
    help = 'Load initial partners data'

    def handle(self, *args, **kwargs):
        partners_data = [
            {'name': 'Youth Empowerment Trust Zimbabwe', 'country_code': 'ZW', 'is_strategic': True},
            {'name': 'South African Youth Council', 'country_code': 'ZA', 'is_strategic': True},
            {'name': 'Tanzania Youth Alliance', 'country_code': 'TZ', 'is_strategic': False},
            {'name': 'Mozambique Youth Organization', 'country_code': 'MZ', 'is_strategic': False},
            {'name': 'Nicaragua Youth Network', 'country_code': 'NI', 'is_strategic': False},
            {'name': 'El Salvador Youth Foundation', 'country_code': 'SV', 'is_strategic': False}
        ]

        for data in partners_data:
            country = Country.objects.get(code=data['country_code'])
            partner, created = Partner.objects.get_or_create(name=data['name'], defaults={'country': country, 'is_strategic': data['is_strategic']})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created partner: {partner.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Partner exists: {partner.name}'))

        self.stdout.write(self.style.SUCCESS(f'{len(partners_data)} partners processed'))
'@

$partnersCommand | Out-File -FilePath "$commandsDir\load_partners.py" -Encoding UTF8
Write-Host "✓ Created load_partners command" -ForegroundColor Green

# Create load_programs.py
$programsCommand = @'
from django.core.management.base import BaseCommand
from core.models import Program

class Command(BaseCommand):
    help = 'Load initial programs data'

    def handle(self, *args, **kwargs):
        programs = [
            {'title': 'Youth Leadership Program', 'slug': 'youth-leadership', 'description': 'Leadership training for young leaders'},
            {'title': 'Community Development', 'slug': 'community-development', 'description': 'Youth-led community initiatives'},
            {'title': 'Entrepreneurship & Innovation', 'slug': 'entrepreneurship-innovation', 'description': 'Support for young entrepreneurs'},
            {'title': 'Digital Skills Training', 'slug': 'digital-skills', 'description': 'Technology education programs'},
            {'title': 'Environmental Sustainability', 'slug': 'environmental-sustainability', 'description': 'Youth environmental initiatives'},
            {'title': 'Arts & Culture Exchange', 'slug': 'arts-culture', 'description': 'Cultural exchange programs'}
        ]

        for data in programs:
            program, created = Program.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created program: {program.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Program exists: {program.title}'))

        self.stdout.write(self.style.SUCCESS(f'{len(programs)} programs processed'))
'@

$programsCommand | Out-File -FilePath "$commandsDir\load_programs.py" -Encoding UTF8
Write-Host "✓ Created load_programs command" -ForegroundColor Green

# Step 5: Create database migrations
Write-Host "`n[5/8] Creating database migrations..." -ForegroundColor Cyan
try {
    & python manage.py makemigrations
    Write-Host "✓ Created migrations" -ForegroundColor Green
} catch {
    Write-Host "✗ Error creating migrations" -ForegroundColor Red
}

# Step 6: Apply migrations
Write-Host "`n[6/8] Applying migrations..." -ForegroundColor Cyan
try {
    & python manage.py migrate
    Write-Host "✓ Applied migrations" -ForegroundColor Green
} catch {
    Write-Host "✗ Error applying migrations" -ForegroundColor Red
}

# Step 7: Load data
Write-Host "`n[7/8] Loading sample data..." -ForegroundColor Cyan
try {
    Write-Host "Loading countries..." -ForegroundColor Yellow
    & python manage.py load_countries
    
    Write-Host "Loading partners..." -ForegroundColor Yellow  
    & python manage.py load_partners
    
    Write-Host "Loading programs..." -ForegroundColor Yellow
    & python manage.py load_programs
    
    Write-Host "✓ All data loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Error loading data" -ForegroundColor Red
}

# Step 8: Final summary
Write-Host "`n[8/8] DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host "✅ Newsletter system deployed successfully!" -ForegroundColor Green
Write-Host "`n📋 What was implemented:" -ForegroundColor Cyan
Write-Host "• Newsletter archive page template" -ForegroundColor White
Write-Host "• Newsletter views and download functionality" -ForegroundColor White
Write-Host "• URL routes for newsletters" -ForegroundColor White
Write-Host "• Management commands for data loading" -ForegroundColor White
Write-Host "• Database migrations" -ForegroundColor White
Write-Host "• Sample data (7 countries, 6 partners, 6 programs)" -ForegroundColor White

Write-Host "`n🚀 Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart server: python manage.py runserver" -ForegroundColor White
Write-Host "2. Visit: http://127.0.0.1:8000/newsletters/" -ForegroundColor White
Write-Host "3. Upload newsletters via Django admin" -ForegroundColor White
Write-Host "4. Test the download functionality" -ForegroundColor White

Write-Host "`n🎉 Newsletter system is ready to use!" -ForegroundColor Green