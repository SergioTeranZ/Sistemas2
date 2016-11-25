$(document).ready(function(){

  var maxLongNombre  = 50;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.
  var maxLongCodigo = 10;      // Longitud máxima que tendrá el campo código.
  var hayPrograma = $(".formularioTipo").attr("data-hayPrograma");

  // Muestra la cantidad de caracteres disponible en el textfield de nombre.
  textoRestante(maxLongNombre,  "#no_table_Nombre");

  // Muestra la cantidad de caracteres disponible en el textarea de descripción.
  textoRestante(maxLongDescrip, "#no_table_Descripcion");

  // Muestra la cantidad de caracteres disponible en el textfield de código.
  textoRestante(maxLongCodigo, "#no_table_Codigo");

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de editar.
  var mensajeErrorEditar = $("#modalEditar").attr("data-hayErroresEditar");
  mensajeErrorEditar = mensajeErrorEditar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Si no existe un programa, entonces no debería mostrarse el formulario.
  if (!hayPrograma)
  {
    $(".formularioTipo").hide();
  }

   // Pasamos los argumentos para eliminar catalogo.
  $('#myModalDelete').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-tipo');
      $("#BotonEliminar").attr("href", linkEliminar);
  });


  // Eliminar definitivamente
  $('#myModalDelete').on('show.bs.modal', function (event) {
    if (event.relatedTarget != null){
      $("#botonDelete").attr("data-id-tipo", event.relatedTarget.getAttribute("data-id-tipo"));
    }
  });

  $('#myModalInhabilitar').on('show.bs.modal', function(e){
    var enlace = $(e.relatedTarget).data('enlace-inhabilitar');
    $("#botonDelete").attr("href", enlace );
  });

  $('#myModalEditar').on('show.bs.modal', function(e){
    var id_tipo = $(e.relatedTarget).data('idtipo');
    var nombre      = $(e.relatedTarget).data('nombre');
    var codigo      = $(e.relatedTarget).data('codigo');
    var descripcion = $(e.relatedTarget).data('descripcion');
    var id_programa = $(e.relatedTarget).data('idprograma');
    var tipoPR =  $(e.relatedTarget).data('tipopr');
    $(e.currentTarget).find('input[name="Id_tipo"]').val(id_tipo);
    localStorage.setItem("tipoActividadEditar", id_tipo);
    $("#no_table_Id_tipo__row").css("display","none");
    $(e.currentTarget).find('input[name="Nombre"]').val(nombre);
    $(e.currentTarget).find('input[name="Codigo"]').val(codigo);
    $(e.currentTarget).find('textarea[name="Descripcion"]').val(descripcion);
    $(e.currentTarget).find('#no_table_Programa').val(id_programa);
    $(e.currentTarget).find('#no_table_Tipo').val(tipoPR);
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  $(e.currentTarget).find("#no_table_Nombre"));

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongDescrip, $(e.currentTarget).find("#no_table_Descripcion"));

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongCodigo, $(e.currentTarget).find("#no_table_Codigo"));
  });

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      $("#agregarTipoActividadBtn").click();        // Abre el modal (da click en el botón agregar).
      $(".error_wrapper").css('color','red');  // Se pone el error en rojo.
  }

  // Si hay errores en el formulario editar...
  if (mensajeErrorEditar != '{}'){
      var tipoActividadEditar = localStorage.getItem("tipoActividadEditar");
      $('span[data-idtipo="' + tipoActividadEditar + '"]').click();
      $(".error_wrapper").css('color','red');
  }


  // -.........................................................................-
  // Para realizar la búsqueda.
  var options = {
    valueNames: ['nombre_tipo', 'descripcion_tipo', { data: ['nombre', 'descripcion'] }],
    item: '<td class="nombre_tipo"></td><td class="descripcion_tipo"><center></center></td>'
  };

  var tipo_actividadList = new List('tipo_actividad', options);

  // -.........................................................................-

  // Para el show more y show less en descripción.
  // Y mostrar un titulo con longitud larga sin que se modifique la vista.
  $("#TipoActividadTable tr").not(":eq(0)").each(function(){ //.not(":eq(0)") first is header of table
    var titulo = $(this).find(".a_table").text();
    var tituloLong = titulo.length;
    var descripcion = $(this).find(".hideContent").text();
    var descripcionLong = descripcion.length;
    var amountText;
    var i;

    // Verificar si la longitud del titulo es mayor a 18 para así reacomodarlo en la columna correspondiente.
    if (tituloLong >= 18){
      var splitTitulo = titulo.split(" ");
      var restTitulo = splitTitulo[0];
      amountText = splitTitulo[0].length;
      i = 1;

      while (true){
        if (splitTitulo.length >= i && amountText + splitTitulo[i].length + 1 < 18){
            restTitulo += " " + splitTitulo[i];
            amountText += splitTitulo[i].length;
            i++;
        }else{
          restTitulo += '\n';
          amountText = 0;
        }

        if (splitTitulo.length <= i)
          break;
      }

      // Se reemplaza los saltos de lineaa de texto por los saltos de linea de HTML.
      restTitulo = restTitulo.replace(/\n/g, "<br />");
      $(this).find(".a-table").html(restTitulo);
    }

    // Si la descripción es menor a 46 se muestra sin modificación.
    // Si es mayor a 46 entonces se hace el split y se muestra restContent y
    // result dependiendo si se quiere ver más o si no.
    if (descripcionLong < 36){
      $(this).find(".showMoreContent").hide();
    }else{
      var restContent = '';
      var result = '';

      var splitDescription = descripcion.split(" ");
      amountText = 0;
      i = 1;

      // Para lo que se mostrará por defecto.
      restContent += splitDescription[0];
      amountText += splitDescription[0].length;

      while (true){
        if (splitDescription.length >= i && amountText + splitDescription[i].length + 1 < 30){
            restContent += " " + splitDescription[i];
            amountText += splitDescription[i].length;
            i++;
        }else{
          restContent += '\n';
          break;
        }
      }


      amountText = 0;

      // Para lo que se oculta.
      if (splitDescription.length >= i){
        result += splitDescription[i];
        amountText += splitDescription[i].length;
        i += 1;

        while (true){
          if (splitDescription.length >= i && amountText + splitDescription[i].length + 1 < 30){
              result += " " + splitDescription[i];
              amountText += splitDescription[i].length;
              i++;
          }else{
            result += '\n';
            amountText = 0;
          }

          if (splitDescription.length <= i)
            break;
        }
      }

      // Se reemplazan los saltos de linea de texto por los saltos de HTML.
      restContent = restContent.replace(/\n/g, "<br />");
      result = result.replace(/\n/g, "<br />");
      $(this).find(".hideContent").html(restContent);
      $(this).find(".restContent").html(result);
    }
  });

  $(".showMoreContent").on("click", function(){
    // Si el ojito está abierto...
    if ($(this).hasClass("glyphicon glyphicon-eye-open")){
      // Se cierra el ojito.
      $(this).removeClass("glyphicon glyphicon-eye-open");
      $(this).addClass("glyphicon glyphicon-eye-close");
      $(this).closest('tr').find(".descripcion_tipo").find(".restContent").show();
    }else{
      // Se abre el ojito.
      $(this).removeClass("glyphicon glyphicon-eye-close");
      $(this).addClass("glyphicon glyphicon-eye-open");
      $(this).closest('tr').find(".descripcion_tipo").find(".restContent").hide();
    }
  });
});
