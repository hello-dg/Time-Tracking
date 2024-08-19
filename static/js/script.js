document.addEventListener('DOMContentLoaded', function () {
    const projectSelect = document.getElementById('project');
    const tagSelector = document.getElementById('tagSelector');
    const tagDropdown = document.getElementById('tagDropdown');
    const tagList = document.querySelector('.dropdown-menu');
    const tagRequiredError = document.getElementById('tagRequiredError');

    function clearTags() {
        tagList.innerHTML = '';
        tagSelector.style.display = 'none';
        tagRequiredError.style.display = 'none';
    }

    function populateMonths() {
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        months.forEach(month => {
            const listItem = document.createElement('li');
            const label = document.createElement('label');
            label.classList.add('dropdown-item');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = 'tags[]';
            checkbox.value = month;

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(month));
            listItem.appendChild(label);
            tagList.appendChild(listItem);
        });

        tagSelector.style.display = 'block';  // Show the tag selector
    }

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


    // Change Icon Color
    function updateTagIcon() {
        const selectedTags = document.querySelectorAll('input[name="tags[]"]:checked');
        if (selectedTags.length > 0) {
            tagDropdown.src = "static/icons/tag_selected_64.png"; // Change to selected icon
        } else {
            tagDropdown.src = "static/icons/tag_not_selected_64.png"; // Change back to default icon
        }
    }

    tagList.addEventListener('change', function () {
        updateTagIcon();
    });

    // Form submission validation
    document.getElementById('time-entry-form').addEventListener('submit', function (event) {
        const selectedTags = document.querySelectorAll('input[name="tags[]"]:checked');
        const tagsPresent = tagList.children.length > 0;

        if (tagsPresent && selectedTags.length === 0) {
            event.preventDefault();  // Prevent form submission
            window.alert("Please select at least one tag. Click the tag icon to the right of the activity dropdown.")
        }
    });
});