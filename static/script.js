document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var fileInput = document.getElementById('file-input');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var request = new XMLHttpRequest();
    request.open('POST', '/upload', true);

    request.onerror = function() {
        console.log('Error: ', request.statusText);
    };

    request.send(formData);
});