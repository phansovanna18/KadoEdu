// $("#submit").click(function() {
//   $("#form_insert_subject").submit();
// });


$("#school_table").DataTable({
  ordering: true,
  columnDefs: [
    {
      orderable: false,
      targets: "no-sort"
    }
  ]
});
