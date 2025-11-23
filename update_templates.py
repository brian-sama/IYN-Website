"""
Django Template Batch Updater
Automatically updates HTML templates with Django template tags
"""

import os
import re

TEMPLATES_DIR = r"c:\Users\Mlungisi Moyo\3D Objects\IYN Website\backend\templates"

# Files already updated
SKIP_FILES = ['index.html', 'about.html']

# URL mapping for Django URL tags
URL_MAPPING = {
    'index.html': 'index',
    'about.html': 'about',
    'programs.html': 'programs',
    'partners.html': 'partners',
    'events.html': 'events',
    'testimonials.html': 'testimonials',
    'contact.html': 'contact',
    'join.html': 'join',
}

def update_template(filepath):
    """Update a single template file with Django tags"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has {% load static %}
    if '{% load static %}' in content:
        print(f"✓ {os.path.basename(filepath)} already updated")
        return False
    
    # Add {% load static %} at the top
    content = '{% load static %}\n' + content
    
    # Update image paths
    content = re.sub(
        r'src="images/([^"]+)"',
        r"src=\"{% static 'images/\1' %}\"",
        content
    )
    
    # Update navigation links
    for html_file, url_name in URL_MAPPING.items():
        # Update href with class
        content = re.sub(
            rf'href="{html_file}"(\s+class="[^"]*")',
            rf'href="{{% url \'{url_name}\' %}}"\1',
            content
        )
        # Update href without class
        content = re.sub(
            rf'href="{html_file}"',
            rf'href="{{% url \'{url_name}\' %}}"',
            content
        )
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {os.path.basename(filepath)}")
    return True

def main():
    """Update all templates"""
    print("Django Template Batch Updater")
    print("=" * 50)
    
    updated_count = 0
    
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith('.html') and filename not in SKIP_FILES:
            filepath = os.path.join(TEMPLATES_DIR, filename)
            if update_template(filepath):
                updated_count += 1
    
    print("=" * 50)
    print(f"✓ Updated {updated_count} templates")
    print("\nManual steps still needed:")
    print("1. Add {% csrf_token %} to forms in contact.html and join.html")
    print("2. Test all pages after running the server")

if __name__ == '__main__':
    main()
