import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.db import models
from django.contrib.auth.models import User

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.city}, {self.state}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_payment")
    razorpay_order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"Payment for Order {self.order.id}"

class PaymentAttempt(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20)
    failure_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Payment Attempt for Payment {self.payment.id}"

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.order.id}"

@login_required
def create_razorpay_order(request, order_id):
    """Create a Razorpay order and render the checkout page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Ensure an address is already selected
    if not order.address:
        return redirect('select_address_for_order', order_id=order.id)

    # Create a Razorpay Order
    razorpay_order_data = {
        "amount": int(order.total_amount * 100),  # Convert to paisa
        "currency": "INR",
        "receipt": f"order_rcpt_{order.id}",
        "payment_capture": 1,
    }
    razorpay_order = client.order.create(data=razorpay_order_data)

    # Save Razorpay order details in the Payment model
    payment, created = Payment.objects.update_or_create(
        order=order,
        defaults={
            "razorpay_order_id": razorpay_order["id"],
            "status": "PENDING",
        }
    )

    # Pass Razorpay and order details to the template
    context = {
        "order": order,
        "razorpay_order": razorpay_order,
        "key_id": settings.RAZORPAY_KEY_ID,
        "addresses": Address.objects.filter(user=request.user),
    }
    return render(request, "checkout.html", context)

@csrf_exempt
def payment_success(request):
    """Handle the Razorpay payment success callback."""
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    try:
        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })

        # Fetch the payment and order
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        order = payment.order

        # Update Payment Attempt
        PaymentAttempt.objects.create(
            payment=payment,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            status="SUCCESS",
        )

        # Mark Payment and Order as Completed
        payment.status = "COMPLETED"
        payment.save()
        order.status = "COMPLETED"
        order.save()

        return render(request, "success.html", {"order": order})

    except razorpay.errors.SignatureVerificationError:
        # Fetch the payment and order
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        PaymentAttempt.objects.create(
            payment=payment,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            status="FAILED",
            failure_reason="Signature verification failed",
        )

        payment.status = "FAILED"
        payment.save()
        return render(request, "failure.html", {"error": "Payment verification failed!"})

@csrf_exempt
def payment_failure(request):
    """Handle payment failure callback."""
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id", None)
    failure_reason = request.POST.get("error_description", "Unknown error")

    # Fetch the payment and order
    payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)

    # Record the failed payment attempt
    PaymentAttempt.objects.create(
        payment=payment,
        razorpay_payment_id=razorpay_payment_id,
        status="FAILED",
        failure_reason=failure_reason,
    )

    payment.status = "FAILED"
    payment.save()

    return render(request, "failure.html", {"error": failure_reason})

