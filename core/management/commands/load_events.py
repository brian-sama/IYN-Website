from django.core.management.base import BaseCommand
from core.models import Event
from datetime import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = 'Load initial events from the static HTML page into the database'

    def handle(self, *args, **kwargs):
        events_data = [
            {
                'title': 'Youth Empowerment Summit',
                'slug': 'youth-empowerment-summit-2024',
                'description': 'A regional gathering of young changemakers to share ideas, build networks, and develop strategies for community impact. This summit brings together youth from across Southern Africa for three days of workshops, networking, and collaborative planning.',
                'location': 'Harare, Zimbabwe',
                'start_date': timezone.make_aware(datetime(2024, 12, 12,  9, 0)),
                'end_date': timezone.make_aware(datetime(2024, 12, 14, 17, 0)),
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Community Outreach Day',
                'slug': 'community-outreach-day-2025',
                'description': 'Hands-on service activities in local communities, bringing together youth volunteers to make a tangible difference. Activities include environmental clean-ups, educational workshops, and community development projects in underserved areas.',
                'location': 'Multiple Locations',
                'start_date': timezone.make_aware(datetime(2025, 1, 28, 8, 0)),
                'end_date': timezone.make_aware(datetime(2025, 1, 28, 16, 0)),
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Innovation Challenge 2025',
                'slug': 'innovation-challenge-2025',
                'description': 'Young entrepreneurs pitch their innovative solutions to address social challenges, competing for seed funding and mentorship. This year\'s focus areas include climate solutions, education technology, and healthcare innovations for underserved communities.',
                'location': 'Johannesburg, South Africa',
                'start_date': timezone.make_aware(datetime(2025, 2, 15, 9, 0)),
                'end_date': timezone.make_aware(datetime(2025, 2, 15, 18, 0)),
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'International Women\'s Day Celebration',
                'slug': 'international-womens-day-2025',
                'description': 'A special event celebrating young women leaders and their contributions to society. Featuring panel discussions, workshops on women\'s leadership, and networking opportunities with established female leaders across various sectors.',
                'location': 'Cape Town, South Africa',
                'start_date': timezone.make_aware(datetime(2025, 3, 8, 10, 0)),
                'end_date': timezone.make_aware(datetime(2025, 3, 8, 16, 0)),
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Earth Day Youth Action',
                'slug': 'earth-day-youth-action-2025',
                'description': 'Youth-led environmental initiatives and climate action projects across our network countries. Join tree planting campaigns, recycling drives, and climate education workshops to mark Earth Day 2025.',
                'location': 'Regional - Multiple Countries',
                'start_date': timezone.make_aware(datetime(2025, 4, 22, 8, 0)),
                'end_date': timezone.make_aware(datetime(2025, 4, 22, 18, 0)),
                'is_featured': False,
                'is_published': True,
            },
        ]

        created_count = 0
        skipped_count = 0

        for data in events_data:
            # Check if event already exists (by slug)
            if not Event.objects.filter(slug=data['slug']).exists():
                Event.objects.create(**data)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created event: {data["title"]}'))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'- Skipped {data["title"]} (already exists)'))

        self.stdout.write(self.style.SUCCESS(f'\n{created_count} events created, {skipped_count} skipped'))
