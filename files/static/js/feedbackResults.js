var chartData;
var fosChart;
var ratingCharts = new Array();

/* AJAX SETUP FOR CSRF */
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
/* END AJAX SETUP */

function printPieChart()
{
    data = chartData.replies.fos;
    fosChart = jQuery.jqplot ('field-of-study-chart', [data], 
    {
        grid: {
            drawBorder: false, 
            drawGridlines: false,
            background: '#ffffff',
            shadow:false
        },
        seriesDefaults: 
        {
            renderer: jQuery.jqplot.PieRenderer, 
            rendererOptions: 
            {
                showDataLabels: true,
                dataLabels: 'value',
                sliceMargin: 10
            }
        }, 
        legend: 
        { 
            show:true, 
            location: 'e',
            fontSize: '15pt',
            border: 'none'
        }
    });
}

function printRatingCharts()
{
    data = chartData.replies.ratings;
    titles = chartData.replies.titles;
    for(var i = 0; i < titles.length; i++)
    {   
        box = '<div class="col-md-6 rating-chart"><div id="rating-chart-' + i + '"></div></div>'
        $('#ratings').append(box);
        ticks = Array.range(1, data[i].length, 1);
        title = titles[i];
        ratingCharts[i] = $.jqplot('rating-chart-' + i, [data[i]], 
        {
            title: title,
            seriesDefaults:
            {
                renderer:$.jqplot.BarRenderer,
                pointLabels: 
                {
                    show: true, 
                    hideZeros: true,
                    formatString: '%d',
                }
            },
            axes: 
            {
                xaxis: 
                {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks,
                },
                yaxis:
                {
                    tickOptions: { show: false}
                },
            },
            grid: 
            { 
                gridLineColor: '#FFF',
                drawBorder: false,    
            }
        });
    }
}

Array.range= function(a, b, step){
    var A= [];
    if(typeof a== 'number'){
        A[0]= a;
        step= step || 1;
        while(a+step<= b){
            A[A.length]= a+= step;
        }
    }
    else{
        var s= 'abcdefghijklmnopqrstuvwxyz';
        if(a=== a.toUpperCase()){
            b=b.toUpperCase();
            s= s.toUpperCase();
        }
        s= s.substring(s.indexOf(a), s.indexOf(b)+ 1);
        A= s.split('');        
    }
    return A;
}

function deleteAnswer(answer, row)
{
    $.ajax({
        method: 'POST',
        url: '/feedback/deleteanswer/',
        data: {'answer_id':answerId, },
        success: function() {
            // TODO Make animation
            $(row).hide();
        },
        error: function(res) {
            var utils = new Utils();
            if (res['status'] === 412) {
                res = JSON.parse(res['responseText']);
                utils.setStatusMessage(res['message'], 'alert-danger');
            }
            else {
                utils.setStatusMessage('En uventet error ble oppdaget. Kontakt dotkom@online.ntnu.no for assistanse.', 'alert-danger');
            }
        },
        crossDomain: false
    });
}

$(document).ready(function()
{
    $.get($(location).attr('href') + "chartdata", function(data)
    {
        chartData = data;
        printPieChart();
        printRatingCharts();
    });
    $(window).on("debouncedresize", function(e)
    {
        fosChart.replot({ resetAxes: true});
        for(var i = 0; i < ratingCharts.length; i++)
        {
            ratingCharts[i].destroy();
        }
        printRatingCharts();
    });

    $('tr').each(function(i, row)
    {
        $(row).find('.icon').click(function()
        {
            answerId = $(row).find('td.answer-id').text();
            deleteAnswer(answerId, row);
        });
    });
});