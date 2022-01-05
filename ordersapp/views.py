from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404

from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Список заказов'

    def get_queryset(self):
        return Order.objects.filter(is_active=True, user=self.request.user)


class CreateOrderView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = 'Geekshop | Создание заказа'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=basket_item.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                # basket_item.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(CreateOrderView, self).form_valid(form)


class DetailOrderView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Просмотр заказа'


class UpdateOrderView(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = 'Geekshop | Создание заказа'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(UpdateOrderView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(UpdateOrderView, self).form_valid(form)


class DeleteOrderView(DeleteView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Удаление заказа'
    success_url = reverse_lazy('orders:list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:list'))
