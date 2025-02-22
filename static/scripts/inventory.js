function searchInventory(event) {
    event.preventDefault(); // Prevent the default form submission
    const searchTerm = document.querySelector('input[name="search"]').value;

    // Fetch search results via AJAX
    fetch(`/inventory?search=${searchTerm}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the new rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error searching inventory:', error));
}

function refreshPage() {
    window.location.reload();
}
function refreshDoorlogs() {
    // Check if the current URL is already pointing to the 'doorlogs' route
    if (window.location.pathname === "/doorlogs") {
        // Reloads only the 'doorlogs' section
        location.reload();
    } else {
        // Navigates back to 'doorlogs' if on a different route
        window.location.href = "/doorlogs";
    }
}

function refreshNotification() {
    // Check if the current URL is already pointing to the 'notification' route
    if (window.location.pathname === "/notification") {
        // Reloads only the 'notification' page
        location.reload();
    } else {
        // Navigates back to 'notification' if on a different route
        window.location.href = "/notification";
    }
}

function sortInventoryByName() {
    // Fetch the inventory sorted by name via AJAX
    fetch(`/inventory?sort_by=name`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory:', error));
}
function sortInventoryByType() {
    // Fetch the inventory sorted by type via AJAX
    fetch(`/inventory?sort_by=type`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by type:', error));
}
function sortInventoryByDosage() {
    // Fetch the inventory sorted by dosage via AJAX
    fetch(`/inventory?sort_by=dosage`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by dosage:', error));
}
function sortInventoryByQuantity() {
    // Fetch the inventory sorted by quantity in ascending order via AJAX
    fetch(`/inventory?sort_by=quantity&order=asc`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by quantity:', error));
}

function sortInventoryByUnit() {
    // Fetch the inventory sorted by type via AJAX
    fetch(`/inventory?sort_by=unit`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by unit:', error));
}

function sortInventoryByDateStored() {
    // Fetch the inventory sorted by date stored in descending order via AJAX
    fetch(`/inventory?sort_by=date_stored&order=desc`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by date stored:', error));
}

function sortInventoryByExpirationDate() {
    // Fetch the inventory sorted by expiration date in descending order via AJAX
    fetch(`/inventory?sort_by=expiration_date&order=desc`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify this as an AJAX request
        }
    })
    .then(response => response.text())
    .then(html => {
        // Replace the table body with the sorted rows
        document.getElementById('inventory-table-body').innerHTML = html;
    })
    .catch(error => console.error('Error sorting inventory by expiration date:', error));
}

function extractCSV() {
    const now = new Date();
    const formattedDate = now.toISOString().split('T')[0]; // YYYY-MM-DD
    const formattedTime = now.toTimeString().split(' ')[0].replace(/:/g, '-'); // HH-MM-SS
    const filename = `medicine_inventory_${formattedDate}_${formattedTime}.csv`;
    
    window.location.href = `/inventory?format=csv&filename=${filename}`;
}

function extractCSVDoorlogs() {
    const now = new Date();
    const formattedDate = now.toISOString().split('T')[0]; // YYYY-MM-DD
    const formattedTime = now.toTimeString().split(' ')[0].replace(/:/g, '-'); // HH-MM-SS
    const filename = `door_logs_${formattedDate}_${formattedTime}.csv`;

    window.location.href = `/doorlogs?format=csv&filename=${filename}`;
}
