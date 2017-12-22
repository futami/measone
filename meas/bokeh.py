from django.shortcuts import render_to_response
import numpy as np

def graph1(request):

    x= [1,3,5,7,9,11,13]
    y= [1,2,3,4,5,6,7]

    p1=np.array([-21.13327,-22.21668,-23.18828,-24.17004,-25.17249,-26.1799,-27.18734,-28.1953,-29.20075,-29.7026,-30.20255,-30.39721,-30.59832,-30.79937,-30.90142,-31.00682,-31.10436])
    b1=np.array([3.54116E-08,5.75725E-08,9.41607E-08,1.37501E-07,3.56973E-07,1.1102E-06,3.06082E-06,8.29829E-06,3.37019E-05,7.98162E-05,0.000182393,0.000266338,0.000375597,0.000549947,0.000658927,0.000802092,0.000937362])
    p2=np.array([-20.78326,-21.86284,-22.85089,-23.82712,-24.83065,-25.84306,-26.84405,-27.8613,-28.36283,-28.86108,-29.37328,-29.57035,-29.77269,-29.96316,-30.16689,-30.26363,-30.37226,-30.4639,-30.57312])
    b2=np.array([8.30571E-08,9.8052E-08,1.52036E-07,2.1902E-07,4.40381E-07,1.17206E-06,3.7519E-06,1.2783E-05,2.655E-05,5.59174E-05,0.000129112,0.00017392,0.000238123,0.000339051,0.000477024,0.000550037,0.000675191,0.000806236,0.000956225])

    b3 = -np.log10(-np.log10(b1))
    b4 = -np.log10(-np.log10(b2))

    from bokeh.plotting import figure, output_file, show 
    from bokeh.embed import components
    #from bokeh.resources import CDN
    #from bokeh.embed import file_html

    plot = figure(title= 'BER plot', x_axis_label= 'Pin', y_axis_label= 'BER', 
    plot_width =400, plot_height =400)

    plot.line(p1, b3, legend= 'BER1', line_width = 2, color='red')
    plot.scatter(p2, b4, legend= 'BER2', line_width = 2, color='blue')
    #Store components 
    script, div = components(plot)

    #Feed them to the Django template.
    return render_to_response( 'meas/bokeh_image.html', {'script' : script , 'div' : div} )
    #return file_html(plot, CDN, "my plot")

def UlidBerChartView(request, ulid):
    from .models import Entry
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.models.tickers import FixedTicker

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

    #ylist = []
    #for i in range(-4,-13,-1):
    #    ylist.append(10**i)
    
    plot = figure(title= 'BER plot', x_axis_label= 'Pin', y_axis_label= 'BER', 
    plot_width =400, plot_height =400)

    plot.scatter(power, -np.log10(-np.log10(prefecber)), legend= 'Pre-FEC', line_width = 2, color='red')
    plot.scatter(power, -np.log10(-np.log10(postfecber)), legend= 'Post-FEC', line_width = 2, color='blue')

    plot.yaxis.ticker = -np.log10(-np.log10(10 ** np.arange(-13, -3, 1.0)))
    plot.ygrid.ticker = FixedTicker(ticks=-np.log10(-np.log10(10 ** np.arange(-13, -3, 1.0))))

    from bokeh.embed import file_html
    from django.http import HttpResponse

    response = HttpResponse(file_html(plot, CDN, 'my plot'))
    return response
    #return file_html(plot, CDN, 'my plot')
    # Error: file_html: 'str' object has no attribute 'get'

def BerChartListView(request):
    from django.shortcuts import render
    from .models import Condition
    from .models import Entry
    qs = Condition.objects.all()
    ulid_list = Condition.objects.values_list('ulid', flat=True)
    #import pdb; pdb.set_trace()

    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.models.tickers import FixedTicker

    chart_list=[]
    for ulid in ulid_list:
        qs = Entry.objects.filter(ulid=ulid, item='OpticalPower')
        vl = qs.values_list('value', flat=True)
        power = np.array(list(vl))

        qs = Entry.objects.filter(ulid=ulid, item='Pre-FEC_ber')
        vl = qs.values_list('value', flat=True)
        prefecber = np.array(list(vl))

        qs = Entry.objects.filter(ulid=ulid, item='Post-FEC_ber')
        vl = qs.values_list('value', flat=True)
        postfecber = np.array(list(vl))

        plot = figure(title= 'BER plot', x_axis_label= 'Pin', y_axis_label= 'BER', 
        plot_width =400, plot_height =400)

        plot.scatter(power, -np.log10(-np.log10(prefecber)), legend= 'Pre-FEC', line_width = 2, color='red')
        plot.scatter(power, -np.log10(-np.log10(postfecber)), legend= 'Post-FEC', line_width = 2, color='blue')

        plot.yaxis.ticker = -np.log10(-np.log10(10 ** np.arange(-13, -3, 1.0)))
        plot.ygrid.ticker = FixedTicker(ticks=-np.log10(-np.log10(10 ** np.arange(-13, -3, 1.0))))

        script, div = components(plot)
        
        #import pdb; pdb.set_trace()
        chart_list.append({'ulid': ulid, 'script': script, 'div': div})

    #import pdb; pdb.set_trace()
    return render(request, 'meas/bokeh_list.html', {'chart_list': chart_list})