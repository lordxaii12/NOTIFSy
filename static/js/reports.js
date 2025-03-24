//-JS CODE FOR 'NOTIFS' BY: RYRUBIO-//
//==================================================================================================================================//
//DIVISION-CREDIT_USED GRAPH//
if (typeof divisionData !== 'undefined' && Object.keys(divisionData).length > 0) {
    const labels = Object.keys(divisionData);
    const dataValues = Object.values(divisionData);

    const ctx = document.getElementById('myChart');
    
    if (ctx) {
        const myChart = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Credits Used by Division',
                    data: dataValues,
                    backgroundColor: 'rgba(255, 1, 17, 0.6)',
                    borderColor: 'rgb(123, 3, 13)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#ccc',
                            lineWidth: 2
                        },
                        ticks: {
                            color: '#000',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    x: {
                        grid: {
                            color: '#ccc',
                            lineWidth: 2
                        },
                        ticks: {
                            color: '#000',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#333',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    }
                }
            }
        });
    } else {
        console.error('Canvas with ID "myChart" not found.');
    }
} else {
    console.error('Division data is undefined or empty.');
}

