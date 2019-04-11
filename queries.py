import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "querysets.settings")
import django
import pytest
django.setup()

from django.db.models import Count

from blog.models import Entry, Blog, Author

if __name__ == '__main__':
    # b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    # b.save()

    for e  in Entry.objects.all():
        print(e.headline)

    entry_list = list(Entry.objects.all())
    print(entry_list)

    print(len(Entry.objects.all()))

    if Entry.objects.filter(headline="London Tour"):
           print("There is at least one Entry with the headline London Tour")

    print(Entry.objects.all()[:2])

    print(repr(Entry.objects.all()))

    # Finding the number of records
    print(Entry.objects.count())

    # Checking for results with exists()
    if Entry.objects.all().filter(headline="London Tour").exists():
        print("The London Tour is present")

    # exclude()- Returns a new Queryset that has objects that dont match the given kwargs
    #
    print(Entry.objects.exclude(headline="London Tour"))

    q = Blog.objects.annotate(Count('entry'))
    print(q)
    # print the name of the first blog
    print(q[0].name)
    # The number of entries on the first blog
    print(q[0].entry__count)


    # order_by()
    print(Entry.objects.all().order_by('rating'))

    print('*****ordering by field in another model*****')
    print(Entry.objects.all().order_by('-blog__id'))

    # Using reverse()
    print(Entry.objects.reverse()[:2])


    # using distinct()
    # print(Author.objects.distinct())

    # not supported on sqlite
    # print(Entry.objects.order_by('pub_date').distinct('pub_date'))


    q = Author.objects.values()
    print('*****selecting the list of dicts*****')
    print(q)
    print('*****selecting the first dict*****')
    print(q[0]) #selects the first dict in in the queryset
    print(Author.objects.values('email'))

    from django.db.models.functions import Lower
    print(Author.objects.values(lower_name=Lower('name')))

    print(Entry.objects.values('blog'))

    print(Entry.objects.values('blog_id'))

    # values_list returns tuple of fields or expressions
    print(Author.objects.values_list('email', 'name'))


    from django.db.models.functions import Lower

    print(Entry.objects.values_list('blog_id', Lower('headline')))

    # passing flat to values_list returns singgle value rather  than a one tuple
    print(Author.objects.values_list('name', flat=True))


    # getting results as a named tuple
    print(Author.objects.values_list('id', 'name', named=True))

    # getting a specific field value og a certain instance values_list >> .get()
    print(Blog.objects.values_list('tagline', flat=True).get(pk=54))
    print(Author.objects.values_list('name', flat=True).get(pk=1))


    # dates(field, kind, order='ASC')
    print(Entry.objects.dates('pub_date', 'year'))
    print(Entry.objects.dates('pub_date', 'month'))
    print(Entry.objects.dates('pub_date', 'week'))
    print(Entry.objects.dates('pub_date', 'day'))
    print(Entry.objects.dates('pub_date', 'day', order='DESC'))
    print(Entry.objects.filter(headline__contains='London').dates('pub_date', 'day'))

    # datetimes(field_name, kind, order='ASC', tzinfo=None)

    # none() ->>> qs that nerver returns andy objects >> no query executed >> instance of EmptyQueryset
    print(Author.objects.none())
    from django.db.models.query import EmptyQuerySet
    print(isinstance(Entry.objects.none(), EmptyQuerySet))

    # all() => a copy of current QuerySet or QuerySet subclass
    print(Author.objects.all())

    # union(*other_qs, all=False)
    qs1 = Entry.objects.values_list('headline')
    qs2 = Entry.objects.values_list('body_text')
    print(qs1.union(qs2).order_by('headline'))


    # intersection(*other_qs)
    print(qs1.intersection(qs2))

    # difference(*other_qs) => EXCEPT keep only elements in the QS but not in some othrQS
    print(qs1.difference(qs2))

    # select_related(*fields) => qs tha will follow FK relationships
    # def test_select_related():
        # assert 'Beatles in Chicage' in Entry.objects.select_related('blog').get(id=4)

    print(Entry.objects.select_related('blog').get(id=4))

    from django.utils import timezone
    blogs = set()

    print(Entry.objects.filter(pub_date__lt=timezone.now()).select_related('blog'))
    print(Entry.objects.select_related('blog').filter(pub_date__lt=timezone.now()))
    # without specifying field also pulls data
    print(Entry.objects.select_related().filter(pub_date__lt=timezone.now()))
