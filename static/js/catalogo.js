$(document).ready(function(){
  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Definición del comportamiento del botón agregar programa cuando se hace click.
  $("#agregarCatalogoBtn").click(function(){
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  "#no_table_nombre");
  });

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      $("#agregarCatalogoBtn").click();        // Abre el modal (da click en el botón agregar).
      $(".error_wrapper").css('color','red');  // Se pone el error en rojo.
  }
});
