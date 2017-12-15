def graph1(request):
    import matplotlib.pyplot
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    #import cStringIO
    import io as cStringIO
    import random

    fig, ax = matplotlib.pyplot.subplots()
    ax.set_title(u'IMINASHI GRAPH')
    x_ax = range(1, 284)
    y_ax = [x * random.randint(436, 875) for x in x_ax]
    ax.plot(x_ax, y_ax)

    canvas = FigureCanvasAgg(fig)
    #buf = cStringIO.StringIO()
    buf = cStringIO.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    from django.http import HttpResponse
    response = HttpResponse(data)
    response['Content-Type'] = 'image/png'
    response['Content-Length'] = len(data)
    #import pdb; pdb.set_trace()
    return response

def graph2(request):
    import matplotlib.pyplot
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import random
    import string
    import os

    class TempImage(object):

        def __init__(self, file_name):
            self.file_name = file_name

        def create_png(self):
            fig, ax = matplotlib.pyplot.subplots()
            ax.set_title(u'IMINASHI GRAPH 2')
            x_ax = range(1, 284)
            y_ax = [x * random.randint(436, 875) for x in x_ax]
            ax.plot(x_ax, y_ax)

            canvas = FigureCanvasAgg(fig)
            canvas.print_figure(self.file_name)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            os.remove(self.file_name)

    chars = string.digits + string.ascii_letters
    img_name = ''.join(random.choice(chars) for i in range(64)) + '.png'

    with TempImage(img_name) as img:
        img.create_png()
        from django.http import HttpResponse
        response = HttpResponse(img_name, content_type='image/png')
        return response

        #response['Content-Type'] = 'image/png'
        #return send_file(img_name, mimetype='image/png')

def graph3(request):
    import matplotlib.pyplot as plt
    import numpy as np

    p1=np.array([-21.13327,-22.21668,-23.18828,-24.17004,-25.17249,-26.1799,-27.18734,-28.1953,-29.20075,-29.7026,-30.20255,-30.39721,-30.59832,-30.79937,-30.90142,-31.00682,-31.10436])
    b1=np.array([3.54116E-08,5.75725E-08,9.41607E-08,1.37501E-07,3.56973E-07,1.1102E-06,3.06082E-06,8.29829E-06,3.37019E-05,7.98162E-05,0.000182393,0.000266338,0.000375597,0.000549947,0.000658927,0.000802092,0.000937362])
    p2=np.array([-20.78326,-21.86284,-22.85089,-23.82712,-24.83065,-25.84306,-26.84405,-27.8613,-28.36283,-28.86108,-29.37328,-29.57035,-29.77269,-29.96316,-30.16689,-30.26363,-30.37226,-30.4639,-30.57312])
    b2=np.array([8.30571E-08,9.8052E-08,1.52036E-07,2.1902E-07,4.40381E-07,1.17206E-06,3.7519E-06,1.2783E-05,2.655E-05,5.59174E-05,0.000129112,0.00017392,0.000238123,0.000339051,0.000477024,0.000550037,0.000675191,0.000806236,0.000956225])

    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import io 

    fig, ax = plt.subplots()
    ax.set_title('BER plot')
    #ax.plot(p, -np.log(-np.log(b)))
    ax.scatter(p1, -np.log(-np.log(b1)), c='red')
    ax.scatter(p2, -np.log(-np.log(b2)), c='blue')

    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    from django.http import HttpResponse
    response = HttpResponse(data)
    response['Content-Type'] = 'image/png'
    response['Content-Length'] = len(data)
    return response

def UlidBerChartView(request, ulid):
    from .models import Entry

    import matplotlib.pyplot as plt
    import numpy as np

    #power = Entry.objects.filter(ulid=ulid, item='OpticalPower')
    #ber = Entry.objects.filter(ulid=ulid, item='Pre-FEC_ber')
    qs = Entry.objects.filter(ulid=ulid, item='OpticalPower')
    vl = qs.values_list('value', flat=True)
    power = np.array(list(vl))

    qs = Entry.objects.filter(ulid=ulid, item='Pre-FEC_ber')
    vl = qs.values_list('value', flat=True)
    prefecber = np.array(list(vl))

    qs = Entry.objects.filter(ulid=ulid, item='Post-FEC_ber')
    vl = qs.values_list('value', flat=True)
    postfecber = np.array(list(vl))    
    
    #import pdb; pdb.set_trace()

    import matplotlib.ticker as tick
    ylist = []
    for i in range(-4,-13,-1):
        ylist.append(10**i)
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import io 

    fig, ax = plt.subplots()
    ax.set_title('BER plot')
    ax.scatter(power, -np.log10(-np.log10(prefecber)), c='red')
    ax.scatter(power, -np.log10(-np.log10(postfecber)), c='blue')
    ax.yaxis.set_major_locator(tick.FixedLocator(-np.log10(-np.log10(ylist))))
    ax.set_ylim(-np.log10(-np.log10([1e-13, 1e-3])))
    ax.grid(True)

    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    from django.http import HttpResponse
    response = HttpResponse(data)
    response['Content-Type'] = 'image/png'
    response['Content-Length'] = len(data)
    return response

def BerChartListView(request):
    from django.shortcuts import render
    from .models import Condition
    qs = Condition.objects.all()
    return render(request, 'meas/chart_list.html', {'condition_list': qs})
