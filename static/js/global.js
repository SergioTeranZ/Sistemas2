/*
  - Descripción:
        permite mostrar, y calcular, cuantos caracteres quedan disponible en un
        textfield/textarea.

  - Parámetros:
        @param maxLong  : número máximo de caracteres a utilizar.
        @param idDivUsar: identificador del div donde se mostrára el texto.
*/
function textoRestante(maxLong, idDivUsar){
  var longitudTexto = $(idDivUsar).val().length;
  var textoRestante = maxLong - longitudTexto;

  // Selecciono el div que es "hermano" del textfield de nombre.
  var longitudTextoAct = $(idDivUsar).val().length;
  $(idDivUsar).siblings(".help-block").html((maxLong - longitudTextoAct) + " caracteres");
  $(idDivUsar).siblings(".help-block").css("text-align","center");

  // Si estoy escribiendo en el textfield de nombre, entonces...
  $(idDivUsar).on('keypress keyup keydown', function(e){
    var longitudTexto = $(idDivUsar).val().length;
    var textoRestante = maxLong - longitudTexto;

    $(idDivUsar).siblings(".help-block").html(textoRestante + " caracteres.");

    /* keyCode.46: delete, keyCode.8: enter, keyCode.37 al keyCode.40: arrows. */
    if (textoRestante <= 0 && e.keyCode != 46 && e.keyCode != 8 && e.keyCode != 37
        && e.keyCode != 38 && e.keyCode != 39 && e.keyCode != 40){
          $(idDivUsar).val($(idDivUsar).val().substring(0, maxLong));
          return false;
    }
  });
}
