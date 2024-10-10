var enlaceId = null;

// Función para abrir el modal y obtener las listas
function openModal(id) {
    enlaceId = id; // Guardar el id del enlace

    // Obtener las listas del usuario (excluyendo las que ya contienen el enlace)
    fetch(`/obtener_listas/${enlaceId}`)  // Incluir enlaceId en la URL
        .then(response => response.json())
        .then(listas => {
            const selectLista = document.getElementById('lista_id'); // Asegúrate de que el ID sea correcto
            selectLista.innerHTML = '<option value="">Selecciona una lista</option>'; // Limpiar el select

            if (listas.length === 0) {
                selectLista.innerHTML += '<option value="" disabled>No tienes listas disponibles</option>';
            } else {
                listas.forEach(lista => {
                    selectLista.innerHTML += `<option value="${lista.id}">${lista.nombre}</option>`;
                });
            }

            // Mostrar el modal
            $('#modalAgregarLista').modal('show');

            // Manejar el evento submit del formulario
            const form = document.getElementById('agregarAListaForm');
            form.onsubmit = function(event) {
                event.preventDefault();
                const listaId = selectLista.value;
                agregarEnlaceALista(enlaceId, listaId);
            };
        })
        .catch(error => console.error('Error al obtener las listas:', error));
}

// Función para agregar el enlace a la lista seleccionada
function agregarEnlaceALista() {
    var listaId = $('#lista_id').val();

    if (!listaId) {
        alert("Selecciona una lista para agregar el enlace.");
        return;
    }

    // Hacer una solicitud AJAX para agregar el enlace a la lista
    $.ajax({
        url: '/agregar_enlace_a_lista_ajax',
        method: 'POST',
        data: {
            enlace_id: enlaceId,
            lista_id: listaId
        },
        success: function(response) {
            // Cerrar el modal actual y abrir el modal de éxito
            $('#modalAgregarLista').modal('hide');
            $('#modalExito').modal('show');
        },
        error: function(error) {
            console.log(error);
            alert("Hubo un error al agregar el enlace a la lista");
        }
    });
}
