function searchDoorLogs(event) {
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
        // Replace the table body with the new rows for doorlogs
        document.getElementById('doorlogs-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error searching doorlogs:', error));
}


function sortDoorLogsByUsername() {
    sortTable('username');
}

function sortDoorLogsByAccountType() {
    sortTable('accountType');
}

function sortDoorLogsByPosition() {
    sortTable('position');
}

function sortDoorLogsByDate() {
    sortTable('date');
}

function sortDoorLogsByTime() {
    sortTable('time');
}

function sortDoorLogsByActionTaken() {
    sortTable('action_taken');
}

function sortTable(column) {
    const table = document.getElementById('doorlogs-table-body');
    const rows = Array.from(table.rows);

    // Determine sort order (ascending or descending)
    const isAscending = table.getAttribute('data-sort') !== column;
    rows.sort((a, b) => {
        const aValue = a.cells[getColumnIndex(column)].innerText;
        const bValue = b.cells[getColumnIndex(column)].innerText;

        return isAscending
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });

    // Clear the table body and append sorted rows
    table.innerHTML = '';
    rows.forEach(row => table.appendChild(row));

    // Update the sorting column
    table.setAttribute('data-sort', isAscending ? column : '');
}

function getColumnIndex(column) {
    const columns = ['username', 'accountType', 'position', 'date', 'time', 'action_taken'];
    return columns.indexOf(column);
}
