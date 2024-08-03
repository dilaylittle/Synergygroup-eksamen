document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.remove('hidden');
    setTimeout(function() {
        document.querySelector('.container').classList.add('show');
    }, 10); // Short delay to ensure CSS transition is applied
});
