const menuLinks = document.querySelectorAll(".nav-options a");
const hamburgerMenu = document.querySelector("#hamburguer-menu");
const navOptions = document.querySelector(".nav-options");
const navBar = document.querySelector(".navbar");

function clickToCopy() {
  console.log("click");
}
function getDistanceFromTop(element) {
  const id = element.getAttribute("href");
  return document.querySelector(id).offsetTop;
}

function smoothScroll(getDistanceFromTop) {
  window.scroll({
    top: getDistanceFromTop,
    behavior: "smooth",
  });
}
function scrollToSection(event) {
  event.preventDefault();
  const distanceFromTop = getDistanceFromTop(event.target) - 100;
  smoothScroll(distanceFromTop);
}

function showMenu() {
  navBar.classList.toggle("navbar-mobile");
}

hamburgerMenu.addEventListener("click", showMenu);
menuLinks.forEach((link) => {
  link.addEventListener("click", scrollToSection);
});
