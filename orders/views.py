from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import PurchaseOrder, SalesOrder
from .forms import (
    PurchaseOrderForm,
    PurchaseOrderItemFormSet,
    SalesOrderForm,
    SalesOrderItemFormSet,
)


# ── Purchase Orders ──────────────────────────────────────────────

@login_required
def po_list(request):
    """List all purchase orders."""
    orders = PurchaseOrder.objects.select_related("supplier", "created_by").order_by("-created_at")
    return render(request, "orders/po_list.html", {"orders": orders})


@login_required
def po_detail(request, pk):
    """View a single purchase order with its items."""
    qs = PurchaseOrder.objects.select_related(
        "supplier", "created_by"
    ).prefetch_related("items__product")
    order = get_object_or_404(qs, pk=pk)
    return render(request, "orders/po_detail.html", {"order": order})


@login_required
def po_create(request):
    """Create a new purchase order with line items."""
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, f"Purchase Order #{order.pk} created.")
            return redirect("orders:po_detail", pk=order.pk)
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
    return render(request, "orders/po_form.html", {"form": form, "formset": formset, "title": "New Purchase Order"})


@login_required
def po_update(request, pk):
    """Update an existing purchase order."""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST, instance=order)
        formset = PurchaseOrderItemFormSet(
            request.POST, instance=order
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Purchase Order #{order.pk} updated.")
            return redirect("orders:po_detail", pk=order.pk)
    else:
        form = PurchaseOrderForm(instance=order)
        formset = PurchaseOrderItemFormSet(instance=order)
    ctx = {
        "form": form, "formset": formset,
        "title": "Edit Purchase Order", "order": order,
    }
    return render(request, "orders/po_form.html", ctx)


@login_required
def po_delete(request, pk):
    """Delete a purchase order."""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, f"Purchase Order #{pk} deleted.")
        return redirect("orders:po_list")
    return render(request, "orders/po_confirm_delete.html", {"order": order})


# ── Sales Orders ─────────────────────────────────────────────────

@login_required
def so_list(request):
    """List all sales orders."""
    orders = SalesOrder.objects.select_related("customer", "created_by").order_by("-created_at")
    return render(request, "orders/so_list.html", {"orders": orders})


@login_required
def so_detail(request, pk):
    """View a single sales order with its items."""
    qs = SalesOrder.objects.select_related(
        "customer", "created_by"
    ).prefetch_related("items__product")
    order = get_object_or_404(qs, pk=pk)
    return render(request, "orders/so_detail.html", {"order": order})


@login_required
def so_create(request):
    """Create a new sales order with line items."""
    if request.method == "POST":
        form = SalesOrderForm(request.POST)
        formset = SalesOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, f"Sales Order #{order.pk} created.")
            return redirect("orders:so_detail", pk=order.pk)
    else:
        form = SalesOrderForm()
        formset = SalesOrderItemFormSet()
    return render(request, "orders/so_form.html", {"form": form, "formset": formset, "title": "New Sales Order"})


@login_required
def so_update(request, pk):
    """Update an existing sales order."""
    order = get_object_or_404(SalesOrder, pk=pk)
    if request.method == "POST":
        form = SalesOrderForm(request.POST, instance=order)
        formset = SalesOrderItemFormSet(
            request.POST, instance=order
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Sales Order #{order.pk} updated.")
            return redirect("orders:so_detail", pk=order.pk)
    else:
        form = SalesOrderForm(instance=order)
        formset = SalesOrderItemFormSet(instance=order)
    ctx = {
        "form": form, "formset": formset,
        "title": "Edit Sales Order", "order": order,
    }
    return render(request, "orders/so_form.html", ctx)


@login_required
def so_delete(request, pk):
    """Delete a sales order."""
    order = get_object_or_404(SalesOrder, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, f"Sales Order #{pk} deleted.")
        return redirect("orders:so_list")
    return render(request, "orders/so_confirm_delete.html", {"order": order})
