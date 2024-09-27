function searchDoorlogs(event) {
    event.preventDefault();  // Prevent the default form submission

    const searchInput = document.querySelector('input[name="search"]').value;
    fetch(`/doorlogs?search=${encodeURIComponent(searchInput)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('doorlogs-table-body').innerHTML = html;  // Update the table body
        })
        .catch(error => console.error('Error fetching door logs:', error));
}

// doorlogs.js

function refreshDoor() {
    fetch('/doorlogs')  // Make a request to the Flask route
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();  // Get the HTML response
        })
        .then(html => {
            document.getElementById('doorlogs-table-body').innerHTML = html;  // Update the table body
        })
        .catch(error => console.error('Error refreshing door logs:', error));
}
