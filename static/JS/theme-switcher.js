document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const themeToggler = document.getElementById('theme-toggler');

    // Загрузка темы, если она была ранее сохранена
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        body.className = currentTheme;
    }
    themeToggler.addEventListener('click', () => {
        if (body.classList.contains('light-theme')) {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
        } else {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            localStorage.setItem('theme', 'light-theme');
        }
    });
});
