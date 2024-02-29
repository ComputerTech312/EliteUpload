window.onload = function() {
    document.getElementById('upload-form').addEventListener('submit', function(e) {
        e.preventDefault();

        var form = e.target;
        var xhr = new XMLHttpRequest();
        var formData = new FormData(form);

        xhr.open(form.method, form.action);
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                var percentComplete = (e.loaded / e.total) * 100;
                var progressBar = document.getElementById('progress-bar');

                progressBar.style.width = percentComplete + '%';
                progressBar.textContent = percentComplete + '%';
            }
        });

        // Add an event listener for the 'load' event
        xhr.addEventListener('load', function() {
            if (xhr.status >= 200 && xhr.status < 400) {
                // The request has been completed successfully
                var response = JSON.parse(xhr.responseText);

                // Display the file URL
                alert('File uploaded successfully. URL: ' + response.file_url);
            } else {
                // There was an error with the request
                alert('An error occurred during the file upload.');
            }
        });

        xhr.send(formData);
    });
};