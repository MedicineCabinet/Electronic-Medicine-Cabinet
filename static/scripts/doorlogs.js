function searchDoorlogs(event) {
    event.preventDefault(); // Prevent the default form submission
    const searchTerm = document.querySelector('input[name="search"]').value;

    // Fetch search results via AJAX
    fetch(`/doorlogs?search=${searchTerm}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the new rows
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error searching doorlogs:', error));
}

function refreshPage() {
    window.location.reload();
}



function sortDoorLogsByUsername() {
    fetch(`/doorlogs?sort_by=username`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by username:', error));
}

function sortDoorLogsByAccountType() {
    fetch(`/doorlogs?sort_by=accountType`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by account type:', error));
}

function sortDoorLogsByPosition() {
    fetch(`/doorlogs?sort_by=position`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by position:', error));
}

function sortDoorLogsByDate() {
    fetch(`/doorlogs?sort_by=date&order=desc`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by date:', error));
}

function sortDoorLogsByTime() {
    fetch(`/doorlogs?sort_by=time&order=desc`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by time:', error));
}

function sortDoorLogsByActionTaken() {
    fetch(`/doorlogs?sort_by=action_taken`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting door logs by action taken:', error));
}
