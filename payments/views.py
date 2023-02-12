from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from .serializers import *
import stripe

@api_view(['GET'])
def get_buy(request, id):
    stripe.api_key = "sk_test_51MaMuTCFuR6MvWxzdid0qSRP9tUj8MzFTSS6KUWoL95OKNKc9JLbMxowkRAd1MWjxkl4WS7vPo8nTDzm5qIC4UuW0062hUoymX"
    item = models.Item.objects.get(id=id)

    search_res = stripe.Product.search(
        query=f"name~'{item.name}' AND description~'{item.description}'"
    )

    if(search_res.data):
        product = search_res.data[0]

    else:
        product = stripe.Product.create(
            name=item.name,
            description=item.description,
        )

    product_price = stripe.Price.create(
        unit_amount=int(item.price),
        currency="usd",
        product=product['id'],
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product_price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= 'http://127.0.0.1:8000/success.html',
            cancel_url= 'http://127.0.0.1:8000/cancel.html',
        )
    except Exception as e:
        return Response(str(e))

    data = ItemSerializer(item).data

    return Response({
        "product_id": product.id,
        "price_id": product_price.id,
        "price_amount": product_price.unit_amount,
        "id": checkout_session.id,

    })


def get_item(request, id):
    
    try:
        item = models.Item.objects.get(id=id)
        
    except Item.DoesNotExist:
        raise Http404("No item matches the given id.")

    return render(request, 'payments/index.html', {
        "item_id": item.id,
        "name": item.name,
        "description": item.description
    })

@api_view(['POST'])
def post_test(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@api_view(['GET'])
def get_test(request):
    items = models.Item.objects.all()
    data = ItemSerializer(items, many=True).data

    return Response(data)\
