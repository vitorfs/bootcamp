$(function () {

    /*  ==========================================
   Profile photo upload with JCrop
   * ========================================== */
    var jcrop_api,
        boundx,
        boundy,
        xsize = 200,
        ysize = 200;

    $("#crop-picture").Jcrop({
        aspectRatio: xsize / ysize,
        onSelect: updateCoords,
        setSelect: [0, 0, 200, 200]
    }, function () {
        var bounds = this.getBounds();
        boundx = bounds[0];
        boundy = bounds[1];
        jcrop_api = this;
    });

    function updateCoords(c) {
        $("#x").val(c.x);
        $("#y").val(c.y);
        $("#w").val(c.w);
        $("#h").val(c.h);
    };

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#crop-picture').attr('src', e.target.result);
                 $("#modal-upload-picture").modal();
                 // window.history.pushState("", "", "/picture/");
            };
            reader.readAsDataURL(input.files[0]);
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

    // $("#btn-upload-picture").click(function () {
    //     readURL(input)
    //     $("#modal-to-show").show();
    // });

    $("#picture-upload-form input[name='picture']").change(function () {
        $("#picture-upload-form").submit();
    });

});
