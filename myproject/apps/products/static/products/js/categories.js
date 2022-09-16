$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('#modal-category').modal("show");
      },
      success: function (data) {
        $('#modal-category .modal-content').html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $('#category-list').html(data.html_category_list);
          $("#modal-category").modal("hide");
        } else {
          $("#modal-category .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  }

  // Create category
  $(".js-create-category").click(loadForm);
  $("#modal-category").on("submit", ".js-category-create-form", saveForm);

  // Update category
  $("#category-list").on("click", ".js-update-category", loadForm)
  $("#modal-category").on("submit", ".js-category-update-form", saveForm);

  // Delete category
  $("#category-list").on("click", ".js-delete-category", loadForm)
  $("#modal-category").on("submit", ".js-category-delete-form", saveForm);

});