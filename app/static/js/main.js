// main.js

// Cuando la página esté completamente cargada
window.onload = function() {
    // Obtén el modal
    var modal = document.getElementById('createPostModal');

    // Obtén el botón que abre el modal
    var btn = document.querySelector('button[data-target="createPostModal"]');

    // Obtén el elemento <span> que cierra el modal
    var span = document.getElementsByClassName("close")[0];

    // Cuando el usuario haga clic en el botón, abre el modal 
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // Cuando el usuario haga clic en <span> (x), cierra el modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Cuando el usuario haga clic en cualquier lugar fuera del modal, cierra el modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
function openModal() {
    document.getElementById('editProfileModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('editProfileModal').style.display = 'none';
}
