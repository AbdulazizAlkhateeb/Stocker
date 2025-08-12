from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Product, Category, Supplier
from django.db.models import Q, F, Count, Avg, Sum, Max, Min
from .forms import ProductForm

# Create your views here.


def product_list_view(request:HttpRequest):
    base = Product.objects.select_related("category").prefetch_related("suppliers")
    selected_category = request.GET.get("category")
    products = base.filter(category_id=selected_category) if selected_category else base

    search = (request.GET.get("search") or "").strip()
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(suppliers__supplier_name__icontains=search)
        ).distinct()

    return render(request, "management/products_list.html", { "products": products, "categories": Category.objects.order_by("category_name"), "selected_category": selected_category, "search": search,})




def product_create_view(request: HttpRequest):
    if not (request.user.is_staff and request.user.has_perm("management.add_product")):
        messages.warning(request, "You don't have permission to add product", "alert-warning")
        return redirect("management:product_list")

    product_form = ProductForm()

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Created Product Successfully", "alert-success")
            return redirect("management:product_list")
        else:
            print("not valid form", product_form.errors)

    return render(request, "management/product_create.html", {"product_form": product_form, "categories": categories, "suppliers": suppliers,},
)

def product_update_view(request: HttpRequest):
    pass




def product_delete_view(request: HttpRequest, product_id: int):

    if not (request.user.is_staff and request.user.has_perm("management.delete_product")):
        messages.warning(request, "only staff can delete product", "alert-warning")
        return redirect("management:product_list")

    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Deleted product successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete product", "alert-danger")

    return redirect("management:product_list")




def dashboard_view(request:HttpRequest):
    return render(request, 'management/dashboard.html')




