const backendUrl = `http://${window.location.hostname}:${window.BACKEND_PORT || 30502}`;

function sendPostRequest() {
    const data = {
        // Example data to send in the POST request
        key1: 'value1',
        key2: 'value2'
    };

    fetch(`${backendUrl}/api/endpoint`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        document.getElementById('jsonResponse').innerText = JSON.stringify(data, null, 2);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// document.getElementById('submit-button').addEventListener('click', (event) => {
//     event.preventDefault();
//     sendPostRequest();
// });

document.getElementById('helloButton').addEventListener('click', () => {
    console.log("Hello button clicked");
    fetch(`${backendUrl}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = data.message;
            document.getElementById('jsonResponse').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('recommendButton').addEventListener('click', () => {
    console.log("Recommend button clicked");
    fetch(`${backendUrl}/api/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = `Recommendations: ${data.songs.join(', ')}`;
        document.getElementById('jsonResponse').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error:', error));
});