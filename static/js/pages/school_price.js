$("#school_table").DataTable({
  ordering: true,
  columnDefs: [
    {
      orderable: false,
      targets: "no-sort"
    }
  ]
});

$("#submitBtn").click(function() {
  $("#lname").text($("#lastname").val());
  $("#fname").text($("#firstname").val());
});

$("#submit").click(function() {
  alert("submitting");
  $("#formfield").submit();
});

// Add & Remove Image
var counter = 1;
$("#addButton").click(function() {
  if (counter > 14) {
    alert("15 hz ot krob man?");
    return false;
  } else {
    counter++;
    $("<div/>", { id: "ImageDiv" + counter })
      .html(
        $('<input type="text" />').attr({
          id: "input_image" + counter,
          name: "input_image" + counter,
          class: "form-control",
          placeholder: "Image" + counter
        })
      )
      .appendTo("#ImageGroup");
  }
});

$("#removeButton").click(function() {
  if (counter < 2) {
    alert("Ot oy remove tt te, tuk 1 brother");
    return false;
  } else {
    $("#ImageDiv" + counter).remove();
    counter--;
  }
});

// End Add & Remove Image

// Add & Remove Stand Out Point En
var sop_en = 1;
$("#sop_en_add").click(function() {
  if (counter > 14) {
    alert("15 hz ot krob man?");
    return false;
  } else {
    counter++;
    $("<div/>", { id: "StandOutPointEnDiv" + counter })
      .html(
        $('<input type="text" />').attr({
          id: "input_image" + counter,
          name: "input_image" + counter,
          class: "form-control",
          placeholder: "Stand Out Point En" + counter
        })
      )
      .appendTo("#StandOutPointEnGroup");
  }
});

$("#sop_en_remove").click(function() {
  if (counter < 2) {
    alert("Ot oy remove tt te, tuk 1 brother");
    return false;
  } else {
    $("#StandOutPointEnDiv" + counter).remove();
    counter--;
  }
});
// End Add & Remove Stand Out Point En

// Add & Remove Stand Out Point Kh
var sop_en = 1;
$("#sop_kh_add").click(function() {
  if (counter > 14) {
    alert("15 hz ot krob man?");
    return false;
  } else {
    counter++;
    $("<div/>", { id: "StandOutPointKhDiv" + counter })
      .html(
        $('<input type="text" />').attr({
          id: "input_image" + counter,
          name: "input_image" + counter,
          class: "form-control",
          placeholder: "Stand Out Point Kh" + counter
        })
      )
      .appendTo("#StandOutPointKhGroup");
  }
});

$("#sop_kh_remove").click(function() {
  if (counter < 2) {
    alert("Ot oy remove tt te, tuk 1 brother");
    return false;
  } else {
    $("#StandOutPointKhDiv" + counter).remove();
    counter--;
  }
});
// End Add & Remove Stand Out Point Kh
