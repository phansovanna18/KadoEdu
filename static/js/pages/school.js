$("#school_table").DataTable({
  ordering: true,
  columnDefs: [
    {
      orderable: false,
      targets: "no-sort"
    }
  ]
});

// $("#submitBtn").click(function() {
//   $("#lname").text($("#lastname").val());
//   $("#fname").text($("#firstname").val());
// });

$("#submit").click(function() {
  // alert("submitting");
  $("#formfield").submit();
});
// Add & Remove Stand Out Point En
var sop = 1;
$("#sop_add").click(function() {
  if (sop > 14) {
    alert("15 hz ot krob man?");
    return false;
  } else {
    sop++;
    $("#StandOutPointGroup").append(
      '<div id="StandOutPointDiv' +
        sop +
        '"><input name="stand_point_en' +
        sop +
        '" type="text" class="form-control" placeholder="Stand Out Point En"/><input name="stand_point_kh' +
        sop +
        '" type="text" class="form-control" placeholder="Stand Out Point kh"/></div>'
    );
  }
});

$("#sop_remove").click(function() {
  if (sop < 2) {
    alert("Ot oy remove tt te, tuk 1 brother");
    return false;
  } else {
    $("#StandOutPointDiv" + sop).remove();
    sop--;
  }
});

var image = 1;
$("#image_add").click(function() {
  if (image > 14) {
    alert("15 hz ot krob man?");
    return false;
  } else {
    image++;
    $("#ImageGroup").append(
      '<div id="ImageDiv' +
        image +
        '"><input name="image' +
        image +
        '" type="text" class="form-control" placeholder="Image' +
        image +
        '"/></div>'
    );
  }
});

$("#image_remove").click(function() {
  if (image < 2) {
    alert("Ot oy remove tt te, tuk 1 brother");
    return false;
  } else {
    $("#ImageDiv" + sop).remove();
    image--;
  }
});
// End Add & Remove Stand Out Point En
