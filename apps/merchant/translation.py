from modeltranslation.translator import register, TranslationOptions
from .models import Order, OrderItem


@register(OrderItem)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('order__product__desc',)