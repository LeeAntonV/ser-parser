const dropZone = document.getElementsByClassName('create-order')[0];
const fileInput = document.getElementById('file-input');
const uploadImage = document.getElementById('upload-image');
const uploadText = document.getElementById('upload-text');
const statusText = document.getElementById('status-text');

const handleDrop = (event, from) => {
    event.preventDefault();
    let file;
    if (from === "drop") {
        file = event.dataTransfer.files[0];
    } else if (from === "change") {
        file = event.target.files[0];
    }
    if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        console.log('File received:', file);
        document.querySelector('.load-title').style.display = 'none';
        document.querySelector('.load-process').style.display = 'block';
        statusText.textContent = "Загружен!"
        uploadImage.style.display = 'none';
        uploadText.style.display = 'none';
        sendFileToServer(file);
    } else {
        console.error('Error: Invalid file type. Please select a .xlsx file.');
    }
    document.querySelector('.load-success').style.display = 'none';
};

const resetFile = () => {
    fileInput.value = '';
    statusText.textContent = '';
    document.querySelector(".load-process").style.display = "none";
    document.querySelector(".load-success").style.display = "none";
    uploadImage.style.display = 'block';
    uploadText.style.display = 'block';
};

dropZone.addEventListener('dragover', event => {
    event.preventDefault();
});

dropZone.addEventListener('drop', event => {
    handleDrop(event, 'drop');
});

dropZone.addEventListener('click', () => {
    if (fileInput.value !== '') {
        resetFile();
    } else {
        fileInput.click();
    }
    document.querySelector('.load-success').style.display = 'none';
});

fileInput.addEventListener('change', event => {
    handleDrop(event, 'change');
    document.querySelector('.load-success').style.display = 'none';
});