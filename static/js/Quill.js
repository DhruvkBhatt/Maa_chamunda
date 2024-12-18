document.addEventListener('DOMContentLoaded', function () {
    const editors = {
        description: new Quill('#description-editor', { theme: 'snow' }),
        highlights: new Quill('#highlights-editor', { theme: 'snow' }),
        inclusions: new Quill('#inclusions-editor', { theme: 'snow' }),
        exclusions: new Quill('#exclusions-editor', { theme: 'snow' }),
        itinerary: new Quill('#itinerary-editor', { theme: 'snow' })
    };

    // For form submission, populate hidden fields with editor contents
    document.querySelector('#add-package-form').addEventListener('submit', function () {
        for (const [key, editor] of Object.entries(editors)) {
            const input = document.querySelector(`#${key}`);
            input.value = editor.root.innerHTML; // Get HTML content
        }
    });
});
