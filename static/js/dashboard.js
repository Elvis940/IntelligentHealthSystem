document.addEventListener("DOMContentLoaded", function () {
  // Sidebar toggle
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.querySelector(".sidebar");
  const mainContent = document.querySelector(".main-content");

  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function (e) {
      e.preventDefault();
      sidebar.classList.toggle("active");
      mainContent.classList.toggle("sidebar-hidden");
    });
  }

  // Responsive behavior
  function handleResize() {
    if (window.innerWidth < 768) {
      sidebar.classList.remove("active");
      mainContent.classList.remove("sidebar-hidden");
    }
  }

  window.addEventListener("resize", handleResize);
  handleResize();
});
