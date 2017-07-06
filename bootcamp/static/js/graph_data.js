var endpoint = '/endpoints/graph/';
$.ajax({
    method: 'GET',
    url: endpoint,
    success: function(request_data){
        bar_labels = request_data.bar_labels;
        bar_data = request_data.bar_data;
        // var feeds_count = request_data.feeds_count,
        // var article_count = request_data.article_count,
        // var article_comment_count = request_data.article_comment_count,
        // var question_count = request_data.question_count,
        // var answer_count = request_data.answer_count,
        setColumnChart();
    },
    error: function(error_data){
        console.log('Error:'),
        console.log(error_data)
    }
})

function setColumnChart(){
    var ctx = document.getElementById("bar_chart").getContext('2d');
    var myChart = new Chart(ctx, {
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
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}
