from django.utils import timezone
from datetime import datetime, timedelta
import telebot
from django.shortcuts import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from telebot import types
from decouple import config
from django.core.exceptions import ImproperlyConfigured
from apps.merchant.models import Order
from apps.product.models import SoldProduct
from django.core.exceptions import ObjectDoesNotExist


def get_env_value(env_variable):
    try:
        return config(env_variable)
    except KeyError:
        error_msg = "Set the {} environment variable".format(env_variable)
        raise ImproperlyConfigured(error_msg)


CHANNEL = int(get_env_value("CHANNEL"))
BOT_TOKEN = get_env_value("BOT_TOKEN")
CHANNEL_USERNAME = "@openai_chat_gpt_robot"

bot = telebot.telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

hideBoard = types.ReplyKeyboardRemove()
extra_datas = {}


@csrf_exempt
def index(request):
    if request.method == "GET":
        return HttpResponse("<a href='http://t.me/dkarimoff96'>Created by</>")
    if request.method == "POST":
        bot.process_new_updates(
            [telebot.types.Update.de_json(request.body.decode("utf-8"))]
        )
        return HttpResponse(status=200)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    if message.text == "/start":
        print(message.text)


@bot.callback_query_handler(func=lambda call: call.data.startswith("yes|"))
def handle_callback_query(call):
    order = Order.objects.get(id=int(call.data.split('|')[-1]))
    order.status = "approved"
    order.save()
    text4channel = f"""✅ <b>Buyurtma holati:</b> #<i>{order.get_status_display_value()[-11::].upper()}</i>\n\n 🔢 <b>Buyurtma raqami:</b> <i>{order.id}</i>\n👤 <b>Mijoz ismi:</b> <i>{order.user.full_name}</i>\n📞 <b>Tel raqami:</b> <i>{order.user.phone_number}</i>\n🏠 <b>Manzili:</b> """
    for location in order.user.location.all():
        text4channel += f"{location.address}\n"
    text4channel += '🛒 <b>Mahsulotlar:</b> \n'
    for order_item in order.get_order_items():
        product_details = order.get_product_details(
            order_item, order_item)
        text4channel += f" 🟢 <i>{product_details}</i>\n"
    txtchannel=text4channel+f"📝 <b>Izoh:</b> <i>{order.comment}</i>\n📅 <b>Sana:</b> <i>{order.created.strftime('%Y-%m-%d %H:%M')}</i>\n💸 <b>Jami:</b> <i>{order.total_amount} ₩"
    text4channel += f"📝 <b>Izoh:</b> <i>{order.comment}</i>\n📅 <b>Sana:</b> <i>{order.created.strftime('%Y-%m-%d %H:%M')}</i>\n💸 <b>Jami:</b> <i>{order.total_amount} ₩</i>\n\n⁉️ <u>Buyurtma yuborildimi?</u>"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(
        text="🚚 Yuborildi", callback_data=f"sent|{order.id}")
    markup.add(b1)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id,
        text4channel,
        reply_markup=markup,
    )
    return bot.send_message(
        CHANNEL,
        txtchannel)

@bot.callback_query_handler(func=lambda call: call.data.startswith("no|"))
def handle_callback_query(call):
    order = Order.objects.get(id=int(call.data.split('|')[-1]))
    order.status = "cancelled"
    order.save()
    text4channel = f"""❌ <b>Buyurtma holati:</b> #<i>{order.get_status_display_value()[:5].upper()}</i>\n\n 🔢 <b>Buyurtma raqami:</b> <i>{order.id}</i>\n👤 <b>Mijoz ismi:</b> <i>{order.user.full_name}</i>\n📞 <b>Tel raqami:</b> <i>{order.user.phone_number}</i>\n🏠 <b>Manzili:</b> """
    for location in order.user.location.all():
        text4channel += f"{location.address}\n"
    text4channel += '🛒 <b>Mahsulotlar:</b> \n'
    for order_item in order.get_order_items():
        product_details = order.get_product_details(
            order_item, order_item)
        text4channel += f" 🟢 <i>{product_details}</i>\n"
    text4channel += f"📝 <b>Izoh:</b> <i>{order.comment}</i>\n📅 <b>Sana:</b> <i>{order.created.strftime('%Y-%m-%d %H:%M')}</i>\n💸 <b>Jami:</b> <i>{order.total_amount} ₩</i>\n\n"
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id,
        text4channel,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("sent|"))
def handle_callback_query(call):
    order_id = int(call.data.split('|')[-1])
    try:
        order = Order.objects.get(id=order_id)
        order.status='sent'
        order.save()
        for order_item in order.orderitem.all():
            try:
                sold_product = SoldProduct.objects.get(
                    product=order_item.product, user=order.user)
                time_difference = timezone.now() - sold_product.created
                if time_difference < timedelta(days=30):
                    sold_product.quantity += order_item.quantity
                    sold_product.amount += order_item.product.new_price * order_item.quantity
                    sold_product.save()
                else:
                    sold_product.quantity = order_item.quantity
                    sold_product.amount = order_item.product.new_price * order_item.quantity
                    sold_product.save()
            except SoldProduct.DoesNotExist:
                SoldProduct.objects.create(
                    product=order_item.product,
                    quantity=order_item.quantity,
                    amount=order_item.product.new_price * order_item.quantity,
                    user=order.user,
                )
        text4channel = f"""🚚 <b>Buyurtma holati:</b> #<i>{order.get_status_display_value().upper()}</i>\n\n 🔢 <b>Buyurtma raqami:</b> <i>{order.id}</i>\n👤 <b>Mijoz ismi:</b> <i>{order.user.full_name}</i>\n📞 <b>Tel raqami:</b> <i>{order.user.phone_number}</i>\n🏠 <b>Manzili:</b> """
        for location in order.user.location.all():
            text4channel += f"{location.address}\n"
        text4channel += '🛒 <b>Mahsulotlar:</b> \n'
        for order_item in order.get_order_items():
            product_details = order.get_product_details(
                order_item, order_item)
            text4channel += f" 🟢 <i>{product_details}</i>\n"
        text4channel += f"📝 <b>Izoh:</b> <i>{order.comment}</i>\n📅 <b>Sana:</b> <i>{order.created.strftime('%Y-%m-%d %H:%M')}</i>\n💸 <b>Jami:</b> <i>{order.total_amount} ₩</i>"
        bot.delete_message(call.from_user.id, call.message.message_id)

        bot.send_message(
            call.from_user.id,
            text4channel,
        )
    except ObjectDoesNotExist:
        bot.send_message(call.from_user.id,
                         f"Order with ID {order_id} does not exist.")
    except Exception as e:
        bot.send_message(call.from_user.id, f"An error occurred: {e}")
