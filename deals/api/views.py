import csv
import io
from django.db.models import Sum
from django.db.models.query import QuerySet
from items.models import Item
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import DealSerializer, UploadSerializer, TopFiveSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class UploadView(generics.CreateAPIView):
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        errors = []
        is_error = False
        csv_file = request.FILES.get('deals')
        try:
            data_set = csv_file.read().decode('UTF-8')
        except UnicodeDecodeError:
            return Response('Status: Error, Desc: <Файл не верного формата> - в процессе '
                            'обработки файла произошла ошибка.', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except AttributeError:
            return Response('Status: Error, Desc: <Файл отсутствует> - в процессе '
                            'обработки файла произошла ошибка.', status=status.HTTP_400_BAD_REQUEST)
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                User.objects.get_or_create(username=column[0])
                Item.objects.get_or_create(name=column[1])
                data = {'customer': User.objects.get(username=column[0]).pk,
                        'item': Item.objects.get(name=column[1]).pk,
                        'total': column[2],
                        'quantity': column[3],
                        'date': column[4]}
            except IndexError:
                is_error = True
                errors.append(column)
                continue
            serializer = DealSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        if is_error:
            return Response(f'Status: Error, Desc: <Следующие строки не были обработаны из за ошибок в них:{errors}> - '
                            'в процессе обработки файла произошла ошибка.', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response('Status: OK - файл был обработан без ошибок', status=status.HTTP_200_OK)


class TopFiveView(generics.ListAPIView):
    serializer_class = TopFiveSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        sorted_customers = User.objects.annotate(total_spent=Sum('deal__total')).order_by('-total_spent')
        data = list()
        if sorted_customers.count() > 5:
            top_customers = sorted_customers.exclude(total_spent__lte=sorted_customers[6].total_spent)  # 6 for postgres
        else:
            top_customers = sorted_customers

        for customer in top_customers:
            others_in_top = top_customers.exclude(username=customer.username)
            gems = Item.objects.filter(id__in=customer.deal_set.values('item')).distinct()
            popular_gems = gems.filter(deal__customer__in=others_in_top)
            info = {
                "username": customer.username,
                "spent_money": customer.total_spent,
                "gems": popular_gems
            }
            data.append(info)
        queryset = data

        if isinstance(queryset, QuerySet):  # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
