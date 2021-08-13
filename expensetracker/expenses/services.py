import datetime
import urllib
import json
import base64
from io import BytesIO

from django.template.defaulttags import register
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from .models import Category, Transaction


@register.filter
def get_item(dictionary, key):
    print(dictionary)
    return dictionary.get(key)


def get_time_now():
    t = datetime.datetime.now()
    t = t.timetuple()
    return datetime.time(t.tm_hour, t.tm_min)


def convert_str_to_datetime(date, time):
    datetime_value = datetime.datetime.strptime(
        date+' '+time, '%Y-%m-%d %H:%M:%S')
    return datetime_value


def get_user_trans_data(user, total_amount=False, categories_amount=False, total_income=False, months_amount=False):
    converter = get_actual_usd_converts()

    transactions = Transaction.objects.filter(user=user)

    sum_total_amount = 0
    by_categories = dict([(category.name, 0) for category in Category.objects.all()]) if categories_amount else None
    income_amount = {'Income': 0, 'Expense': 0}
    by_months = dict([(datetime.datetime.strptime(str(month), '%m').strftime('%b'),0) for month in range(1,13)])
    for transaction in transactions:
        trans_shortut = transaction.currency.shortcut
        trans_type = transaction.type
        if trans_shortut != 'USD':
            parse_usd_value = converter['rates'][trans_shortut]
            converted = (float(transaction.amount) / (parse_usd_value))
        else:
            converted = float(transaction.amount)

        if total_amount:
            if trans_type == 'E':
                sum_total_amount -= converted
            else:
                sum_total_amount += converted

        elif categories_amount:
            category_name = transaction.category.name
            if trans_type == 'E':
                by_categories[category_name] -= round(converted, 2)
            else:
                by_categories[category_name] += round(converted, 2)

        elif total_income:
            if trans_type == 'E':
                income_amount['Expense'] -= round(converted, 2)
            else:
                income_amount['Income'] += round(converted, 2)
        
        elif months_amount:
            month = transaction.date.strftime('%b')
            if trans_type == 'E':
                by_months[month] -= round(converted, 2)
            else:
                by_months[month] += round(converted, 2)

    data = round(sum_total_amount,
                 2) if total_amount else by_categories if categories_amount else income_amount if total_income else by_months
    return data


def get_actual_usd_converts():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


def statistics_img(user,  categories_amount=False, total_income=False, months_amount=True):
    trans_data = [(label, amount)
                  for label, amount in get_user_trans_data(user, False, categories_amount, total_income, months_amount).items()]
    labels = [label[0] for label in trans_data]
    amounts = [amount[1] for amount in trans_data]
    high = max(amounts)
    low = min(amounts)
    x = np.arange(len(labels))

    fig, ax = plt.subplots()
    rect = ax.bar(x, amounts, width=[0.8 if not total_income else 0.2 for _ in x], color=[
                  'crimson' if amount < 0 else 'limegreen' for amount in amounts])

    plt.xticks(rotation=45)
    plt.ylim([np.ceil(low-0.2*(high-low)), np.ceil(high+0.2*(high-low))])

    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
            }

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.bar_label(rect, padding=6)
    ax.set_ylabel('Amount - $', rotation=0, labelpad=50, fontdict=font)

    ax.set_title(
        f"{user.username}  -  {'Money per category' if categories_amount else 'Income/Expense' if total_income else 'Money per month' if months_amount else 'Undefind'}", fontdict=font)

    fig.tight_layout()

    return buffer_graphic(plt)


def buffer_graphic(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='jpg', )
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic
