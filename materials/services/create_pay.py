import os
import stripe


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def get_payment_link(payment):

    if payment.course:
        title = payment.course.title
        description = payment.course.description
    else:
        title = payment.lesson.title
        description = payment.lesson.description

    product = stripe.Product.create(
        name=title,
        description=description,
    )

    price = stripe.Price.create(
        unit_amount=int(f"{str(payment.amount)}" + "00"),
        currency="usd",
        product=product["id"],
    )

    payment = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price["id"],
                "quantity": 1,
            },
        ],
        mode="payment",
    )

    return payment["url"]
