const links = document.querySelectorAll(".nav-link")

links.forEach(link => {
    link.addEventListener('click', e => {
        document.querySelector('.nav-link.active').classList.remove('active')
        e.currentTarget.classList.add('active')
    })
})