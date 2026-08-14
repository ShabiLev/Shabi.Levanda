(() => {
  const toggle = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-navigation");
  const header = document.querySelector("[data-header]");

  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!toggle || !navigation) return;
    toggle.setAttribute("aria-expanded", "false");
    toggle.querySelector(".sr-only").textContent = "Open navigation";
    navigation.classList.remove("open");
    document.body.classList.remove("menu-open");
    if (restoreFocus) toggle.focus();
  };

  toggle?.addEventListener("click", () => {
    const willOpen = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(willOpen));
    toggle.querySelector(".sr-only").textContent = willOpen
      ? "Close navigation"
      : "Open navigation";
    navigation.classList.toggle("open", willOpen);
    document.body.classList.toggle("menu-open", willOpen);
  });

  navigation?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });

  const desktopViewport = window.matchMedia("(min-width: 761px)");
  desktopViewport.addEventListener("change", (event) => {
    if (event.matches) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      toggle?.getAttribute("aria-expanded") === "true"
    )
      closeMenu({ restoreFocus: true });
  });

  const onScroll = () =>
    header?.classList.toggle("scrolled", window.scrollY > 12);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
