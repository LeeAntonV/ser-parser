const sendFileToServer = async (file) => {
    try {
        const url = 'http://127.0.0.1:8000/parser'; // вбейте туда свои url, например http://localhost:8000/parsing

        let formData = new FormData();
        formData.append('upload_file', file);

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error uploading file to server');
        }
        const data = await response.blob();
        const updatedData = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        console.log('File received from server:', updatedData);

        const fileURL = window.URL.createObjectURL(updatedData);
        console.log('File URL:', fileURL);

        document.querySelector('.load-process').style.display = 'none';
        document.querySelector('.load-success').style.display = 'flex';
        document.querySelector(".load").style.cursor = "pointer"
        const downloadLink = document.getElementById('download-link');
        downloadLink.href = fileURL;
        downloadLink.download = 'output.xlsx';
    } catch (error) {
        console.error('Error uploading file to server:', error);
        document.querySelector('.load-process').style.display = 'none';
        document.querySelector('.load-title').textContent = 'Ошибка при загрузке файла';
        document.querySelector('.load-title').style.display = 'block';
    }
};

window.sendFileToServer = sendFileToServer
export { sendFileToServer } 