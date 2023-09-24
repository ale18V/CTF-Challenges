imageInput = document.getElementById('imageInput');
imageInput.onchange = evt => {
    const [file] = imageInput.files
    if (file) {
        let imageContainer = document.getElementById('uploadedImage');
        imageContainer.style.display = 'block';
        imageContainer.children[0].setAttribute('src', URL.createObjectURL(file));
    }
}