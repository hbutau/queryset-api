import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "querysets.settings")
import django
django.setup()

from blog.models import Entry, Blog

if __name__ == '__main__':
    b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    b.save()

    for e in Entry.objects.all():
        print(e.headline)


