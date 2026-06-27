document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const role = params.get("role");
  const roleSelect = document.getElementById("role");
  if (roleSelect && role) {
    roleSelect.value = role;
  }
});
