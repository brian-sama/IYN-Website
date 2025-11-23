from django.core.management.base import BaseCommand
from core.models import Testimonial, Country


class Command(BaseCommand):
    help = 'Load initial testimonials from the static HTML page into the database'

    def handle(self, *args, **kwargs):
        # Get or create countries
        zimbabwe, _ = Country.objects.get_or_create(
            code='ZW',
            defaults={'name': 'Zimbabwe'}
        )
        south_africa, _ = Country.objects.get_or_create(
            code='ZA',
            defaults={'name': 'South Africa'}
        )

        testimonials_data = [
            {
                'name': 'Tanaka Moyo',
                'role': 'Youth Entrepreneur, Zimbabwe',
                'country': zimbabwe,
                'content': 'IYN gave me the confidence and skills to start my own social enterprise. Through their mentorship program, I learned how to turn my passion for education into a sustainable business that now serves over 500 students in my community.',
                'rating': 5,
            },
            {
                'name': 'Thabo Ndlovu',
                'role': 'Community Leader, South Africa',
                'country': south_africa,
                'content': 'Being part of IYN connected me with like-minded youth leaders across Africa. The network has been instrumental in helping me launch community development projects that address unemployment and skills development in my township.',
                'rating': 5,
            },
            {
                'name': 'Rumbi Chikwanha',
                'role': 'Advocacy Coordinator, Zimbabwe',
                'country': zimbabwe,
                'content': 'IYN empowered me to find my voice and advocate for youth rights at both local and international levels. I\'ve had the opportunity to speak at regional forums and influence policies that directly affect young people.',
                'rating': 5,
            },
            {
                'name': 'Sipho Mthembu',
                'role': 'Tech Innovator, South Africa',
                'country': south_africa,
                'content': 'The entrepreneurship program gave me access to resources and mentorship that helped me develop a mobile app addressing health challenges in rural communities. IYN believed in my vision when others didn\'t.',
                'rating': 5,
            },
            {
                'name': 'Chipo Mutasa',
                'role': 'Environmental Activist, Zimbabwe',
                'country': zimbabwe,
                'content': 'Through IYN, I found a platform to amplify my environmental conservation work. The network helped me organize youth climate action campaigns that reached thousands of young people across the region.',
                'rating': 5,
            },
            {
                'name': 'Mandla Khumalo',
                'role': 'Arts Program Director, South Africa',
                'country': south_africa,
                'content': 'IYN\'s arts and culture program opened doors I never imagined possible. I\'ve been able to mentor young artists and create platforms for youth expression through music, dance, and visual arts.',
                'rating': 5,
            },
        ]

        created_count = 0
        skipped_count = 0

        for data in testimonials_data:
            # Check if testimonial already exists (by name)
            if not Testimonial.objects.filter(name=data['name']).exists():
                Testimonial.objects.create(
                    **data,
                    is_approved=True,  # Pre-approve these testimonials
                    is_featured=True   # Make them featured
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created testimonial for {data["name"]}'))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'- Skipped {data["name"]} (already exists)'))

        self.stdout.write(self.style.SUCCESS(f'\n{created_count} testimonials created, {skipped_count} skipped'))
