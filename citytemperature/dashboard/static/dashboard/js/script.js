

function chartA(years,temperatures){
	Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Yearly Average Temperature'
        },
        xAxis: {
            categories: years            
        },
        series: [{
            name: 'YEAR',
            data: temperatures,
            color: 'green'
        }]

    });
}

function chartB(list,temp_y){
	 Highcharts.chart('container1', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'City Average Temperature'
        },
        xAxis: {
            // categories:cities
            type:'category'
        },
        series: [{
            name: 'CITY',
            data: list,
            color: 'green'
        }],
    drilldown: {
        series: temp_y
    }
    });
}
