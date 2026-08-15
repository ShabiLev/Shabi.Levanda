const header = document.querySelector("[data-header]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const mobileNavigation = document.querySelector("[data-mobile-nav]");
const desktopBreakpoint = window.matchMedia("(min-width: 1041px)");

const setMenuState = (open, { restoreFocus = false } = {}) => {
  if (!menuToggle || !mobileNavigation) return;

  menuToggle.setAttribute("aria-expanded", String(open));
  const openLabel = menuToggle.dataset.menuOpenLabel || "Open navigation menu";
  const closeLabel = menuToggle.dataset.menuCloseLabel || "Close navigation menu";
  menuToggle.setAttribute("aria-label", open ? closeLabel : openLabel);
  mobileNavigation.classList.toggle("open", open);
  header?.classList.toggle("menu-active", open);
  document.body.classList.toggle("menu-open", open);

  if (restoreFocus) menuToggle.focus();
};

const updateHeader = () => {
  header?.classList.toggle("scrolled", window.scrollY > 10);
};

menuToggle?.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  setMenuState(!isOpen);
});

mobileNavigation?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setMenuState(false));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuToggle?.getAttribute("aria-expanded") === "true") {
    setMenuState(false, { restoreFocus: true });
  }
});

desktopBreakpoint.addEventListener("change", (event) => {
  if (event.matches) setMenuState(false);
});

window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

const year = document.querySelector("[data-year]");
if (year) year.textContent = String(new Date().getFullYear());
