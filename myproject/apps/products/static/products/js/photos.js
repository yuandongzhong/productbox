$(function () {

  /*
    Image upload
  */

  $(".js-upload-photos").click(function () {
    $("#id_image_file").click();
  });

  /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
  $("#id_image_file").change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#image").attr("src", e.target.result);
        $("#modalCrop").modal("show");
      }
      reader.readAsDataURL(this.files[0]);
    }
  });

  /* SCRIPTS TO HANDLE THE CROPPER BOX */
  var $image = $("#image");
  var cropBoxData;
  var canvasData;
  $("#modalCrop").on("shown.bs.modal", function () {
    $image.cropper({
      viewMode: 1,
      aspectRatio: 1 / 1,
      minCropBoxWidth: 200,
      minCropBoxHeight: 200,
      ready: function () {
        $image.cropper("setCanvasData", canvasData);
        $image.cropper("setCropBoxData", cropBoxData);
      }
    });
  }).on("hidden.bs.modal", function () {
    cropBoxData = $image.cropper("getCropBoxData");
    canvasData = $image.cropper("getCanvasData");
    $image.cropper("destroy");
  });

  $(".js-zoom-in").click(function () {
    $image.cropper("zoom", 0.1);
  });

  $(".js-zoom-out").click(function () {
    $image.cropper("zoom", -0.1);
  })

  /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
  $(".js-crop-and-upload").click(function () {
    var cropData = $image.cropper("getData");
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    $("#formUpload").submit();
  });



  /*
    Image preview
  */

  var activatePhotoPreview = function () {
    $(".image-checkbox").each(function () {
      var checkbox = $(this);
      checkbox.find('img').first().on("click", function () {
        $('#imagepreview').attr('src', $(this).attr('src'));
        $('#modal-photo-preview').modal('show');
      });
    });
  }

  var deactivatePhotoPreview = function () {
    $(".image-checkbox").each(function () {
      var checkbox = $(this);
      checkbox.find('img').first().off('click');
    });
  }

  // Init the state when load
  activatePhotoPreview();



  /*
  Image checkbox
  */

  var selectionCount = function () {
    return $.find('input[type="checkbox"]:checked').length
  }

  // init the check state from the input
  $(".image-checkbox").each(function () {
    if ($(this).find('input[type="checkbox"]').first().attr("checked")) {
      $(this).addClass('image-checkbox-checked');
    } else {
      $(this).removeClass('image-checkbox-checked');
    }
  });

  var activateCheckbox = function () {
    // sync the check state to the input
    $(".image-checkbox").on("click", function (e) {
      $(this).toggleClass('image-checkbox-checked');
      var $checkbox = $(this).find('input[type="checkbox"]');
      $checkbox.prop("checked", !$checkbox.prop("checked"))

      if (selectionCount() > 0) {
        // activate delete button
        $('button.js-delete-photo').prop('disabled', false);
      } else {
        // disable delete button
        $('button.js-delete-photo').prop('disabled', true);
      }
      e.preventDefault();
    });
  }

  // Click event for photo edit button
  $(".js-edit-photo").on("click", function (e) {
    var editButton = $(this);
    editButton.hide();
    $(".delete-button-group").show();
    $(".image-checkbox").each(function () {
      $(this).find('input[type="checkbox"]').first().prop('disabled', false);
    });
    activateCheckbox();
    deactivatePhotoPreview();
    $("button.js-upload-photos").hide();
  });

  // Click event for cancel button
  $(".js-delete-photo-cancel").on("click", function (e) {
    cancelDeletion();
  });

  var cancelDeletion = function () {
    $(".delete-button-group").hide();
    $(".js-edit-photo").show();
    $('button.js-delete-photo').prop('disabled', true);
    // Remove click listener from clickbox
    $(".image-checkbox").off('click');
    // Show the upload button again
    $("button.js-upload-photos").show();
    $(".image-checkbox").each(function () {
      // Disable the checkbox
      $(this).find('input[type="checkbox"]').first().prop('disabled', true);
      // Remove the .image-checkbox-checked class
      $(this).removeClass('image-checkbox-checked');
      var $checkbox = $(this).find('input[type="checkbox"]');
      // Deselect all checked image
      $checkbox.prop("checked", false)
      // Assign the click event for photo preview again
      $(this).find('img').first().on("click", function () {
        $('#imagepreview').attr('src', $(this).attr('src'));
        $('#modal-photo-preview').modal('show');
      });
    });
  }

  // Get photo id from selected checkboxes
  var getPhotoList = function () {
    var photos = [];
    $.each($("input[type='checkbox']:checked"), function () {
      photos.push($(this).val());
    });
    return photos;
  }

  // Activate photo deletion confirmation
  $("#photo-container").on("click", ".js-delete-photo", function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('#modal-photo').modal("show");
      },
      success: function (data) {
        $('#modal-photo').find('.modal-content').first().html(data.html_form);
      }
    });
  });


  // Confirm the deletion
  $("#modal-photo").on("submit", ".js-photo-delete-form", function () {
    var form = $(this);
    var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    $.ajax({
      url: form.attr("action"),
      // data: form.serialize(),
      data: {
        'photos[]': getPhotoList(),
        'csrfmiddlewaretoken': csrfmiddlewaretoken
      },
      type: form.attr("method"),
      dataType: 'json',
      beforeSend: function () {},
      success: function (data) {
        if (data.success) {
          $("#photo-list").html(data.html_photo_list);
          $("#modal-photo").modal("hide");
          cancelDeletion();
        }
      }
    });
    return false;
  });

});