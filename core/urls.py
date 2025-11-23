from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('partners/', views.partners_view, name='partners'),
    path('partners/zimbabwe/', views.partners_zimbabwe, name='partners_zimbabwe'),
    path('partners/southafrica/', views.partners_southafrica, name='partners_southafrica'),
    path('events/', views.events_view, name='events'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('join/', views.join, name='join'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('testimonials/submit/', views.submit_testimonial, name='submit_testimonial'),
    # Gallery URLs
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),
    path('gallery/upload/<int:partner_id>/', views.gallery_upload, name='gallery_upload_partner'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    
    # Newsletter URLs
    path('newsletters/', views.newsletters, name='newsletters'),
    path('newsletters/download/<slug:slug>/', views.newsletter_download, name='newsletter_download'),
]
