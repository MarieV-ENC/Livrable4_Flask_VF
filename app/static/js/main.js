// Déclenche l'animation du faucon lors d'un changement de page
document.querySelectorAll('a').forEach(function(link) {

    link.addEventListener('click', function(event) {

        // Ignorer les liens externes, ancres ou onglets
        if (
            link.target === "_blank" ||
            link.href.includes('#') ||
            link.href.startsWith('javascript:')
        ) {
            return;
        }

        event.preventDefault();

        const faucon = document.getElementById('faucon');
        const page = document.getElementById('page');

        // Lance le vol du faucon
        faucon.classList.add('fly');

        // Ajoute le flou sur le contenu
        page.classList.add('page-transition');

        // Attend la fin de l'animation avant de changer de page
        setTimeout(function() {
            window.location.href = link.href;
        }, 2200);
    });
});