from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Category
from decimal import Decimal
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import JsonResponse

def dish_list(request):
    qs = Dish.objects.select_related('category').all().order_by('name')
    categories = Category.objects.all()

    
    category = request.GET.get('category')
    spiciness_min = request.GET.get('sp_min')
    spiciness_max = request.GET.get('sp_max')
    has_nuts = request.GET.get('has_nuts')
    vegetarian = request.GET.get('vegetarian')
    q = request.GET.get('q')

    if category and category != 'All':
        qs = qs.filter(category__name=category)
    if spiciness_min:
        try:
            qs = qs.filter(spiciness__gte=int(spiciness_min))
        except ValueError:
            pass
    if spiciness_max:
        try:
            qs = qs.filter(spiciness__lte=int(spiciness_max))
        except ValueError:
            pass
    if has_nuts == 'on':
        qs = qs.filter(has_nuts=True)
    if vegetarian == 'on':
        qs = qs.filter(vegetarian=True)
    if q:
        qs = qs.filter(name__icontains=q)

    
    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    dishes = paginator.get_page(page)

    context = {
        'dishes': dishes,
        'categories': categories,
        'selected_category': category or 'All',
       
        'sp_min': spiciness_min,
        'sp_max': spiciness_max,
        'has_nuts': has_nuts,
        'vegetarian': vegetarian,
        'q': q,
    }
    return render(request, 'menu/dish_list.html', context)


def _get_cart(request):
    return request.session.setdefault('cart', {})

@require_POST
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    cart = _get_cart(request)
    str_id = str(dish_id)
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        cart[str_id] = {
            'name': dish.name,
            'price': str(dish.price),
            'quantity': 1,
        }
    request.session.modified = True
   
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({'status': 'ok', 'cart_size': sum(i['quantity'] for i in cart.values())})
    return redirect(request.META.get('HTTP_REFERER', reverse('menu:dish_list')))

 

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0.00')
    for dish_id, data in cart.items():
        price = Decimal(data['price'])
        qty = int(data['quantity'])
        subtotal = price * qty
        items.append({
            'dish_id': int(dish_id),
            'name': data['name'],
            'price': price,
            'quantity': qty,
            'subtotal': subtotal,
        })
        total += subtotal
    context = {'items': items, 'total': total}
    return render(request, 'menu/cart_detail.html', context)

@require_POST
def cart_update(request, dish_id):
    cart = _get_cart(request)
    str_id = str(dish_id)
    qty = request.POST.get('quantity')
    try:
        qty = int(qty)
        if qty <= 0:
            cart.pop(str_id, None)
        else:
            if str_id in cart:
                cart[str_id]['quantity'] = qty
    except (ValueError, TypeError):
        pass
    request.session.modified = True
    return redirect('menu:cart_detail')

@require_POST
def cart_remove(request, dish_id):
    cart = _get_cart(request)
    cart.pop(str(dish_id), None)
    request.session.modified = True
    return redirect('menu:cart_detail')
