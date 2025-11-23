from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import (
    Country, Partner, Program, Event, Testimonial,
    ContactSubmission, NewsletterSubscriber, UserProfile,
    Gallery, GalleryImage, JoinSubmission, Newsletter
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_strategic', 'is_active', 'display_order', 'created_at', 'updated_at']

    list_filter = ['is_strategic', 'is_active', 'country', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['display_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'display_order', 'created_at', 'updated_at']

    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['display_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_date', 'is_featured', 'is_published', 'created_at', 'updated_at']

    list_filter = ['is_featured', 'is_published', 'country', 'start_date']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'country', 'rating', 'is_approved', 'is_featured', 'created_at', 'updated_at']

    list_filter = ['is_approved', 'is_featured', 'rating', 'country', 'created_at']
    search_fields = ['name', 'role', 'content']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at', 'updated_at', 'submitted_by']
    actions = ['approve_testimonials', 'feature_testimonials']

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} testimonials approved.')
    approve_testimonials.short_description = "Approve selected testimonials"

    def feature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} testimonials featured.')
    feature_testimonials.short_description = "Feature selected testimonials"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_responded', 'created_at']
    list_filter = ['is_read', 'is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_responded']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_responded']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} submissions marked as read.')
    mark_as_read.short_description = "Mark as read"

    def mark_as_responded(self, request, queryset):
        updated = queryset.update(is_responded=True)
        self.message_user(request, f'{updated} submissions marked as responded.')
    mark_as_responded.short_description = "Mark as responded"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'issue_number', 'publication_date', 'is_published', 'download_count', 'created_at']
    list_filter = ['is_published', 'publication_date', 'created_at']
    search_fields = ['title', 'description', 'issue_number']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    readonly_fields = ['download_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Newsletter Information', {
            'fields': ('title', 'slug', 'issue_number', 'publication_date', 'description')
        }),
        ('Files', {
            'fields': ('cover_image', 'file')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Statistics', {
            'fields': ('download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'publication_date'


@admin.register(JoinSubmission)
class JoinSubmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'country', 'area_of_interest', 'is_processed', 'is_approved', 'created_at', 'updated_at']
    list_filter = ['is_processed', 'is_approved', 'country', 'created_at']
    search_fields = ['full_name', 'email', 'country', 'area_of_interest', 'message']
    list_editable = ['is_processed', 'is_approved']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone', 'country', 'organization')
        }),
        ('Interest & Details', {
            'fields': ('area_of_interest', 'message')
        }),
        ('Status', {
            'fields': ('is_processed', 'is_approved', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_processed', 'mark_as_approved']

    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} submissions marked as processed.')
    mark_as_processed.short_description = "Mark as processed"

    def mark_as_approved(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} submissions marked as approved.')
    mark_as_approved.short_description = "Mark as approved"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'organization', 'is_delegate', 'created_at', 'updated_at']

    list_filter = ['is_delegate', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'organization', 'role']
    readonly_fields = ['created_at', 'updated_at']


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    readonly_fields = ['uploaded_by', 'upload_date']
    fields = ['image', 'caption', 'uploaded_by', 'upload_date']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'partner', 'image_count', 'created_by', 'is_public', 'created_at', 'updated_at']

    list_filter = ['is_public', 'partner', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'image_count']
    inlines = [GalleryImageInline]
    
    def image_count(self, obj):
        return obj.image_count
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'caption', 'uploaded_by', 'upload_date']
    list_filter = ['gallery', 'upload_date', 'uploaded_by']
    search_fields = ['caption', 'gallery__title']
    readonly_fields = ['uploaded_by', 'upload_date']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Admin interface for viewing the admin action logs"""
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_time', 'user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    date_hierarchy = 'action_time'
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
