// Ocultar automáticamente los mensajes flash después de 3 segundos
window.setTimeout(function() {
    $(".alert").fadeTo(1500, 0).slideUp(0, function(){
        $(this).remove(); 
    });
}, 1500); // Tiempo en milisegundos (3 segundos)
