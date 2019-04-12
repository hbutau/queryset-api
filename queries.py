import datetime
import os
from collections import OrderedDict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "querysets.settings")
import django
import pytest
django.setup()

from django.db.models import Count
from django.db.models import Q

from blog.models import Entry, Blog, Author
from pizza.models import Topping, Pizza, Restaurant, Topping


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
    # print(Author.objects.values_list('name', flat=True).get(pk=1))


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



    # prefetch_related(*lookups) => similar to above but not for many_to_one and One_to_one
    # returns a qs that witll automatically retrieve in a single batch related obs of the specified lkp
    print(Pizza.objects.all())
    print(Pizza.objects.all().prefetch_related('toppings'))

    print(Restaurant.objects.select_related('best_pizza').prefetch_related('best_pizza__toppings'))

    from django.db.models import Prefetch
    # using prefetch object to control prefetch operation
    print(Restaurant.objects.prefetch_related(Prefetch('pizzas__toppings')))


    # Providing a custom qs with the optional queryset arg => to change default ordering
    print(Restaurant.objects.prefetch_related(Prefetch('pizzas__toppings', queryset=Topping.objects.order_by('name'))))

    # Or even call select_related() to reduce the number of queries
    print(Pizza.objects.prefetch_related(Prefetch('restaurants', queryset=Restaurant.objects.select_related('best_pizza'))))


    # passing the prefetched result to a custom attr using => to_attr => []
    vegetarian_pizzas = Pizza.objects.filter(restaurants=True)
    print(Restaurant.objects.prefetch_related(
        Prefetch('pizzas', to_attr='menu'),
        Prefetch('pizzas', queryset=vegetarian_pizzas,
        to_attr='vegetarian_menu'),
        'vegetarian_menu__toppings'))


    # lkups created with custom to_attr can be used by other lookups
    print(Restaurant.objects.prefetch_related(Prefetch('pizzas', queryset=vegetarian_pizzas, to_attr='vegetarian_menu'), 'vegetarian_menu__toppings'))


    # Filtering down the prefetch results with to_attr
    queryset = Pizza.objects.filter(restaurants=True)
    restaurants = Restaurant.objects.prefetch_related(Prefetch('pizzas', queryset=queryset, to_attr='vegetarian_pizzas'))
    vegetarian_pizzas = restaurants[0].vegetarian_pizzas


   # extra(select=None, where=None, params=None,tables=None,order_by=None,select_param_None) => hook for injecting specific clauses into SQL generated by QuerySet
    print(Author.objects.extra(where={"email='lois@gmail.com'"}))


    # using select to add more to SELECT sql clause
    print(Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"}))

    print(Blog.objects.extra(select={'entry_count': 'SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id'},))

    # using select_params
    print(Blog.objects.extra(select=OrderedDict([('a', '%s'), ('b', '%s')]), select_params=('one', 'two')))

    # Using order_by with extra()
    q = Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
    q = q.extra(order_by = ['-is_recent'])
    print(q)


    # Using defer() => pass fields that we dont want to load
    print(Entry.objects.defer("headline"))


    # making multiple calls with defer
    print(Entry.objects.defer("pub_date").filter(rating=5).defer("headline"))


    # defering loading of fields in related models => select_related
    print(Blog.objects.select_related().defer("entry__headline", "entry__pub_date"))


    # more like the opposite of defer(). only(*fiels)
    # using only to defer other fields
    print(Entry.objects.only("rating").only("headline"))

    # Using using(alias) => specifyin which db the QuerySet will be used with
    # print(Entry.objects.using('db.sqlite3'))


    # select_for_update(nowait=False,skip_locked=False,of=0) returns a qs thant locks rows till end of txn
    # from django.db import transaction

    # entries = Entry.objects.select_for_update().filter(author=request.user)
    # with transaction.atomic():
        # for entry in entries:
            # print(entry)


    # raw() => Takes a raw SQL query executes it and returns RawQueryset instance

    # AND

    print(Author.objects.filter(Q(name='Lois Butau') & Q(email='lois@gmail.com')))


   # OR(I) combining 2 Queryset

    print(Author.objects.filter(Q(email='lois@gmail') | Q(email='hbutau@example.com')))


    # get(**kwargs) => returns an obj matchin the lookups given
    print(Author.objects.get(email='lois@gmail.com'))

    # Creating and saving an object in one go with create(**kwargs)
    # me = Author.objects.create(email='me@example.com', name='Me Example')
    print(Author.objects.get(email='me@example.com'))

    # using get_or_create()
    obj, created = Author.objects.get_or_create(
            name='Examplse User',
            email='eg@gmail.com'
            )

    print(obj, created)


    # update_or_create(defaults=None, **kwargs) => for updating an object with given kwargs
    #
    obj, created = Author.objects.update_or_create(
            name='Example User',
            defaults={'name': 'New User'}
            )

    print(obj, created)

    # bulk_create() => inserts the provided list of objs with one query.
    Author.objects.bulk_create([
        Author(name='Bob Marley'),
        Author(name='Rita Marley'),
        ])


    # count() =>returns an interger representing the number of objects in the datatbase matching the QS
    print(Author.objects.filter(name='Humphrey Butau').count())
    print(len(Author.objects.filter(name='Humphrey Butau')))

    # in_bulk(id_list=None, field_name='pk') => takes list of field values and field_name returns dict
    print(Author.objects.in_bulk([1, 2]))


    # latest(*fields) => returns the latest obj in table based on fields
    print(Entry.objects.latest('pub_date'))


    # earliest(*fields) => works like latest bust with change of direction

    # first() => returns first obj matched by the QS
    print(Entry.objects.order_by('authors', 'pub_date').first())

    # aggregate(*args, **kwargs) => returns dict of aggregate values(avs, sums
    print(Blog.objects.aggregate(Count('entry')))
    # controllling the name of of aggregation value by using a **kwarg
    print(Blog.objects.aggregate(number_of_entries=Count('entry')))


    # exists()
    if Author.objects.filter(name='Lois Butau').exists():
        print('Lois is present')


    # update(**kwargs) => performs SQL update query for specified fields and returns number of rows matched
    print(Author.objects.filter(name='Lois Butau').update(name='Linda Butau'))

    # delete() => performs a SQL delete on all rows in QS and returns number of objs deleted
    # print(Author.objects.filter(name='Humphrey Butau').delete())


    # using explain() returns a str of QS execution plan detailing how the db would do the query
    print(Author.objects.filter(name='Linda Butau').explain())


    # exact() => exact match
    print(Author.objects.get(email__exact='lois@gmail.com'))


    # iexact() => case insensitive exact match
    print(Author.objects.get(email__iexact='LOIS@GMAIL.COM'))


    # case senditive containment test
    print(Author.objects.get(email__contains='lois@gmail.com'))

    # case insensitive containment test
    print(Author.objects.get(email__contains='LOIS@GMAIL.COM'))


    # in => in a given iterable
    print(Author.objects.filter(id__in=[1,2,3]))


    # gt greater than
    print(Author.objects.filter(id__gt=1))

    # gte greater than or equal to
    print(Author.objects.filter(id__gte=1))

    # lt  => less than
    print(Author.objects.filter(id__lt=4))


    # lte  => less than or eqaul to
    print(Author.objects.filter(id__lte=4))


    # startswith
    print(Blog.objects.filter(name__startswith='Beat'))


    # endswith => ends with
    print(Blog.objects.filter(name__endswith='log'))

    # iendswith => case nssensitive ends with
    print(Blog.objects.filter(name__iendswith='Log'))


    # range => range test inclusive
    start_date = datetime.date(2019, 4, 10)
    end_date = datetime.date(2005, 4, 11)
    print(Entry.objects.filter(pub_date__range=(start_date, end_date)))


    # date takes a date value
    # Entry.objects.filter(pub_date__date=datetime.date(2019, 4, 11))

    # year
    print(Entry.objects.filter(pub_date__year=2019))

    # month
    print(Entry.objects.filter(pub_date__month=4))


    # day
    print(Entry.objects.filter(pub_date__day=10))

    # week
    print(Entry.objects.filter(pub_date__week=52))


    # week_day
    print(Entry.objects.filter(pub_date__week_day=2))
    print(Entry.objects.filter(pub_date__week_day__gte=2))

    # quarter
    print(Entry.objects.filter(pub_date__quarter=2))

    # time
    # print(Entry.objects.filter(pub_date__time=datetime.time(14, 30)))

    # hour
    # print(Entry.objecs.filter(pub_date__hour__lt=23))

    # isnull => takes either True or False
    print(Entry.objects.filter(pub_date__isnull=True))


    print(Entry.objects.get(headline__regex=r'^(Be?)+'))

    # iregex => case insensitive regex expression
    print(Entry.objects.get(headline__iregex=r'^(bE?)+'))
