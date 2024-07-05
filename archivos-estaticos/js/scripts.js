function confirmarBorrado(elemento) {
    if (confirm("¿Estás seguro de que deseas eliminarla?")) {
        var url = elemento.getAttribute('data-borrar-url');
        window.location.href = url;
    }
}

/* para footer */
document.addEventListener('DOMContentLoaded', function() {
    window.addEventListener('scroll', function() {
        // Obtiene la posición del footer
        let footer = document.getElementById('footer');
        // let footerHeight = footer.offsetHeight;
        let scrollPosition = window.scrollY + window.innerHeight;

        // Muestra el footer cuando se hace scroll hasta abajo del contenido
        if (scrollPosition >= document.body.offsetHeight) {
            footer.style.display = 'block';
        } else {
            footer.style.display = 'none';
        }
    });
});


/* para fotos de realizar publicacion */

// Función para actualizar la lista de archivos seleccionados
function updateFileList(input) {
    var preview = document.getElementById('file-preview');
    preview.innerHTML = ''; // Limpiar la lista de archivos previa

    // Itera sobre los archivos seleccionados y agregarlos a la lista
    for (var i = 0; i < input.files.length; i++) {
        var file = input.files[i];
        var fileReader = new FileReader();

        fileReader.onload = (function(e) {
            var fileItem = document.createElement('div');
            fileItem.classList.add('photo-container');
            
            var img = document.createElement('img');
            img.src = e.target.result;
            img.alt = file.name;

            var deleteButton = document.createElement('span');
            deleteButton.textContent = 'x';
            deleteButton.className = 'eliminar-foto';
            deleteButton.onclick = function() {
                // Encuentra y elimina el contenedor de la foto al hacer clic en el botón
                var container = this.parentNode;
                container.parentNode.removeChild(container);
            };

            fileItem.appendChild(img);
            fileItem.appendChild(deleteButton);
            preview.appendChild(fileItem);
        });

        fileReader.readAsDataURL(file);
    }
}


// Arreglo para almacenar las IDs de las fotos que se quieren eliminar
var fotosAEliminar = [];

// Función para actualizar la lista de archivos seleccionados
function updateFileListEditar(input) {
    var preview = document.getElementById('file-preview');
    preview.innerHTML = '';

    var fileList = document.createElement('ul');
    fileList.classList.add('file-list');

    // Itera sobre los archivos seleccionados y los agrega a la lista de previsualización
    for (var i = 0; i < input.files.length; i++) {
        var fileItem = document.createElement('li');
        var fileName = input.files[i].name;
        fileItem.textContent = fileName;

        // Botón para eliminar la selección del archivo
        var deleteButton = document.createElement('button');
        deleteButton.textContent = 'x';
        deleteButton.className = 'eliminar-foto';
        deleteButton.onclick = function() {
            var container = this.parentNode;
            container.parentNode.removeChild(container);
        };

        fileItem.appendChild(deleteButton);
        fileList.appendChild(fileItem);
    }

    preview.appendChild(fileList);
}

// Función para actualizar el campo oculto con las IDs de las fotos a eliminar
function actualizarCampoFotosAEliminar() {
    var campoFotosAEliminar = document.getElementById('fotos-a-eliminar');
    campoFotosAEliminar.value = fotosAEliminar.filter(Boolean).join(',');
}

// Función para manejar la eliminación de una foto existente
function eliminarFoto(fotoContainer) {
    var fotoId = fotoContainer.getAttribute('data-id');
    
    // Confirmación antes de eliminar la foto
    if (confirm('¿Estás seguro de que quieres eliminar esta foto?')) {
        fotoContainer.remove();
        fotosAEliminar.push(fotoId);
        actualizarCampoFotosAEliminar();
    }
}

// Función para validar el formulario antes de enviarlo
function validarYEnviarFormulario(event) {
    var fotosRestantes = document.querySelectorAll('.photo-container').length;
    var nuevasFotos = document.getElementById('custom-file').files.length;

    // Verifica que haya al menos una foto
    if (fotosRestantes + nuevasFotos === 0) {
        event.preventDefault();
        alert('¡Debes subir por lo menos una foto!');
    }
}