from django.core.management.base import BaseCommand
from core.models import Program
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class Command(BaseCommand):
    help = 'Loads initial program data from static content'

    def handle(self, *args, **kwargs):
        programs_data = [
            {
                'title': 'Youth Leadership Program',
                'description': 'Comprehensive mentorship and leadership training for emerging young leaders ready to make an impact. This program includes workshops, one-on-one mentoring, and practical community projects.',
                'image_url': 'https://images.unsplash.com/photo-1531206715517-5c0ba140b2b8?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 1
            },
            {
                'title': 'Community Development',
                'description': 'Empowering youth-led initiatives that create sustainable change in local communities. Participants learn project management, community engagement, and sustainable development practices.',
                'image_url': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 2
            },
            {
                'title': 'Entrepreneurship & Innovation',
                'description': 'Supporting young entrepreneurs with training, mentorship, and seed funding opportunities. Learn business planning, financial management, and innovation strategies.',
                'image_url': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 3
            },
            {
                'title': 'Digital Skills Training',
                'description': 'Bridging the digital divide by providing technology education, coding skills, and digital literacy programs for youth in underserved communities.',
                'image_url': 'https://images.unsplash.com/photo-1523580494863-6f3031224c94?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 4
            },
            {
                'title': 'Environmental Sustainability',
                'description': 'Youth-led environmental initiatives focusing on conservation, climate action, and sustainable practices in communities across our network countries.',
                'image_url': 'https://images.unsplash.com/photo-1562564055-71e051d33c19?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 5
            },
            {
                'title': 'Arts & Culture Exchange',
                'description': 'Promoting cultural understanding and creative expression through arts programs, cultural exchanges, and creative collaborations between youth from different countries.',
                'image_url': 'https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?auto=format&fit=crop&w=600&h=400&q=80',
                'display_order': 6
            }
        ]

        for data in programs_data:
            program, created = Program.objects.get_or_create(
                title=data['title'],
                defaults={
                    'slug': slugify(data['title']),
                    'description': data['description'],
                    'display_order': data['display_order'],
                    'icon_class': 'fas fa-star'
                }
            )
            
            if created or not program.image:
                self.stdout.write(f"Downloading image for {program.title}...")
                try:
                    response = requests.get(data['image_url'])
                    if response.status_code == 200:
                        file_name = f"{slugify(data['title'])}.jpg"
                        program.image.save(file_name, ContentFile(response.content), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Saved image for: {program.title}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to download image for {program.title}: {e}'))

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created program: {program.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Program already exists: {program.title}'))
