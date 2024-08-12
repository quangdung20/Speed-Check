function fetchData() {
            const startTime = document.getElementById('start_time').value;
            const endTime = document.getElementById('end_time').value;
            const messageDiv = document.getElementById('message');

            fetch(`http://localhost:5000/api/speed_data?start_time=${startTime}&end_time=${endTime}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        messageDiv.textContent = "No data available for the selected time range.";
                        clearCharts();
                    } else {
                        messageDiv.textContent = "Data fetched successfully!";

                        const times = data.map(d => new Date(d.time).toLocaleString());
                        const speedRealRight = data.map(d => d.speed_real_right);
                        const speedSetRight = data.map(d => d.speed_set_right);
                        const speedRealLeft = data.map(d => d.speed_real_left);
                        const speedSetLeft = data.map(d => d.speed_set_left);

                        new Chart(document.getElementById('chartRight').getContext('2d'), {
                            type: 'line',
                            data: {
                                labels: times,
                                datasets: [
                                    { label: 'Speed Real Right', data: speedRealRight, borderColor: 'blue', fill: false },
                                    { label: 'Speed Set Right', data: speedSetRight, borderColor: 'red', fill: false }
                                ]
                            },
                            options: {
                                scales: {
                                    x: { title: { display: true, text: 'Time' } },
                                    y: { title: { display: true, text: 'Speed' } }
                                }
                            }
                        });

                        new Chart(document.getElementById('chartLeft').getContext('2d'), {
                            type: 'line',
                            data: {
                                labels: times,
                                datasets: [
                                    { label: 'Speed Real Left', data: speedRealLeft, borderColor: 'green', fill: false },
                                    { label: 'Speed Set Left', data: speedSetLeft, borderColor: 'orange', fill: false }
                                ]
                            },
                            options: {
                                scales: {
                                    x: { title: { display: true, text: 'Time' } },
                                    y: { title: { display: true, text: 'Speed' } }
                                }
                            }
                        });
                    }
                })
                .catch(error => {
                    messageDiv.textContent = "An error occurred while fetching data.";
                    console.error('Error fetching data:', error);
                });
        }

        // Clear the charts if there's no data
        function clearCharts() {
            const ctxRight = document.getElementById('chartRight').getContext('2d');
            ctxRight.clearRect(0, 0, ctxRight.canvas.width, ctxRight.canvas.height);

            const ctxLeft = document.getElementById('chartLeft').getContext('2d');
            ctxLeft.clearRect(0, 0, ctxLeft.canvas.width, ctxLeft.canvas.height);
        }
