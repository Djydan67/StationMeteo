

var temp = new XMLHttpRequest();
temp.open('GET', '/donnees', true);
temp.onreadystatechange = function () {
    if (temp.readyState == 4 && temp.status == 200) {
        var donnees = JSON.parse(temp.responseText);
        afficherDonnees(donnees);
    }
};
temp.send();

// Fonction pour afficher les données dans le conteneur HTML
function afficherDonnees(donnees) {
    var donneesContainer = document.getElementById('AfficheTemp');

    // Créer une liste pour afficher les données
    var liste = document.createElement('ul');

    // Parcourir les données et créer un élément de liste pour chaque entrée
    donnees.forEach(function (donnee) {
        var item = document.createElement('li');
        item.textContent = 'Temperature: ' + donnee.temperature + ', Humidite: ' + donnee.humidite;
        liste.appendChild(item);
    });

    // Ajouter la liste au conteneur
    donneesContainer.appendChild(liste);
}

//var ctx = document.getElementById("lineChart").getContext("2d");
//var lineChart = new Chart(ctx, {
//    type: "line",
//    data: {
//        labels: {{ labels_temperature | safe }},
//datasets: [
//    {
//        label: "Temperature",
//        data: {{ values_temperature | safe }},
//    fill: false,
//    borderColor: "rgb(75, 192, 192)",
//    lineTension: 0.1
//                },
//    {
//        label: "Humidity",
//        data: {{ values_humidite | safe }},
//    fill: false,
//    borderColor: "rgb(192, 75, 192)",
//    lineTension: 0.1
//                }
//]
//            },
//option: {
//    responsive: false
//}
//         });       
