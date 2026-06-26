// Function handles simple DOM node removal actions
function dropCourse(buttonElement) {
  // Confirm target choice validation rule
  const confirmation = confirm("Are you sure you want to drop this course?");

  if (confirmation) {
    // Traverse up the DOM tree node structures to remove the table row element
    const tableRow = buttonElement.parentElement.parentElement;
    tableRow.remove();

    // Dynamic status tracker variable recalculation metric update
    updateCourseCount();
  }
}

// Function updates active courses metric tracker node
function updateCourseCount() {
  const courseListContainer = document.getElementById("course-list");
  const metricDisplayContainer = document.getElementById("course-count");

  // Determine number of existing table rows left inside container
  const remainingRowsCount =
    courseListContainer.getElementsByTagName("tr").length;

  // Assign calculated figure directly into targeted dashboard card inner element
  metricDisplayContainer.textContent = remainingRowsCount;
}
