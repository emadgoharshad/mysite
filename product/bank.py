import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from product.models import Cart, Order
from product.models import Payment

def go_to_gateway(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += (item.product.price) * item.quantity

    amount = total_price
    phone_number = '989112221234'

    factory = bankfactories.BankFactory()

    try:
       bank = factory.create()

       bank.set_request(request)
       bank.set_amount(amount)

       bank.set_client_callback_url('/callback-gateway')
       bank.set_mobile_number(phone_number)

       bank_record = bank.ready()


       return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        raise e

def callback_gateway_view(request):
    user=request.user

    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM,None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست")
        raise Http404

    try:
       bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست")

    new_payment = Payment()
    new_payment.user = user
    new_payment.payment_number = bank_record.tracking_code
    new_payment.payment_method = bank_record.bank_type
    new_payment.amount_paid = bank_record.amount
    new_payment.status = bank_record.staus
    new_payment.save()

    if bank_record.is_success:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0
        for item in cart_items:
            total_price += (item.product.price) * item.quantity

        cart = Cart.objects.filter(user=user)
        p = []
        for item in cart:
            p += item.product,item.quantity


        new_order = Order()
        new_order.user = user
        new_order.payment = new_payment
        new_order.total_price = total_price
        new_order.tracking_code = bank_record.tracking_code
        new_order.product,new_order.quantity = p
        new_order.save()

        Cart.objects.filter(user=user).delete()

        return HttpResponse("پرداخت با موفقیت انجام شد.")

    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")





















