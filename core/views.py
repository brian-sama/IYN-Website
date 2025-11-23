from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from .models import Partner, Event, Testimonial, Program, Country, Gallery, GalleryImage, Newsletter
from .forms import (
    ContactForm, NewsletterForm, TestimonialSubmissionForm,
    UserRegistrationForm, UserProfileForm, GalleryForm, GalleryImageForm,
    JoinSubmissionForm
)


def index(request):
    """Homepage view"""
    partners = Partner.objects.filter(is_active=True)[:6]
    events = Event.objects.filter(is_published=True)[:3]
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:3]
    
    context = {
        'partners': partners,
        'events': events,
        'testimonials': testimonials,
    }
    return render(request, 'index.html', context)


def about(request):
    """About page view"""
    return render(request, 'about.html')


def programs(request):
    """Programs page view"""
    programs_list = Program.objects.filter(is_active=True)
    context = {'programs': programs_list}
    return render(request, 'programs.html', context)


def partners_view(request):
    """Partners page view"""
    countries = Country.objects.all()
    strategic_partners = Partner.objects.filter(is_strategic=True, is_active=True)
    
    context = {
        'countries': countries,
        'strategic_partners': strategic_partners,
    }
    return render(request, 'partners.html', context)


def partners_zimbabwe(request):
    """Zimbabwe Partners page view"""
    partners = Partner.objects.filter(country__name='Zimbabwe', is_active=True)
    return render(request, 'partners-zimbabwe.html', {'partners': partners})


def partners_southafrica(request):
    """South Africa Partners page view"""
    partners = Partner.objects.filter(country__name='South Africa', is_active=True)
    return render(request, 'partners-southafrica.html', {'partners': partners})


def events_view(request):
    """Events page view"""
    events_list = Event.objects.filter(is_published=True)
    paginator = Paginator(events_list, 9)  # Show 9 events per page
    
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    context = {'events': events}
    return render(request, 'events.html', context)


def testimonials_view(request):
    """Testimonials page view"""
    testimonials_list = Testimonial.objects.filter(is_approved=True)
    
    context = {'testimonials': testimonials_list}
    return render(request, 'testimonials.html', context)


def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)


def join(request):
    """Join Us page view - for membership interest submissions"""
    if request.method == 'POST':
        form = JoinSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your interest! We will contact you soon with next steps.')
            return redirect('join')
    else:
        form = JoinSubmissionForm()
    
    context = {'form': form}
    return render(request, 'join.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription handler (AJAX)"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to newsletter!')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def submit_testimonial(request):
    """Testimonial submission handler"""
    if request.method == 'POST':
        form = TestimonialSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            if request.user.is_authenticated:
                testimonial.submitted_by = request.user
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed before publishing.')
            return redirect('testimonials')
    else:
        form = TestimonialSubmissionForm()
    
    context = {'form': form}
    return render(request, 'submit_testimonial.html', context)


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def profile(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {'profile_form': profile_form}
    return render(request, 'profile.html', context)


def gallery_list(request):
    """Gallery list view with optional partner filtering"""
    partner_id = request.GET.get('partner')
    
    if request.user.is_authenticated:
        # Authenticated users can see all galleries
        galleries_list = Gallery.objects.all()
    else:
        # Anonymous users only see public galleries
        galleries_list = Gallery.objects.filter(is_public=True)
    
    # Filter by partner if specified
    if partner_id:
        galleries_list = galleries_list.filter(partner_id=partner_id)
    
    # Order by most recent
    galleries_list = galleries_list.order_by('-created_at')
    
    # Get all partners for filter dropdown
    partners = Partner.objects.filter(is_active=True)
    
    context = {
        'galleries': galleries_list,
        'partners': partners,
        'selected_partner': partner_id,
    }
    return render(request, 'gallery.html', context)


def gallery_detail(request, slug):
    """Gallery detail view showing all images"""
    gallery = get_object_or_404(Gallery, slug=slug)
    
    # Check permission for non-public galleries
    if not gallery.is_public and not request.user.is_authenticated:
        messages.error(request, 'This gallery is not publicly accessible.')
        return redirect('gallery_list')
    
    images = gallery.images.all()
    
    context = {
        'gallery': gallery,
        'images': images,
    }
    return render(request, 'gallery_detail.html', context)


@login_required
def gallery_upload(request, partner_id=None):
    """Gallery upload view - create gallery and upload multiple images"""
    # Create a formset for multiple image uploads
    ImageFormSet = modelformset_factory(GalleryImage, form=GalleryImageForm, extra=5, max_num=20)
    
    if request.method == 'POST':
        gallery_form = GalleryForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.none())
        
        if gallery_form.is_valid() and image_formset.is_valid():
            # Save gallery
            gallery = gallery_form.save(commit=False)
            gallery.created_by = request.user
            gallery.save()
            
            # Save images
            images_count = 0
            for image_form in image_formset:
                if image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.gallery = gallery
                    image.uploaded_by = request.user
                    image.save()
                    images_count += 1
            
            messages.success(request, f'Gallery "{gallery.title}" created with {images_count} images!')
            return redirect('gallery_detail', slug=gallery.slug)
    else:
        # Pre-fill partner if coming from partner page
        initial_data = {}
        if partner_id:
            partner = get_object_or_404(Partner, id=partner_id)
            initial_data['partner'] = partner
        
        gallery_form = GalleryForm(initial=initial_data)
        image_formset = ImageFormSet(queryset=GalleryImage.objects.none())
    
    context = {
        'gallery_form': gallery_form,
        'image_formset': image_formset,
    }
    return render(request, 'gallery_upload.html', context)



def newsletters(request):
    """View to list all published newsletters"""
    newsletters_list = Newsletter.objects.filter(is_published=True)
    context = {
        'newsletters': newsletters_list,
        'title': 'Newsletters',
        'page': 'newsletters',
    }
    return render(request, 'newsletter_archive.html', context)


def newsletter_download(request, slug):
    """View to handle newsletter downloads and increment counter"""
    newsletter = get_object_or_404(Newsletter, slug=slug, is_published=True)
    newsletter.increment_downloads()
    
    response = FileResponse(newsletter.file.open('rb'), as_attachment=True, filename=newsletter.file.name.split('/')[-1])
    return response
