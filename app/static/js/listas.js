function cargarEnlaces(listaId) {
    // Hacer la solicitud AJAX para obtener los enlaces de la lista
    $.ajax({
        url: '/obtener_enlaces_lista/' + listaId,
        method: 'GET',
        success: function(response) {
            // Limpiar el contenido existente en el ul
            $('#listaEnlaces' + listaId).empty();
            
            // Si no hay enlaces, mostrar un mensaje
            if (response.length === 0) {
                $('#listaEnlaces' + listaId).append('<li class="list-group-item">No hay enlaces en esta lista.</li>');
            } else {
                // Llenar el ul con los enlaces obtenidos
                response.forEach(function(enlace) {
                    $('#listaEnlaces' + listaId).append(
                        '<li class="list-group-item d-flex justify-content-between align-items-center">' +
                        '<a href="' + enlace.href + '" target="_blank" class="text-decoration-none text-dark"><strong>' + enlace.titulo + '</strong> (' + enlace.categoria + ')</a>' +
                        '<button class="btn btn-danger btn-sm ml-auto" onclick="eliminarEnlaceDeLista(' + enlace.id + ', ' + listaId + ')"><i class="fas fa-times"></i></button>' +
                        '</li>'
                    );
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function eliminarEnlaceDeLista(enlaceId, listaId) {
    // Hacer la solicitud AJAX para eliminar el enlace de la lista
    $.ajax({
        url: '/eliminar_enlace_lista',
        method: 'POST',
        data: { enlace_lista_id: enlaceId },
        success: function(response) {
            // Recargar la lista de enlaces para esa lista
            cargarEnlaces(listaId);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
