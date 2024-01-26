document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var uploadURL = document.getElementById('upload-url');
    uploadURL.textContent = 'Uploading...';

    var progressBar = document.getElementById('progress-bar'); // Assuming you have a progress bar element

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        const reader = response.body.getReader();
        const totalLength = +response.headers.get('Content-Length');

        reader.read().then(function process({done, value}) {
            if (done) {
                return uploadURL.innerHTML = 'File URL: <a href="' + data + '" target="_blank">' + data + '</a>';
            }

            progressBar.value += value.length;
            progressBar.max = totalLength;

            return reader.read().then(process);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        uploadURL.textContent = 'Error uploading file.';
    });
});