// JavaScript source code
<script>
    function shareOnTwitter() {
        getTemperatureDataToShare();
    }


    function getTemperatureDataToShare() {
        // Effectuer une requ�te � l'API Flask pour obtenir les donn�es de temp�rature
        fetch('/api/temperature/share')
            .then(response => response.json())
            .then(data => {
                // Les donn�es sont maintenant disponibles dans la variable 'data'
                console.log('Donn�es de temp�rature:', data);

                // Construire le message � partager sur Twitter
                data.forEach(function (entry, index) {
                    // Utilise seulement la premi�re entr�e
                    if (index === 0) {
                        var tweet = `Derni�res donn�es de temp�rature:\n${entry.Date}: Temp�rature ${entry.Temperature}�C, Humidit� ${entry.Humidite}%`;

                        // URL de partage sur Twitter avec le message
                        var twitterShareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweet)}`;

                        // Ouvrir une nouvelle fen�tre pour le partage sur Twitter
                        var twitterWindow = window.open(twitterShareUrl, '_blank');

                        // V�rifier si la fen�tre a �t� ouverte avec succ�s
                        if (twitterWindow) {
                            // Message de r�ussite
                            alert("Donn�es partag�es sur Twitter avec succ�s !");
                        } else {
                            // Message d'�chec
                            alert("�chec de l'ouverture de la fen�tre de partage sur Twitter. Assurez-vous que les pop-ups ne sont pas bloqu�s.");
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Erreur lors de la r�cup�ration des donn�es de temp�rature:', error);
                // Message d'erreur en cas d'�chec
                alert("Erreur lors de la r�cup�ration des donn�es de temp�rature. Veuillez r�essayer.");
            });
}


</script>
// JavaScript source code
