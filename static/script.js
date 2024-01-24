document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var uploadURL = document.getElementById('upload-url');
    uploadURL.textContent = 'Uploading...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        uploadURL.innerHTML = 'File URL: <a href="' + data + '" target="_blank">' + data + '</a>';
    })
    .catch(error => {
        console.error('Error:', error);
        uploadURL.textContent = 'Error uploading file.';
    });
});
