
window.addEventListener('scroll', function () {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});


document.querySelectorAll('.nav-item a').forEach(item => {
    item.addEventListener('mouseenter', function () {
        this.style.color = '#4caf50';
    });
    item.addEventListener('mouseleave', function () {
        this.style.color = '';
    });
    
    item.addEventListener('click', function (e) {
        document.querySelectorAll('.nav-item a').forEach(link => {
            link.classList.remove('active-nav');
        });
        this.classList.add('active-nav');
    });
});
