function uploadImage() {
    const fileInput = document.getElementById('fileInput');

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        outputImage.src = imageUrl;
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
}
