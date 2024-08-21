document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger-menu');
    const navUL = document.querySelector('nav ul');

    // Menü umschalten bei Klick auf das Hamburger-Icon
    hamburger.addEventListener('click', () => {
        navUL.classList.toggle('nav-active');
    });

    // Menü schließen bei Klick auf einen Menüpunkt
    navUL.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
            navUL.classList.remove('nav-active');
        }
    });

    // Menü schließen bei Klick außerhalb des Menüs
    document.addEventListener('click', (e) => {
        if (!hamburger.contains(e.target) && !navUL.contains(e.target)) {
            navUL.classList.remove('nav-active');
        }
    });
});
