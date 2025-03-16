import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


class PaymentStripe:
    """ Класс для работы со stripe (система оплаты он-лайн) """

    @staticmethod
    def create_stripe_product(product):
        """  Создает продукт для оплаты в stripe """
        stripe_product = stripe.Product.create(name=product)
        return stripe_product.get('id')

    @staticmethod
    def create_stripe_price(product_id, amount):
        """ Создает цену в stripe """

        price = stripe.Price.create(
            currency="rub",
            unit_amount=amount * 100,
            product=product_id,
        )
        return price

    @staticmethod
    def create_stripe_session(price):
        """ Создает сессию на оплату в stripe """
        session = stripe.checkout.Session.create(
            success_url="https://127.0.0.1:8000/",
            line_items=[{"price": price.get("id"), "quantity": 1}],
            mode="payment",
        )
        return session.get("id"), session.get("url")
