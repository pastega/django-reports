import uuid, base64
from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns

def generate_code():
    return str(uuid.uuid4()).replace('-', '')[:12]

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    buffer.close()
    return graph

def get_key(res_by):
    if res_by == '#1': # Transaction
        key = 'transaction_id'
    elif res_by == '#2': # Creadted
        key = 'created'
    return key

def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 4))

    key = get_key(results_by)

    d = data.groupby(key, as_index=False)['total_price'].agg('sum')

    if chart_type == '#1': # Bar Chart
        plt.bar(d['key'], d['total_price'])
        #sns.barplot(x=key, y='total_price', data=d)

    elif chart_type == '#2': # Pie Chart
        plt.pie(data=data, x='price', labels=kwargs['labels'])
    
    elif chart_type == '#3': # Line Chart
        plt.plot(data['transaction_id'], data['price'], color='green', marker='o', linestyle='dashed')
    
    else:
        print('Unsupported chart type!')

    plt.tight_layout()
    chart = get_graph()
    return chart
