$(function () {

  $.fn.markdown = function () {
    var _textarea = $(this);

    $(".markdown .btn-group button").click(function (e) {
      e.preventDefault();
      var action = $(this).attr("ref");
      var selection = $(_textarea).selection();

      switch (action) {
        case "header":
          $(_textarea).selection("replace", {text: "# " + selection});
          break;
        case "bold":
          $(_textarea).selection("replace", {text: "**" + selection + "**"});
          break;
        case "italic":
          $(_textarea).selection("replace", {text: "_" + selection + "_"});
          break;
        case "list":
          var selection_list = selection.split("\n");
          var selection_list_result = "";
          for (var i = 0 ; i < selection_list.length ; i++) {
            selection_list_result += "* " + selection_list[i] + "\n";
          };
          if (selection_list_result.length > 0) {
            selection_list_result = selection_list_result.substring(0, selection_list_result.length - 1);
          }
          $(_textarea).selection("replace", {text: selection_list_result});
          break;
        case "link":
          $("#markdown_link_text").val("");
          $("#markdown_url").val("");
          $("#markdown_insert_link").modal("show");
          break;
        case "picture":
          $("#markdown_picture_url").val("");
          $("#markdown_alt_text").val("");
          $("#markdown_insert_picture").modal("show");
          break;
        case "indent-left":
          var selection_list = selection.split("\n");
          var selection_list_result = "";
          for (var i = 0; i < selection_list.length; i++) {
            selection_list_result += "    " + selection_list[i] + "\n";
          };
          if (selection_list_result.length > 0) {
            selection_list_result = selection_list_result.substring(0, selection_list_result.length - 1);
          }
          $(_textarea).selection("replace", {text: selection_list_result});
          break;
        case "indent-right":
          var selection_list = selection.split("\n");
          var selection_list_result = "";
          for (var i = 0; i < selection_list.length ; i++) {
            selection_list_result += selection_list[i].trim() + "\n";
          };
          if (selection_list_result.length > 0) {
            selection_list_result = selection_list_result.substring(0, selection_list_result.length - 1);
          }
          $(_textarea).selection("replace", {text: selection_list_result});
          break;
      }

    });

    $(".add_link").click(function () {
      var selection = $(_textarea).selection();
      var text = $("#markdown_link_text").val();
      var url = $("#markdown_url").val();
      var link = "[" + text + "](" + url + ")";
      $(_textarea).selection("replace", {text: link});
      $("#markdown_insert_link").modal("hide")
    });

    $(".add_picture").click(function () {
      var selection = $(_textarea).selection();
      var url = $("#markdown_picture_url").val();
      var alt = $("#markdown_alt_text").val();
      var picture = "![" + alt + "](" + url + ")";
      $(_textarea).selection("replace", {text: picture});
      $("#markdown_insert_picture").modal("hide")
    });

  };
});