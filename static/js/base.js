document.addEventListener("DOMContentLoaded", function () {
  // Sidebar toggle functionality
  const sidebarCollapse = document.getElementById("sidebarCollapse");
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");

  if (sidebarCollapse) {
    sidebarCollapse.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");
      content.classList.toggle("expanded");
    });
  }

  // Submenu toggle functionality
  const submenuToggles = document.querySelectorAll(
    '[data-bs-toggle="collapse"]'
  );
  submenuToggles.forEach((toggle) => {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      const submenuId = this.getAttribute("href");
      const submenu = document.querySelector(submenuId);
      const icon = this.querySelector(".fas.fa-chevron-down");

      if (submenu) {
        submenu.classList.toggle("show");
        if (icon) {
          icon.style.transform = submenu.classList.contains("show")
            ? "rotate(180deg)"
            : "rotate(0)";
        }
      }
    });
  });

  // Responsive behavior
  function handleResize() {
    if (window.innerWidth < 768) {
      sidebar.classList.add("collapsed");
      content.classList.add("expanded");
    }
  }

  window.addEventListener("resize", handleResize);
  handleResize();
});
