document.addEventListener("DOMContentLoaded", function () {
    let fileInput = document.querySelector("input[type='file']");
    let previewImg = document.getElementById("preview-img");

    if (fileInput) {
        fileInput.addEventListener("change", function (event) {
            let file = event.target.files[0];
            if (file) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = "block"; // Hiển thị ảnh
                };
                reader.readAsDataURL(file);
            } else {
                previewImg.style.display = "none"; // Ẩn ảnh nếu không có file
            }
        });
    }
});
