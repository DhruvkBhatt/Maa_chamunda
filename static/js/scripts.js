console.log("JavaScript is working!");
// Fetch packages and populate the container
document.addEventListener('DOMContentLoaded', function () {
    const packagesContainer = document.getElementById('packages-container');

    // Fetch packages from API
    fetch('/packages')
        .then(response => response.json())
        .then(packages => {
            packages.forEach(pkg => {
                const card = document.createElement('div');
                card.className = 'col-md-4';
                card.innerHTML = `
                    <div class="card">
                        <img src="${pkg.images.split(',')[0]}" class="card-img-top" alt="${pkg.name}">
                        <div class="card-body">
                            <h5>${pkg.name}</h5>
                            <p>${pkg.description}</p>
                            <a href="/packages/${pkg.id}" class="btn btn-primary">View</a>
                            <a href="/edit-package/${pkg.id}" class="btn btn-warning">Edit</a>
                            <form action="/delete-package/${pkg.id}" method="POST" style="display:inline;">
                                <button class="btn btn-danger" type="submit">Delete</button>
                            </form>
                        </div>
                    </div>
                `;
                packagesContainer.appendChild(card);
            });
        });
});

// Show/Hide "Other" input fields for Specialty Tour
document.getElementById('specialty-tour').addEventListener('change', function () {
    const otherSpecialtyInput = document.getElementById('other-specialty-tour');
    if (this.value === 'Other') {
        otherSpecialtyInput.classList.remove('d-none');
    } else {
        otherSpecialtyInput.classList.add('d-none');
        otherSpecialtyInput.value = '';
    }
});
// Show/Hide "Other" input fields for Category
// document.getElementById('category').addEventListener('change', function () {
//     const otherCategoryInput = document.getElementById('other-category');
//     if (this.value === 'Other') {
//         otherCategoryInput.classList.remove('d-none');
//     } else {
//         otherCategoryInput.classList.add('d-none');
//         otherCategoryInput.value = '';
//     }
// });
// Show/Hide "Other" input fields for Tour Type
document.getElementById('tour-type').addEventListener('change', function () {
    const otherTourTypeInput = document.getElementById('other-tour-type');
    if (this.value === 'Other') {
        otherTourTypeInput.classList.remove('d-none');
    } else {
        otherTourTypeInput.classList.add('d-none');
        otherTourTypeInput.value = '';
    }
});

// Generate Itinerary fields based on Duration
document.getElementById('generate-itinerary').addEventListener('click', function () {
    const durationInput = document.getElementById('duration').value.trim();
    const itineraryContainer = document.getElementById('itinerary-container');
    itineraryContainer.innerHTML = '<h5>Itinerary</h5>'; // Reset container

    // Extract number of days from the duration string
    const match = durationInput.match(/(\d+)\s*days?/i);
    if (match) {
        const numberOfDays = parseInt(match[1], 10);
        // Generate text areas for each day
        for (let i = 1; i <= numberOfDays; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('mb-3');
            dayDiv.innerHTML = `
                <label for="day-${i}" class="form-label">Day ${i}</label>
                <textarea id="day-${i}" name="itinerary_day_${i}" class="form-control" placeholder="Enter activities for Day ${i}" required></textarea>
            `;
            itineraryContainer.appendChild(dayDiv);
        }
    } else {
        alert('Please enter a valid duration in the format "X days".');
    }
});

document.querySelectorAll('.rich-text-editor').forEach((textarea) => {
    CKEDITOR.replace(textarea.id);
});
