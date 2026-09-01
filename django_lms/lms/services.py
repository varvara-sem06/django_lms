import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    return stripe.Product.create(
        name=course.title,
    )


def create_stripe_price(product, course):
    return stripe.Price.create(
        product=product.id,
        unit_amount=int(course.price * 100),
        currency="usd",
    )


def create_checkout_session(price):
    return stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
        success_url="http://127.0.0.1:8000/payment/success/",
        cancel_url="http://127.0.0.1:8000/payment/cancel/",
    )


def retrieve_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)
