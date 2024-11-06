document.getElementById('addUserForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent traditional form submission

    const formData = new FormData(this);  // Gather form data

    fetch('/accounts', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify as AJAX request
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal if the user was added successfully
            const addUserModal = document.getElementById('addUserModal');
            const modal = bootstrap.Modal.getInstance(addUserModal);
            modal.hide();

            // Refresh the page or update the table dynamically
            location.reload(); // Or use AJAX to fetch and update only the table
        } else {
            // Display an error message if adding the user failed
            alert("Error adding user: " + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});
