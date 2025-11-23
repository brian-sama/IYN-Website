from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactSubmission, NewsletterSubscriber, Testimonial, UserProfile, Gallery, GalleryImage, JoinSubmission


class ContactForm(forms.ModelForm):
    """Form for contact submissions"""
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (optional)'}),
        }


class JoinSubmissionForm(forms.ModelForm):
    """Form for Join Us submissions"""
    class Meta:
        model = JoinSubmission
        fields = ['full_name', 'email', 'country', 'area_of_interest', 'phone', 'organization', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your country'}),
            'area_of_interest': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Leadership, Entrepreneurship, Arts'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization (optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us more about your interests... (optional)', 'rows': 4}),
        }


class TestimonialSubmissionForm(forms.ModelForm):
    """Form for submitting testimonials"""
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'country', 'photo', 'content', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Role/Position'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share your experience...', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }


class UserRegistrationForm(UserCreationForm):
    """Extended user registration form"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class UserProfileForm(forms.ModelForm):
    """Form for user profile information"""
    class Meta:
        model = UserProfile
        fields = ['country', 'bio', 'photo', 'phone', 'organization', 'role', 'is_delegate']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself...', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Role'}),
            'is_delegate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GalleryForm(forms.ModelForm):
    """Form for creating/editing galleries"""
    class Meta:
        model = Gallery
        fields = ['title', 'slug', 'description', 'partner', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gallery Title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL-friendly slug (e.g., youth-summit-2025)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe this gallery...', 'rows': 4}),
            'partner': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'partner': 'Leave blank for general IYN Activities gallery',
            'is_public': 'Uncheck to make this gallery visible only to logged-in users',
        }


class GalleryImageForm(forms.ModelForm):
    """Form for uploading images to a gallery"""
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image caption (optional)'}),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be less than 10MB.')
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('Only image files are allowed.')
        return image

