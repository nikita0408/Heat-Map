document.addEventListener('DOMContentLoaded', () => {
    const customerForm = document.getElementById('customerForm');
    const heatMapContainer = document.getElementById('heatMapContainer');
    const heatMap = document.getElementById('heatMap');

    customerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const customerID = document.getElementById('customerID').value;
        generateHeatMap(customerID);
    });

    function generateHeatMap(customerID) {
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ customer_id: customerID })
        };

        fetch('http://localhost:5000/generate_heat_map', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.heat_map) {
                    heatMap.innerHTML = JSON.stringify(data.heat_map);
                    heatMapContainer.style.display = 'block';
                } else {
                    alert(data.message);
                    heatMapContainer.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});
