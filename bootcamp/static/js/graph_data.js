// var bar_labels = JSON.parse({{ bar_labels|safe }});
// var bar_data = {{ bar_data }};

// var bar_labels = ["Feeds", "Articles", "Comments", "Questions", "Answers", "Activities"];
// var bar_data = [34, 23, 25, 23, 45, 54];

setBarChart()
setLineChart()

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

// function setBarChart(){
//     var ctx = document.getElementById("bar_chart").getContext('2d');
//     var bar_labels = ["Feeds", "Articles", "Comments", "Questions", "Answers", "Activities"];
//     var bar_data = {{ bar_data }};
//     var myChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: bar_labels,
//             datasets: [{
//                 label: 'Activities by type:',
//                 data: bar_data,
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 159, 64, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255,99,132,1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero:true
//                     }
//                 }]
//             }
//         }
//     });
// }

// function setLineChart(){
//     var ctx = document.getElementById("line_chart").getContext('2d');
//     var myChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: bar_labels,
//             datasets: [{
//                 label: 'Activities by type:',
//                 data: bar_data,
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255,99,132,1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero:true
//                     }
//                 }]
//             }
//         }
//     });
// }
