$(document).ready(function(){
  var maxLongNombre  = 50;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.
  var maxLongCodigo = 10;      // Longitud máxima que tendrá el campo código.

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de editar.
  var mensajeErrorEditar = $("#modalEditar").attr("data-hayErroresEditar");
  mensajeErrorEditar = mensajeErrorEditar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Definición del comportamiento del botón agregar programa cuando se hace click.
  $("#agregarProgBtn").click(function(){
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  "#no_table_Nombre");

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongDescrip, "#no_table_Descripcion");

    // Muestra la cantidad de caracteres disponible en el textfield de código.
    textoRestante(maxLongCodigo, "#no_table_Abreviacion");
  });

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      $("#agregarProgBtn").click();
      $(".error_wrapper").css('color','red');
  }

  // Pasamos los argumentos para editar el catalogo.
  $('#ModalEditarPrograma').on('show.bs.modal', function(e){
      var id_programa = $(e.relatedTarget).data('id-programa');
      var abreviacion = $(e.relatedTarget).data('abreviacion');
      var nombre      = $(e.relatedTarget).data('nombre');
      var descripcion = $(e.relatedTarget).data('descripcion');
      localStorage.setItem("programaEditar", id_programa);
      $(e.currentTarget).find('input[name="id_programa"]').val(id_programa);
      $(e.currentTarget).find('input[name="Abreviacion"]').val(abreviacion);
      $(e.currentTarget).find('input[name="Nombre"]').val(nombre);
      $(e.currentTarget).find("#no_table_Descripcion").val(descripcion);

      // Muestra la cantidad de caracteres disponible en el textfield de nombre.
      textoRestante(maxLongNombre,  $(e.currentTarget).find("#no_table_Nombre"));

      // Muestra la cantidad de caracteres disponible en el textarea de descripción.
      textoRestante(maxLongDescrip, $(e.currentTarget).find("#no_table_Descripcion"));

      // Muestra la cantidad de caracteres disponible en el textfield de código.
      textoRestante(maxLongCodigo, $(e.currentTarget).find("#no_table_Abreviacion"));
  });

  // Si hay errores en el formulario editar...
  if (mensajeErrorEditar != '{}'){
      var programaEditar = localStorage.getItem("programaEditar");
      $('span[data-id-programa="' + programaEditar + '"]').click();
      $(".error_wrapper").css('color','red');
  }

  // Se tuvo que añadir el id al formulario para poder editarlo o eliminarlo en
  // un futuro. Por eso se oculta.
  $("#no_table_id_programa__row").hide();

  // Pasamos los argumentos para eliminar el programa.
  $('#modalEliminarPrograma').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-programa');
      $("#BotonEliminar").attr("href", linkEliminar);
  });

  // -.........................................................................-
  // Para realizar la búsqueda.
  var options = {
    valueNames: ['nombre_programa', 'descripcion_programa', { data: ['nombre', 'descripcion'] }],
    item: '<td class="nombre_programa"></td><td class="descripcion_programa"><center></center></td>'
  };

  var programList = new List('programs', options);

  // -.........................................................................-

  // Para el show more y show less en descripción.
  // Y mostrar un titulo con longitud larga sin que se modifique la vista.
  $("#TipoActividadTable tr").not(":eq(0)").each(function(){ //.not(":eq(0)") first is header of table
    var titulo = $(this).find(".a-table").text();
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
    if (descripcionLong < 46){
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
        if (splitDescription.length >= i && amountText + splitDescription[i].length + 1 < 46){
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
          if (splitDescription.length >= i && amountText + splitDescription[i].length + 1 < 46){
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
      $(this).closest('tr').find(".descripcion_programa").find(".restContent").show();
    }else{
      // Se abre el ojito.
      $(this).removeClass("glyphicon glyphicon-eye-close");
      $(this).addClass("glyphicon glyphicon-eye-open");
      $(this).closest('tr').find(".descripcion_programa").find(".restContent").hide();
    }
  });
});
