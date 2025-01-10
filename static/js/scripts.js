// console.log("JavaScript is working!");
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

// // Show/Hide "Other" input fields for Specialty Tour
// document.getElementById('specialty-tour').addEventListener('change', function () {
//     const otherSpecialtyInput = document.getElementById('other-specialty-tour');
//     if (this.value === 'Other') {
//         otherSpecialtyInput.classList.remove('d-none');
//     } else {
//         otherSpecialtyInput.classList.add('d-none');
//         otherSpecialtyInput.value = '';
//     }
// });


document.addEventListener('DOMContentLoaded', function () {
    const specialtyTourElement = document.getElementById('specialty-tour');
    if (specialtyTourElement) {
        specialtyTourElement.addEventListener('change', function () {
            const otherSpecialtyInput = document.getElementById('other-specialty-tour');
            if (this.value === 'Other') {
                otherSpecialtyInput.classList.remove('d-none');
            } else {
                otherSpecialtyInput.classList.add('d-none');
                otherSpecialtyInput.value = '';
            }
        });
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
// document.getElementById('tour-type').addEventListener('change', function () {
//     const otherTourTypeInput = document.getElementById('other-tour-type');
//     if (this.value === 'Other') {
//         otherTourTypeInput.classList.remove('d-none');
//     } else {
//         otherTourTypeInput.classList.add('d-none');
//         otherTourTypeInput.value = '';
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    const tourTypeElement = document.getElementById('tour-type');
    if (tourTypeElement) {
        tourTypeElement.addEventListener('change', function () {
            const otherTourTypeInput = document.getElementById('other-tour-type');
            if (this.value === 'Other') {
                otherTourTypeInput.classList.remove('d-none');
            } else {
                otherTourTypeInput.classList.add('d-none');
                otherTourTypeInput.value = '';
            }
        });
    }
});

// // Generate Itinerary fields based on Duration
// document.getElementById('generate-itinerary').addEventListener('click', function () {
//     const durationInput = document.getElementById('duration').value.trim();
//     const itineraryContainer = document.getElementById('itinerary-container');
//     itineraryContainer.innerHTML = '<h5>Itinerary</h5>'; // Reset container

//     // Extract number of days from the duration string
//     const match = durationInput.match(/(\d+)\s*days?/i);
//     if (match) {
//         const numberOfDays = parseInt(match[1], 10);
//         // Generate text areas for each day
//         for (let i = 1; i <= numberOfDays; i++) {
//             const dayDiv = document.createElement('div');
//             dayDiv.classList.add('mb-3');
//             dayDiv.innerHTML = `
//                 <label for="day-${i}" class="form-label">Day ${i}</label>
//                 <textarea id="day-${i}" name="itinerary_day_${i}" class="form-control" placeholder="Enter activities for Day ${i}" required></textarea>
//             `;
//             itineraryContainer.appendChild(dayDiv);
//         }
//     } else {
//         alert('Please enter a valid duration in the format "X days".');
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const generateItineraryButton = document.getElementById('generate-itinerary');

    if (generateItineraryButton) {
        generateItineraryButton.addEventListener('click', function () {
            const durationInput = document.getElementById('duration')?.value.trim();
            const itineraryContainer = document.getElementById('itinerary-container');

            if (!durationInput || !itineraryContainer) {
                alert('Required elements are missing. Please check the form.');
                return;
            }

            itineraryContainer.innerHTML = '<h5>Itinerary</h5>'; // Reset container

            // Extract number of days from the duration string
            const match = durationInput.match(/(\d+)\s*days?/i);
            if (match) {
                const numberOfDays = parseInt(match[1], 10);

                // Fetch existing itinerary data
                const existingItineraries = Array.from(itineraryContainer.querySelectorAll('textarea'))
                    .reduce((acc, textarea) => {
                        const dayNumber = parseInt(textarea.id.split('-')[1], 10);
                        acc[dayNumber] = textarea.value;
                        return acc;
                    }, {});

                // Generate text areas for each day
                for (let i = 1; i <= numberOfDays; i++) {
                    const dayDiv = document.createElement('div');
                    dayDiv.classList.add('mb-3');
                    dayDiv.innerHTML = `
                        <label for="day-${i}" class="form-label">Day ${i}</label>
                        <textarea id="day-${i}" name="itinerary_day_${i}" class="form-control" 
                                  placeholder="Enter activities for Day ${i}" required>${existingItineraries[i] || ''}</textarea>
                    `;
                    itineraryContainer.appendChild(dayDiv);
                }
            } else {
                alert('Please enter a valid duration in the format "X days".');
            }
        });
    }
});

// Preload existing itineraries when the page loads
document.addEventListener('DOMContentLoaded', function () {
    const itineraryContainer = document.getElementById('itinerary-container');
    if (itineraryContainer && itineraryContainer.dataset.itineraries) {
        const itineraries = JSON.parse(itineraryContainer.dataset.itineraries);
        itineraries.forEach((itinerary, index) => {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('mb-3');
            dayDiv.innerHTML = `
                <label for="day-${index + 1}" class="form-label">Day ${index + 1}</label>
                <textarea id="day-${index + 1}" name="itinerary_day_${index + 1}" class="form-control" 
                          placeholder="Enter activities for Day ${index + 1}" required>${itinerary}</textarea>
            `;
            itineraryContainer.appendChild(dayDiv);
        });
    }
});

document.querySelectorAll('.rich-text-editor').forEach((textarea) => {
    CKEDITOR.replace(textarea.id);
});
document.addEventListener('DOMContentLoaded', () => {
    const itineraryContainer = document.getElementById('itinerary-container');
    const deleteIdsInput = document.getElementById('delete-itinerary-ids');
    const addItineraryButton = document.getElementById('add-itinerary');

    if (itineraryContainer && deleteIdsInput) {
        // Add new itinerary day only if the button exists
        if (addItineraryButton) {
            addItineraryButton.addEventListener('click', () => {
                const dayNumber = itineraryContainer.children.length;
                const newItinerary = document.createElement('div');
                newItinerary.classList.add('mb-3', 'itinerary-item');
                newItinerary.innerHTML = `
                    <label for="itinerary-day-${dayNumber}" class="form-label">Day ${dayNumber}</label>
                    <textarea id="itinerary-day-${dayNumber}" name="itinerary_day_${dayNumber}" class="form-control" required></textarea>
                    <button type="button" class="btn btn-danger remove-itinerary">Remove</button>
                `;
                itineraryContainer.appendChild(newItinerary);
            });
        }

        // Remove itinerary day functionality
        itineraryContainer.addEventListener('click', (event) => {
            if (event.target.classList.contains('remove-itinerary')) {
                const itineraryItem = event.target.closest('.itinerary-item');
                const itineraryId = itineraryItem.dataset.id;

                if (itineraryId) {
                    // Mark for deletion
                    deleteIdsInput.value += `${itineraryId},`;
                }
                itineraryContainer.removeChild(itineraryItem);
            }
        });
    }
});
