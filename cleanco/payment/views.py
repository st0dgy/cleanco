from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from django.http import HttpRequest, HttpResponse
from cart.cart import Cart
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings


def checkout(request):
    # users with accounts (pre-fill the form)
    if request.user.is_authenticated:
        try:
            # authenticated users with shipment info
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {"shipping": shipping_address}
            return render(request, "payment/checkout.html", context=context)
        except:
            # authenticated users with no shipment info

            return render(request, "payment/checkout.html")
    else:
        # guest user
        return render(request, "payment/checkout.html")


def complete_order(request):
    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        delivery_option = request.POST.get("delivery_option")
        payment_option = request.POST.get("payment_option")
        state = request.POST.get("state")
        city = request.POST.get("city")
        warehouse_number = request.POST.get("warehouse_number")
        # all-in-one shipping address
        shipping_address = (
            "Номер телефону: "
            + phone
            + "\n"
            + "Служба доставки: "
            + delivery_option
            + "\n"
            + "Область: "
            + state
            + "\n"
            + "Населений пункт: "
            + city
            + "\n"
            + "№ Відділення: "
            + warehouse_number
            + "\n"
            "Тип оплати: " + payment_option
        )
        # shopping cart info
        cart = Cart(request)
        total_cost = cart.get_total()

        """
        Order variations
        1) Create order -> account users with/without shipping info
        2) Create order -> guest users
        
        """
        # 1)
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user,
            )

            order_id = order.pk
            product_list = []
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                    user=request.user,
                )
                product_list.append(item["product"])

            all_products = product_list
            # email order
            send_mail(
                "Замовлення отримано",
                str(name) + ", " + "\n\n" + "Ми отримали Ваше замовлення!" + "\n\n"
                "Будь ласка, перегляньте його:"
                + "\n\n"
                + str(all_products)
                + "\n\n"
                + "Сума: ₴"
                + str(cart.get_total()),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        # 2)
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
            )

            order_id = order.pk
            product_list = []
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                )
                product_list.append(item["product"])

            all_products = product_list

        # email order
        send_mail(
            "Замовлення отримано",
            "Дякую," + "\n\n" + "ми отримали Ваше замовлення!" + "\n\n"
            "Будь ласка, перегляньте його:"
            + "\n\n"
            + str(all_products)
            + "\n\n"
            + "Сума: ₴"
            + str(cart.get_total()),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        order_success = True
        response = JsonResponse({"success": order_success})

        return response


def payment_success(request):
    # clearing shopping cart after completing order
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    return render(request, "payment/payment-success.html")


def payment_failed(request):
    return render(request, "payment/payment-failed.html")
