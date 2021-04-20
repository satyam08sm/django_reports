import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns


def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code


def get_salesman_from_id(id):
    return Profile.objects.get(id=id).user.username


def get_customer_from_id(id):
    return Customer.objects.get(id=id)


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    d = data.groupby(kwargs.get('results_by'), as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        # plt.bar(data['transaction_id'], data['price'])
        sns.barplot(x=kwargs.get('results_by'), y='total_price', data=d)
    elif chart_type == '#2':
        # labels = kwargs.get('labels')
        labels = d[kwargs.get('results_by')].values
        plt.pie(data=d, x='total_price', labels=labels)

    elif chart_type == '#3':
        plt.plot(d[kwargs.get('results_by')], d['total_price'], color='green', marker='o', linestyle='dashed')

    else:
        print('None')
    plt.tight_layout()
    chart = get_graph()
    return chart
