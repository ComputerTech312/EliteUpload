document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var uploadURL = '/upload'; // Update this to your upload URL

    var progressBar = document.getElementById('progress-bar');

    var request = new XMLHttpRequest();
    request.open('POST', uploadURL, true);

    request.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var percentComplete = (e.loaded / e.total) * 100;
            progressBar.style.width = percentComplete + '%';
        }
    };

    request.upload.onloadstart = function(e) {
        progressBar.style.width = '0%';
    };

    request.upload.onloadend = function(e) {
        progressBar.style.width = '100%';
    };

    request.send(formData);
});