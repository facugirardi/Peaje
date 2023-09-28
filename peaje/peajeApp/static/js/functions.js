//Funcion para ocultar el mensaje de error o exito ingresado por el usuario
setTimeout(function() {
    var messages = document.querySelectorAll('.messages li');
    messages.forEach(function(message) {
        message.style.display = 'none';
    });
}, 1500);