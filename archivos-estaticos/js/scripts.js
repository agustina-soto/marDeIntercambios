function confirmarBorrado(elemento) {
    if (confirm("¿Estás seguro de que deseas eliminar esta publicación?")) {
        var url = elemento.getAttribute('data-borrar-url');
        window.location.href = url;
    }
}