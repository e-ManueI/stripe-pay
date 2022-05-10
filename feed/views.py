import stripe
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Price, Product
from django.conf import settings
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = "http://127.0.0.1:8000" #changed in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': price.stripe_price_id,
                    'quantity': 1, 
                }, 
            ],
            mode = 'payment',
            success_url = YOUR_DOMAIN + '/success/', 
            cancel_url = YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)
        # return JsonResponse({
        #     'id': checkout_session.id
            
        # }
        # )
class SuccessView(TemplateView):
    template_name = "success.html"
    
class CancelView(TemplateView):
    template_name = "cancel.html"

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"
    
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context
    
# webhook handler
@csrf_exempt
def stripe_webhook(request):
    payload = request.body.decode('utf-8')
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        #Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        #Invalid signature
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        
        # Fulfill the purchase...
        fulfill_order(session)
    
    print(payload)
    #passed signature verification
    return HttpResponse(status=200)

def fulfill_order(session):
    print("fulfilling order")