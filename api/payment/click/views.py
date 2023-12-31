import hashlib

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from payments import PaymentStatus
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsClient
from common.order.models import Checkout, Order
from common.payment.click import utils
from common.payment.click.models import Payment
from common.payment.payme.models import Payment
from common.payment.payme.models import PaymentType
from config.settings.base import env


@csrf_exempt
def prepare(request):
    return utils.prepare(request)


@csrf_exempt
def complete(request):
    return utils.complete(request)


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def paymentLoad(id):
    return Payment.objects.get(id=id)


def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    return secret_key


class PaymentClick(APIView):
    # permission_classes = [IsClient]

    def get(self, request):
        checkout = Checkout.objects.filter(user=request.user).last()
        # payment = Payment.objects.create(user_id=request.user.id,
        #                                  total=checkout.amount,
        #                                  description="o'qish uchun to'lov",
        #                                  billing_first_name=request.user.first_name,
        #                                  billing_last_name=request.user.last_name,
        #                                  billing_address_1="Toshkent",
        #                                  billing_address_2='Toshkent',
        #                                  billing_city='Tashkent',
        #                                  billing_postcode='1000000',
        #                                  billing_country_code='47',
        #                                  billing_country_area='Asia',
        #                                  billing_email=request.user.email)

        payment = Payment.objects.create(user=request.user,
                                         amount=checkout.amount,
                                         paymentType=PaymentType.CLICK)
        context = {
            'merchant_id': env('CLICK_MERCHANT_ID'),
            'service_id': env('CLICK_SERVICE_ID'),
            'amount': payment.amount,
            'transaction_param': payment.id,
            'return_url': 'https://api.kale.uz/payment-click-complete/',
        }
        return Response(context, status=status.HTTP_200_OK)


class PaymentPrepareAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        paymentID = request.data.get('merchant_trans_id', None)
        result = self.click_webhook_errors(request)
        payment = paymentLoad(paymentID)
        if result['error'] == '0':
            payment.status = PaymentStatus.WAITING
            payment.save()
        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_trans_id', None)
        return Response(result, status=status.HTTP_200_OK)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        click_paydoc_id = request.data.get('click_paydoc_id', None)
        paymentID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        error_note = request.data.get('error_note', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), paymentID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        payment = paymentLoad(paymentID)
        if not payment:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(amount) - float(payment.amount) > 0.01):
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if paymentID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if payment.status == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }


class PaymentCompleteAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):

        paymentID = request.data.get('merchant_trans_id', None)
        payment = paymentLoad(paymentID)
        result = self.click_webhook_errors(request)
        if request.data.get('error', None) != None and int(request.data.get('error', None)) < 0:
            payment.status = PaymentStatus.REJECTED
            payment.save()
        if result['error'] == '0':
            payment.status = PaymentStatus.CONFIRMED
            payment.save()

            checkout = Checkout.objects.filter(user=payment.user).first()
            if checkout.isDelivery:
                orders = [
                    Order(checkout=checkout,
                          product=i.product,
                          quantity=i.quantity,
                          totalAmount=i.amount
                          ) for i in checkout.products.select_related('cart', 'product').all()
                ]
            else:
                orders = [
                    Order(checkout=checkout,
                          product=i.product,
                          quantity=i.quantity,
                          totalAmount=i.amount
                          ) for i in checkout.products.select_related('cart', 'product').all()
                ]
            orders = Order.objects.bulk_create(orders)
            payment.orders.set(orders)
            payment.save()

            # REMOVE CART PRODUCTS FROM CHECKOUT
            for i in checkout.products.select_related('cart', 'product').all():
                i.delete()
        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_prepare_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_prepare_id', None)
        return Response(result)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        click_paydoc_id = request.data.get('click_paydoc_id', None)
        paymentID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        error_note = request.data.get('error_note', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), paymentID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        payment = paymentLoad(paymentID)
        if not payment:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(amount) - float(payment.amount) > 0.01):
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if paymentID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if payment.status == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }


class PaymentComplete(APIView):

    def get(self, request):
        return Response({'Success': True}, status=status.HTTP_200_OK)
