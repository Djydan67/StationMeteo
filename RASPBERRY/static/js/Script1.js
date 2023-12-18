// JavaScript source code
<script>
    function shareOnTwitter() {
        getTemperatureDataToShare();
    }


    function getTemperatureDataToShare() {
        // Effectuer une requête à l'API Flask pour obtenir les données de température
        fetch('/api/temperature/share')
            .then(response => response.json())
            .then(data => {
                // Les données sont maintenant disponibles dans la variable 'data'
                console.log('Données de température:', data);

                // Construire le message à partager sur Twitter
                data.forEach(function (entry, index) {
                    // Utilise seulement la première entrée
                    if (index === 0) {
                        var tweet = `Dernières données de température:\n${entry.Date}: Température ${entry.Temperature}°C, Humidité ${entry.Humidite}%`;

                        // URL de partage sur Twitter avec le message
                        var twitterShareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweet)}`;

                        // Ouvrir une nouvelle fenêtre pour le partage sur Twitter
                        var twitterWindow = window.open(twitterShareUrl, '_blank');

                        // Vérifier si la fenêtre a été ouverte avec succès
                        if (twitterWindow) {
                            // Message de réussite
                            alert("Données partagées sur Twitter avec succès !");
                        } else {
                            // Message d'échec
                            alert("Échec de l'ouverture de la fenêtre de partage sur Twitter. Assurez-vous que les pop-ups ne sont pas bloqués.");
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des données de température:', error);
                // Message d'erreur en cas d'échec
                alert("Erreur lors de la récupération des données de température. Veuillez réessayer.");
            });
}


</script>
// JavaScript source code
