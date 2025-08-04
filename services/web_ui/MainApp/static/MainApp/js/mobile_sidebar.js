let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
});
document.addEventListener('touchend', function (e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const sidebar = document.getElementById('mobile-sidebar');
    const deltaX = touchEndX - touchStartX;

    if (deltaX > 100) {
        sidebar.classList.add('active');
    }
    if (deltaX < -100) {
        sidebar.classList.remove('active');
    }
}

function toggleSidebar() {
    document.getElementById("mobile-sidebar").classList.toggle("active");
}