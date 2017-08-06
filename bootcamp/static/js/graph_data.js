setBarChart()
setLineChart()
setDoughnutChart()

function setBarChart(){
    var ctx_bar_chart = document.getElementById("bar_chart").getContext('2d');
    var my_bar_chart = new Chart(ctx_bar_chart, {
        type: 'bar',
        data: {
            labels: bar_labels,
            datasets: [{
                label: 'Activities by type:',
                data: bar_data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            },
            title: {
                display: true,
                text: 'User activity by type.'
            }
        }
    });
}

function setLineChart(){
    var ctx_line_chart = document.getElementById("line_chart").getContext('2d');
    var my_line_chart = new Chart(ctx_line_chart, {
        type: 'line',
        data: {
            labels: line_labels,
            datasets: [{
                label: 'Daily Activity:',
                data: line_data,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 2.5,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: Math.max.apply(Math, line_data) + 2
                    }
                }]
            },
            title: {
                display: true,
                text: 'User activity by day.'
            }
        }
    });
}

function setDoughnutChart(){
    var ctx_doughnut_chart = document.getElementById("doughnut_chart").getContext('2d');
    var my_doughnut_chart = new Chart(ctx_doughnut_chart, {
        type: 'doughnut',
        data: {
            labels: bar_labels,
            datasets: [{
                label: 'Activities by total participation:',
                data: bar_data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            rotation: -Math.PI,
            cutoutPercentage: 60,
            circumference: Math.PI,
            legend: {
                position: 'left'
            },
            animation: {
                animateRotate: false,
                animateScale: true
            },
            title: {
                display: true,
                text: 'User activity by total participation.'
            }
        }
    });
}
