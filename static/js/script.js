//document.addEventListener('DOMContentLoaded', function () {
//    const projectSelect = document.getElementById('project');
//    const tagsSelect = document.getElementById('tags');
//
//    // Function to clear the options in the tags select
//    function clearTags() {
//        while (tagsSelect.options.length > 0) {
//            tagsSelect.remove(0);
//        }
//        tagsSelect.removeAttribute('required');
//    }
//
//    // Function to populate months in the tags select
//    function populateMonths() {
//        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
//        months.forEach(month => {
//            const option = document.createElement('option');
//            option.value = month;
//            option.textContent = month;
//            tagsSelect.appendChild(option);
//        });
//        tagsSelect.setAttribute('required', 'required');
//    }
//
//    // Event listener for project select change
//    projectSelect.addEventListener('change', function () {
//        clearTags();
//
//        if (projectSelect.value === "Monthly Bookkeeping") {
//            populateMonths();
//        }
//    });
//
//    // Initial check in case the page is loaded with a project already selected
//    if (projectSelect.value === "Monthly Bookkeeping") {
//        populateMonths();
//    } else {
//        clearTags();
//    }
//});

//document.addEventListener('DOMContentLoaded', function () {
//    const projectSelect = document.getElementById('project');
//    const tagSelector = document.getElementById('tagSelector');
//    const tagDropdown = document.getElementById('tagDropdown');
//    const tagList = document.querySelector('.dropdown-menu');
//    const tagRequiredError = document.getElementById('tagRequiredError');
//
//    // Function to clear the checkboxes in the tag selector
//    function clearTags() {
//        tagList.innerHTML = '';  // Clear all tag options
//        tagSelector.style.display = 'none';  // Hide the tag selector
//        tagRequiredError.style.display = 'none';  // Hide any error message
//    }
//
//    // Function to populate months as checkboxes in the tag selector
//    function populateMonths() {
//        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
//        months.forEach(month => {
//            const listItem = document.createElement('li');
//            const label = document.createElement('label');
//            label.classList.add('dropdown-item');
//
//            const checkbox = document.createElement('input');
//            checkbox.type = 'checkbox';
//            checkbox.name = 'tags[]';
//            checkbox.value = month;
//
//            label.appendChild(checkbox);
//            label.appendChild(document.createTextNode(month));
//            listItem.appendChild(label);
//            tagList.appendChild(listItem);
//        });
//
//        tagSelector.style.display = 'block';  // Show the tag selector
//    }
//
//    // Event listener for project select change
//    projectSelect.addEventListener('change', function () {
//        clearTags();
//
//        if (projectSelect.value === "Monthly Bookkeeping") {
//            populateMonths();
//        }
//    });
//
//    // Initial check in case the page is loaded with a project already selected
//    if (projectSelect.value === "Monthly Bookkeeping") {
//        populateMonths();
//    } else {
//        clearTags();
//    }
//
//    // Handle form submission to check if at least one tag is selected
//    document.getElementById('yourForm').addEventListener('submit', function (event) {
//        const selectedTags = document.querySelectorAll('input[name="tags[]"]:checked');
//        const tagsPresent = tagList.children.length > 0;
//
//        // Check if tags are present and none are selected
//        if (tagsPresent && selectedTags.length === 0) {
//            event.preventDefault();  // Prevent form submission
//            tagRequiredError.style.display = 'block';  // Show the error message
//        }
//    });
//});


document.addEventListener('DOMContentLoaded', function () {
    const projectSelect = document.getElementById('project');
    const tagSelector = document.getElementById('tagSelector');
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

    // Form submission validation
    document.getElementById('time-entry-form').addEventListener('submit', function (event) {
        const selectedTags = document.querySelectorAll('input[name="tags[]"]:checked');
        const tagsPresent = tagList.children.length > 0;

        if (tagsPresent && selectedTags.length === 0) {
            event.preventDefault();  // Prevent form submission
            window.alert("Please select at least one tag. Click the blue tag icon.")
        }
    });
});
