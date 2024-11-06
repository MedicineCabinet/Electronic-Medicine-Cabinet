function loadContent(section, sidebarLinkId, offcanvasLinkId) {
    // Fetch the new content
    fetch(`/${section}`)
        .then(response => response.text())
        .then(html => {
            // Load the new content into the main content area
            document.getElementById('main-content').innerHTML = html;

            // Remove the "active" class from all sidebar links
            const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
            sidebarLinks.forEach(link => link.classList.remove('active'));

            // Remove the "active" class from all offcanvas links
            const offcanvasLinks = document.querySelectorAll('.offcanvas-body .nav-link');
            offcanvasLinks.forEach(link => link.classList.remove('active'));

            // Add the "active" class to the clicked sidebar link
            if (sidebarLinkId) {
                document.getElementById(sidebarLinkId).classList.add('active');
            }

            // Add the "active" class to the clicked offcanvas link
            if (offcanvasLinkId) {
                document.getElementById(offcanvasLinkId).classList.add('active');
            }
        })
        .catch(error => console.error('Error loading content:', error));
}

// Automatically load Inventory when the page is first loaded
document.addEventListener("DOMContentLoaded", function() {
    loadContent('inventory', 'inventory-link', 'offcanvas-inventory-link');
});

// Add function to load Doorlogs
function loadDoorlogs() {
    loadContent('doorlogs', 'doorlogs-link', 'offcanvas-doorlogs-link');
}

// Event listener for doorlogs link
document.getElementById('doorlogs-link').addEventListener('click', loadDoorlogs);
document.getElementById('offcanvas-doorlogs-link').addEventListener('click', loadDoorlogs);

// Event Listener for Window Resize
function checkScreenSizeAndCloseOffcanvas() {
    const offcanvasSidebar = document.getElementById('offcanvasSidebar');
    const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvasSidebar);
    // Function when the screen is currently on small size
    if (window.innerWidth >= 992) { // 992px is the breakpoint for lg (large screens)
        if (bsOffcanvas && bsOffcanvas._isShown) {
            bsOffcanvas.hide(); // Close the offcanvas if it's shown
        }
    }
}

// Attach the resize event listener
window.addEventListener('resize', checkScreenSizeAndCloseOffcanvas);
