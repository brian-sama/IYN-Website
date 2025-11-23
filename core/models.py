from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Country(models.Model):
    """Model for partner countries"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)  # ISO country code
    flag_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    gradient_color_start = models.CharField(max_length=7, default='#0066cc')  # Hex color
    gradient_color_end = models.CharField(max_length=7, default='#004d99')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class Partner(models.Model):
    """Model for partner organizations"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/logos/')
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='partners')
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    is_strategic = models.BooleanField(default=False, help_text="Mark as strategic partner")
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Program(models.Model):
    """Model for IYN programs and initiatives"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., 'fas fa-users')")
    image = models.ImageField(upload_to='programs/', blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class Event(models.Model):
    """Model for events"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='events/', blank=True)
    registration_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_past(self):
        end = self.end_date if self.end_date else self.start_date
        return end < timezone.now()


class Testimonial(models.Model):
    """Model for user testimonials"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g., Youth Delegate, Zimbabwe")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


class ContactSubmission(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Admin notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    """Model for newsletter subscribers"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    """Model for newsletter publications"""
    title = models.CharField(max_length=200, help_text="Newsletter title (e.g., 'IYN Monthly - January 2025')")
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text="Brief description of this newsletter edition")
    cover_image = models.ImageField(upload_to='newsletters/covers/', blank=True, help_text="Cover image/thumbnail")
    file = models.FileField(upload_to='newsletters/files/', help_text="Newsletter PDF or document")
    issue_number = models.CharField(max_length=50, blank=True, help_text="e.g., 'Vol 1, Issue 3'")
    publication_date = models.DateField(help_text="Date this newsletter was published")
    is_published = models.BooleanField(default=True, help_text="Make this newsletter publicly available")
    download_count = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return f"{self.title} ({self.publication_date.strftime('%B %Y')})"

    def increment_downloads(self):
        """Increment download counter"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class JoinSubmission(models.Model):
    """Model for Join Us form submissions"""
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    area_of_interest = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False, help_text="Mark as processed/contacted")
    is_approved = models.BooleanField(default=False, help_text="Mark as approved member")
    notes = models.TextField(blank=True, help_text="Admin notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Join Us Submission"
        verbose_name_plural = "Join Us Submissions"

    def __str__(self):
        return f"{self.full_name} - {self.country}"


class UserProfile(models.Model):
    """Extended user profile for registered members"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=100, blank=True)
    is_delegate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Gallery(models.Model):
    """Model for photo galleries"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    partner = models.ForeignKey(
        Partner, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='galleries',
        help_text="Leave blank for general IYN Activities gallery"
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_galleries')
    is_public = models.BooleanField(default=True, help_text="Public galleries are visible to all visitors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def image_count(self):
        return self.images.count()

    @property
    def cover_image(self):
        """Return the first image as cover"""
        return self.images.first()


class GalleryImage(models.Model):
    """Model for individual images in a gallery"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/%Y/%m/')
    caption = models.CharField(max_length=500, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_images')
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['upload_date']

    def __str__(self):
        return f"{self.gallery.title} - Image {self.pk}"

