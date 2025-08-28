from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        customer = order.customer
        
        subject = f'New Order Confirmation: {order.item}'
        message = f'''
        Hello {customer.name},
        
        Thank you for your order!
        
        Order Details:
        - Item: {order.item}
        - Amount: ${order.amount}
        - Time: {order.time}
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [customer.email],
            fail_silently=False,
        )


        
        
        return f"Email sent to {customer.email} for order {order_id}"
    except Order.DoesNotExist:
        return f"Order {order_id} does not exist"