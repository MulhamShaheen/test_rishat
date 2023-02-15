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
        currency=item.currency,
        product=product['id'],
    )
    try:
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        #             'price': product_price.id,
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url= 'http://127.0.0.1:8000/success.html',
        #     cancel_url= 'http://127.0.0.1:8000/cancel.html',
         intent = stripe.PaymentIntent.create(
            amount=int(product_price.unit_amount),
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
    except Exception as e:
        return Response(str(e))

    data = ItemSerializer(item).data

    return Response({
        "product_id": product.id,
        "price_id": product_price.id,
        "price_amount": product_price.unit_amount,
        "id": intent.id,
        "client_secret": intent.client_secret

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


@api_view(['GET'])
def get_order(request, id):
    stripe.api_key = "sk_test_51MaMuTCFuR6MvWxzdid0qSRP9tUj8MzFTSS6KUWoL95OKNKc9JLbMxowkRAd1MWjxkl4WS7vPo8nTDzm5qIC4UuW0062hUoymX"
    order = models.Order.objects.get(id=id)
    
    stipe_order = stripe.Product.create(
            name=str(order),
            description=order.get_description(),
        )

    order_price = stripe.Price.create(
        unit_amount=int(order.get_prices_sum()),
        currency="usd",
        product=stipe_order['id'],
    )
    try:
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        #             'price': order_price.id,
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url= 'http://127.0.0.1:8000/success.html',
        #     cancel_url= 'http://127.0.0.1:8000/cancel.html',
        # )
        
        intent = stripe.PaymentIntent.create(
            amount=int(order.get_prices_sum()),
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        
    except Exception as e:
        return Response(str(e))
    
    return Response({
        "product_id": order.id,
        "price_id": order_price.id,
        "price_amount": order_price.unit_amount,
        "id": intent.id,
        "client_secret": intent.client_secret
        
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

    return Response(data)
