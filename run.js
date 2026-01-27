async function uploadImage() {
    const [fileHandle] = await showOpenFilePicker({
        multiple: false,
        types: [{
            description: 'Images',
            accept: {
                'image/png': ['.png'],
                'image/gif': ['.gif'],
                'image/jpeg': ['.jpg', '.jpeg'],
            },
        }],
    });

    const file = await fileHandle.getFile();

    const reader = new FileReader();
    reader.onloadend = function () {
        const img = new Image();
        img.onload = function() {
            const myCanvas = document.getElementsByClassName('drawing-canvas')[0];
            const ctx = myCanvas.getContext('2d');
            const canvasWidth = myCanvas.width;
            const canvasHeight = myCanvas.height;

            ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);
            document.getElementsByClassName("drawing-btn--save")[0].click();
        };

        img.src = reader.result;
    };

    reader.readAsDataURL(file);
}

const username = JSON.parse(localStorage.getItem("nowkie_user"))["username"];

if (window.location.href !== `https://xn--d1ah4a.com/${username}`) {
    throw new Error('Ты находишься не на своей страничке. Перейти по ссылке https://итд.com/${username} для правильной работы скрипта');
} else {
    document.getElementsByClassName("profile-banner__btn")[0].click();
    uploadImage();
}
