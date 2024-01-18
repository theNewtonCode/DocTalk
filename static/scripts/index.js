function dragOverHandler(event) {
    event.preventDefault();
    document.getElementById('drop-area').style.border = '2px dashed #4CAF50';
}

function dropHandler(event) {
    event.preventDefault();
    document.getElementById('drop-area').style.border = '2px dashed #4CAF50';

    var files = event.dataTransfer.files;
    handleFile(files);

    // Show "Ask the Doc" button after successful upload
    document.getElementById('ask-doc-btn').style.display = 'block';
    document.getElementById('try-new-btn').style.display = 'block';

}

function handleFile(files) {
    var fileInput = document.getElementById('file-input');
    fileInput.files = files;

    // Submit the form to the Flask endpoint
    var formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(message => alert(message))
    .catch(error => console.error('Error:', error));
}

const urlParams = new URLSearchParams(window.location.search);
const completed = urlParams.get('completed');

if (completed === 'true') {
    // If 'completed' is true, hide the "Ask the Doc" button and show the "Let's QA" button
    document.getElementById('ask-doc-btn').style.display = 'none';
    document.getElementById('lets-qa-btn').style.display = 'block';
    document.getElementById('try-new-btn').style.display = 'block';
} else {
    // If 'completed' is not present or false, show the "Ask the Doc" button
    // document.getElementById('ask-doc-btn').style.display = 'none';
    document.getElementById('lets-qa-btn').style.display = 'none';
    document.getElementById('try-new-btn').style.display = 'none';

}

function askTheDoc() {
    // Show loading bar
    document.getElementById('loading-bar').style.display = 'block';

    // Call the Flask route/function for "Ask the Doc"
    fetch('/ask-doc', {
        method: 'GET'
    })
    .then(response => response.text())
    .then(message => {
        alert(message);
        // Hide loading bar on completion
        document.getElementById('loading-bar').style.display = 'none';

        // Update the URL to include 'completed=true'
        window.history.replaceState({}, document.title, "/?completed=true");

        // Hide "Ask the Doc" button and show "Let's QA" button
        document.getElementById('ask-doc-btn').style.display = 'none';
        document.getElementById('lets-qa-btn').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading bar on error
        document.getElementById('loading-bar').style.display = 'none';
    });
}

function navigateToLetsQA() {
    // Redirect to the "/lets-qa" route
    window.location.href = '/lets-qa';
}

function tryNewDoc() {
    // Clear all search parameters and redirect to 'index.html'
    window.location.href = '/';
}
