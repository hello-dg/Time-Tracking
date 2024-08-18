document.addEventListener('DOMContentLoaded', function () {
    const projectSelect = document.getElementById('project');
    const tagsSelect = document.getElementById('tags');

    // Function to clear the options in the tags select
    function clearTags() {
        while (tagsSelect.options.length > 0) {
            tagsSelect.remove(0);
        }
        tagsSelect.removeAttribute('required');
    }

    // Function to populate months in the tags select
    function populateMonths() {
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            tagsSelect.appendChild(option);
        });
        tagsSelect.setAttribute('required', 'required');
    }

    // Event listener for project select change
    projectSelect.addEventListener('change', function () {
        clearTags();

        if (projectSelect.value === "Monthly Bookkeeping") {
            populateMonths();
        }
    });

    // Initial check in case the page is loaded with a project already selected
    if (projectSelect.value === "Monthly Bookkeeping") {
        populateMonths();
    } else {
        clearTags();
    }
});