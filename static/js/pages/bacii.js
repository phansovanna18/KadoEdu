$("#school_table").DataTable({
  ordering: true,
  columnDefs: [
    {
      orderable: false,
      targets: "no-sort"
    }
  ]
});
