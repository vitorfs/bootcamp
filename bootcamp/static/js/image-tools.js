$(function () {

    var removeImage = document.getElementById('removeImage');
    removeImage.addEventListener('click', resetImage);
    function resetImage() {
        $('#imageResult').attr('src', '');
        removeImage.hidden = true
    }

    /*  ==========================================
    SHOW UPLOADED IMAGE
    * ========================================== */

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#imageResult')
                    .attr('src', e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
            removeImage.hidden = false
        }
    }

    $(function () {
        $('#imageInput').on('change', function () {
            readURL(input);
        });
    });

    /*  ==========================================
        SHOW UPLOADED IMAGE NAME
    * ========================================== */
    var input = document.getElementById('imageInput');
    var infoArea = document.getElementById('upload-label');
    input.addEventListener('change', showFileName);

    function showFileName(event) {
        var input = event.srcElement;
        var fileName = input.files[0].name;
        infoArea.textContent = 'File name: ' + fileName;
    }

});