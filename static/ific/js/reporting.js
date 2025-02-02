function add_chart (data) {
    var div = document.createElement('div')
    div.setAttribute("class", "ific_chart")
    var canvas = document.createElement('canvas')
    let canvas_id = Math.random().toString(36).substring(2)
    canvas.id = canvas_id
    div.appendChild(canvas)
    var parent_div = document.getElementById('chart-content')
    parent_div.appendChild(div)

    var ctx = document.getElementById(canvas_id).getContext('2d')
    var myChart = new Chart(ctx, data)
}


function clear_chart_content() {
    $('#chart-content').empty()
}



function add_stacked_bar_chart() {
    let dummy_data = {
        type: 'bar',
        data: {
			labels: ['January', 'February', 'March', 'April', 'May', 'June'],
			datasets: [{
				label: 'Dataset 1',
				backgroundColor: 'rgba(255, 99, 132, 0.5)',
				data: [12, 19, 3, 5, 2, 3],
			}, {
				label: 'Dataset 2',
				backgroundColor:'rgba(54, 162, 235, 0.5)',
				data: [12, 19, 3, 5, 2, 3],
			}, {
				label: 'Dataset 3',
				backgroundColor: 'rgba(75, 192, 192, 0.5)',
				data: [12, 19, 3, 5, 2, 3],
			}]

		},
        options: {
            
           
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    }
    add_chart(dummy_data)
}







// TEST CHART

function test_bar_chart(type) {
    let dummy_data = {
        type: type,
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, .5)',
                    'rgba(54, 162, 235, .5)',
                    'rgba(255, 206, 86, .5)',
                    'rgba(75, 192, 192, .5)',
                    'rgba(153, 102, 255, .5)',
                    'rgba(255, 159, 64, .5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            
        }
    }
    add_chart(dummy_data)
}


$(document).ready(function(){

    
})
