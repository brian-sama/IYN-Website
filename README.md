# International Youth Network - Django Backend

## Project Structure

```
IYN Website/
├── backend/                    # Django project root
│   ├── iyn_project/           # Project configuration
│   │   ├── settings.py        # Main settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # WSGI config
│   ├── core/                  # Main app
│   │   ├── models.py          # Database models
│   │   ├── admin.py           # Admin configurations
│   │   ├── views.py           # View functions
│   │   ├── forms.py           # Form definitions
│   │   └── urls.py            # App URLs
│   ├── templates/             # HTML templates
│   ├── media/                 # User uploads
│   ├── manage.py              # Django management
│   └── requirements.txt       # Python dependencies
└── static/                    # Static files (CSS, JS, images)
```

## Features Implemented

✅ **Database Models:**
- Country - Partner countries with flags and colors
- Partner - Partner organizations with logos
- Program - IYN programs and initiatives
- Event - Event management with dates and locations
- Testimonial - User testimonials with approval system
- ContactSubmission - Contact form submissions
- NewsletterSubscriber - Email newsletter list
- UserProfile - Extended user information

✅ **Admin Interface:**
- Full CRUD operations for all models
- Custom list displays and filters
- Bulk actions (approve testimonials, mark as read, etc.)
- Search functionality
- File upload handling

✅ **Frontend Views:**
- Homepage with featured content
- About, Programs, Partners, Events, Testimonials pages
- Contact form with email notifications
- User registration and authentication
- User profile management
- Newsletter subscription
- Testimonial submission

## Getting Started

### 1. Create Superuser (Admin Account)

```bash
cd backend
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 2. Run Development Server

```bash
python manage.py runserver
```

The website will be available at: http://127.0.0.1:8000/

### 3. Access Admin Panel

Visit: http://127.0.0.1:8000/admin/

Login with the superuser credentials you created.

## Admin Panel Usage

### Adding Content

1. **Countries**: Add partner countries with flags and gradient colors
2. **Partners**: Upload partner logos and information
3. **Programs**: Create programs with icons and descriptions
4. **Events**: Add events with dates, locations, and images
5. **Testimonials**: Review and approve submitted testimonials
6. **Contact Submissions**: View and respond to contact form messages
7. **Newsletter Subscribers**: Manage email subscribers

### Managing Users

- View registered users
- Manage user profiles
- Mark users as delegates

## Available URLs

- `/` - Homepage
- `/about/` - About page
- `/programs/` - Programs page
- `/partners/` - Partners page
- `/events/` - Events page
- `/testimonials/` - Testimonials page
- `/contact/` - Contact form
- `/join/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile (requires login)
- `/admin/` - Admin panel

## Next Steps

### Template Integration (To Do)

The HTML templates have been copied but need Django template tags:

1. Update image paths to use `{{ MEDIA_URL }}` or `{% static %}`
2. Add `{% csrf_token %}` to all forms
3. Replace hardcoded links with `{% url 'name' %}`
4. Add template loops for dynamic content (partners, events, etc.)
5. Add authentication checks (`{% if user.is_authenticated %}`)

### Email Configuration (Optional)

To enable email notifications for contact forms, add to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Production Deployment (Future)

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up static file serving (WhiteNoise or CDN)
5. Configure environment variables for secrets
6. Set up proper email service

## Database

The project uses SQLite for development (`db.sqlite3`). All tables are created and ready to use.

## Media Files

Uploaded files (logos, photos, etc.) are stored in `backend/media/`.

## Static Files

Static files (CSS, JS, images) should be placed in the `static/` directory at the project root.

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic
```

### Database issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Clear all data
```bash
# Delete db.sqlite3 and run migrations again
python manage.py migrate
python manage.py createsuperuser
```

## Support

For questions or issues, refer to Django documentation: https://docs.djangoproject.com/
