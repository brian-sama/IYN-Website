from django.core.management.base import BaseCommand
from core.models import Partner, Country
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Loads initial partner and country data'

    def handle(self, *args, **kwargs):
        # 1. Create Countries
        countries_data = [
            {'name': 'Zimbabwe', 'code': 'ZW', 'gradient_start': '#0066cc', 'gradient_end': '#004d99'},
            {'name': 'South Africa', 'code': 'ZA', 'gradient_start': '#0066cc', 'gradient_end': '#004d99'},
            {'name': 'Tanzania', 'code': 'TZ', 'gradient_start': '#00cc99', 'gradient_end': '#00a67c'},
            {'name': 'Mozambique', 'code': 'MZ', 'gradient_start': '#ff6b6b', 'gradient_end': '#ee5a52'},
            {'name': 'Nicaragua', 'code': 'NI', 'gradient_start': '#ffa726', 'gradient_end': '#f57c00'},
            {'name': 'El Salvador', 'code': 'SV', 'gradient_start': '#ab47bc', 'gradient_end': '#8e24aa'},
            {'name': 'Switzerland', 'code': 'CH', 'gradient_start': '#26c6da', 'gradient_end': '#00acc1'},
        ]

        countries = {}
        for c_data in countries_data:
            country, created = Country.objects.get_or_create(
                name=c_data['name'],
                defaults={
                    'code': c_data['code'],
                    'gradient_color_start': c_data['gradient_start'],
                    'gradient_color_end': c_data['gradient_end']
                }
            )
            countries[c_data['name']] = country
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created country: {country.name}'))

        # 2. Create Strategic Partners
        strategic_partners = [
            {
                'name': 'Terre des Hommes Schweiz',
                'description': 'Our founding partner and supporter',
                'is_strategic': True,
                'country': countries['Switzerland']
            },
            {
                'name': 'Global Youth Networks',
                'description': 'International collaboration partners',
                'is_strategic': True,
                'country': None
            },
            {
                'name': 'Educational Institutions',
                'description': 'University and college partners',
                'is_strategic': True,
                'country': None
            }
        ]

        for p_data in strategic_partners:
            partner, created = Partner.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'is_strategic': p_data['is_strategic'],
                    'country': p_data['country']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created strategic partner: {partner.name}'))

        # 3. Create Zimbabwe Partners
        zim_partners = [
            {
                'name': 'Million Memory Project Zimbabwe (MMPZ)',
                'description': 'Million Memory Project Zimbabwe focuses on preserving cultural heritage and empowering youth through arts, storytelling, and community engagement. They work with young people to document oral histories, create digital archives, and develop creative projects that celebrate Zimbabwean culture while addressing contemporary social issues.',
                'country': countries['Zimbabwe'],
                'logo_file': 'mmpz.jpg'
            },
            {
                'name': 'Lunia Centre for Youths',
                'description': 'Lunia Centre for Youths provides comprehensive support for rural youth through education programs, skills training, and community development initiatives. They focus on empowering young people in remote areas with practical skills, leadership training, and resources to become agents of positive change in their communities.',
                'country': countries['Zimbabwe'],
                'logo_file': 'lunia.webp'
            },
            {
                'name': 'Bekezela Home Based Care',
                'description': 'Bekezela Home Based Care provides essential healthcare services and support to vulnerable communities, with a focus on youth health education and HIV/AIDS prevention. They train young peer educators, distribute health information, and offer counseling services to promote healthy lifestyles and reduce stigma around health issues.',
                'country': countries['Zimbabwe'],
                'logo_file': None # Placeholder in template
            },
            {
                'name': 'Bantwana Zimbabwe',
                'description': 'Bantwana Zimbabwe focuses on improving the wellbeing of vulnerable children and youth through comprehensive support programs. They provide educational assistance, psychosocial support, life skills training, and economic strengthening initiatives to help young people overcome challenges and build brighter futures.',
                'country': countries['Zimbabwe'],
                'logo_file': None # Placeholder in template
            }
        ]

        import os
        from django.conf import settings
        from django.core.files import File

        for p_data in zim_partners:
            partner, created = Partner.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'country': p_data['country'],
                    'is_strategic': False
                }
            )
            
            if (created or not partner.logo) and p_data.get('logo_file'):
                file_path = os.path.join(settings.BASE_DIR, 'static', 'images', p_data['logo_file'])
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        partner.logo.save(p_data['logo_file'], File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Saved logo for: {partner.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Logo file not found: {file_path}'))

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created partner: {partner.name}'))
