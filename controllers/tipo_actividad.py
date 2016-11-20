# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario

#. --------------------------------------------------------------------------- .
'''
Vista de Gestionar Tipo Actividad, tiene las opciones:
- Agregar Tipo
- Modificar Tipo
- Eliminar Tipo
- Papelera (Archivo Historico)
'''

def construir_formulario_agregar_tipo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    lista_programas =  db(db.PROGRAMA.papelera == False).select()
    programas = {}

    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas:
        programas[programa.id_programa] = programa.nombre

    formulario_agregar_tipo = SQLFORM.factory(
                        Field('Nombre',
                               requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                           IS_LENGTH(128)]),
                        Field('Tipo', default = 'Seleccione...',
                              requires = IS_IN_SET({'P':'Evaluables por pares académicos', 'R':'No evaluables por pares académicos'},
                                                    zero=T('Seleccione...'),
                                                    error_message = 'Debes elegir entre "Evaluables por pares académicos" o "No evaluables por pares académicos"')),
                        Field('Descripcion', type="text",
                              requires = [IS_NOT_EMPTY(error_message='La descripción del tipo de actividad no puede quedar vacía.'),
                                          IS_LENGTH(2048)]),
                        Field('Programa',
                              requires = IS_IN_SET(programas, zero="Seleccione...",
                                                   error_message = 'Debes elegir uno de los programas listados.')),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción'}
                )
    formulario_agregar_tipo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_agregar_tipo.element(_type='submit')['_value']="Agregar"

    return formulario_agregar_tipo

def construir_formulario_editar_tipo():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    lista_programas = db(db.PROGRAMA.papelera == False).select()
    programas = {}

    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas:
        programas[programa.id_programa] = programa.nombre


    formulario_editar_tipo = SQLFORM.factory(
                        Field('Nombre',
                              #default = tipo.nombre,
                              requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                           IS_LENGTH(128)]),
                        Field('Tipo', #default = tipo.tipo_p_r,
                              requires = IS_IN_SET({'P':'Evaluables por pares académicos', 'R':'No evaluables por pares académicos'},
                                                    zero=T('Seleccione...'),
                                                    error_message = 'Debes elegir entre "Evaluables por pares académicos" o "No evaluables por pares académicos"')),
                        Field('Descripcion', type="text",
                              #default = tipo.descripcion,
                              requires = [IS_NOT_EMPTY(error_message='La descripción del tipo de actividad no puede quedar vacía.'),
                                          IS_LENGTH(2048)]),
                        Field('Programa', #default = tipo.id_programa,
                              requires = IS_IN_SET(programas, zero="Seleccione...",
                                                   error_message = 'Debes elegir uno de los programas listados.')),
                        Field('Id_tipo',type="hidden"),
                        submit_button = 'Actualizar',
                        labels = {'Descripcion' : 'Descripción'}
                )

    formulario_editar_tipo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar_tipo.element(_type='submit')['_value']="Agregar"
    
    return formulario_editar_tipo

#. ---------------------------------------------------------------------------
'''
    Gestionar Tipo de Actividad
'''
def gestionar():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    formulario_agregar_tipo = construir_formulario_agregar_tipo()
    formulario_editar_tipo = construir_formulario_editar_tipo()

    # Vista básica
    if formulario_editar_tipo.accepts(request.vars, session,formname="formulario_editar_tipo"):
        tipo = db(db.TIPO_ACTIVIDAD.id_tipo == request.vars.Id_tipo).select()[0]
        tipo.nombre = request.vars.Nombre
        tipo.tipo_p_r = request.vars.Tipo
        tipo.descripcion = request.vars.Descripcion
        id_programa = request.vars.Programa
        tipo.id_programa = id_programa
        tipo.update_record()                                 # Se actualiza el tipo de actividad.

    if formulario_agregar_tipo.accepts(request.vars, session,formname="formulario_agregar_tipo"):
        id_programa = request.vars.Programa
        db.TIPO_ACTIVIDAD.insert(nombre = request.vars.Nombre,
                                 tipo_p_r = request.vars.Tipo,
                                 descripcion = request.vars.Descripcion,
                                 id_programa = id_programa)


    if len(request.args) == 0:

        listaTipoActividades = db(db.TIPO_ACTIVIDAD.papelera == False).select(db.TIPO_ACTIVIDAD.ALL)
        programa = dict()
        programa["nombre"] = None
        programa["descripcion"] = None


    else :

        id_programa = request.args[0]

        listaTipoActividades =   db((db.TIPO_ACTIVIDAD.papelera == False)
                                 & (db.TIPO_ACTIVIDAD.id_programa == id_programa)).select(db.TIPO_ACTIVIDAD.ALL)

        programa = db(db.PROGRAMA.id_programa == id_programa).select(db.PROGRAMA.ALL).first()


    return dict(admin = get_tipo_usuario(session)
            , listaTipoActividades = listaTipoActividades
            , programa_nombre = programa["nombre"], programa_descripcion = programa["descripcion"]
            , formulario_agregar_tipo = formulario_agregar_tipo
            , formulario_editar_tipo = formulario_editar_tipo)

#. --------------------------------------------------------------------------- .
'''
    Permite añadir un nuevo tipo de actividad.
'''
def agregar_tipo():
  
    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    # Configuro widgets para el formulario de Agregar Tipo Actividad
    db.TIPO_ACTIVIDAD.nombre.widget = SQLFORM.widgets.string.widget
    db.TIPO_ACTIVIDAD.descripcion.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.producto.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.nro_campos.widget = SQLFORM.widgets.integer.widget
    def horizontal_radio(f, v):
        return SQLFORM.widgets.radio.widget(f, v, cols=2)
    db.TIPO_ACTIVIDAD.tipo_p_r.widget = horizontal_radio

    # Se obtienen todos los programas almacenados en la base de datos.
    lista_programas = db().select(db.PROGRAMA.ALL)
    programas = []

    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas: programas.append(programa.nombre)

    # AQUI VA UN CONDICIONAL.
    # Para agregar un tipo de actividad se debe tener al menos un programa.
    formulario_agregar_tipo = SQLFORM.factory(
                        Field('Nombre',
                               requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                           IS_LENGTH(128)]),
                        Field('Tipo', default = 'Seleccione...',
                              requires = IS_IN_SET({'P':'Evaluables por pares académicos', 'R':'No evaluables por pares académicos'},
                                                    zero=T('Seleccione...'),
                                                    error_message = 'Debes elegir entre "Evaluables por pares académicos" o "No evaluables por pares académicos"')),
                        Field('Descripcion', type="text",
                              requires = [IS_NOT_EMPTY(error_message='La descripción del tipo de actividad no puede quedar vacía.'),
                                          IS_LENGTH(2048)]),
                        Field('Programa',
                              requires = IS_IN_SET(programas, zero="Seleccione...",
                                                   error_message = 'Debes elegir uno de los programas listados.')),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción'}
                )

    hayPrograma = len(programas) != 0

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if hayPrograma and formulario_agregar_tipo.accepts(request.vars, session,formname="formulario_agregar_tipo"):
        session.form_nombre = request.vars.Nombre
        programa = db(db.PROGRAMA.nombre == request.vars.Programa).select()
        id_programa = programa[0].id_programa
        db.TIPO_ACTIVIDAD.insert(nombre = request.vars.Nombre,
                                 tipo_p_r = request.vars.Tipo,
                                 descripcion = request.vars.Descripcion,
                                 id_programa = id_programa)
    elif not hayPrograma :
        session.message = 'Lo sentimos, no existen programas.'
    # En caso de que el formulario no sea aceptado
    elif formulario_agregar_tipo.errors:
        session.message = 'Lo sentimos, todos los campos son obligatorios.'
    # Metodo GET
    else:
        session.message = ''

    formulario_agregar_tipo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_agregar_tipo.element(_type='submit')['_value']="Agregar"

    return dict(formulario=formulario_agregar_tipo, admin = get_tipo_usuario(session), mensaje=session.message, hayPrograma = hayPrograma)

#. --------------------------------------------------------------------------- .
'''
Vista con el formulario para agregar campos al tipo actividad,
tambien tiene una tabla con los campos que ya han sido agregados
'''
def formulario_agregar_tipo_campos():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    # Se definen los posibles tipos de campo.
    tipo_campos = ['Fecha', 'Telefono', 'Texto Corto','Documento','Cantidad Entera','Cantidad Decimal', 'Texto Largo', 'Cedula']

    # Obtengo todos los catálogos almacenados.
    lista_catalogos = db().select(db.CATALOGO.ALL)
    catalogos = {}

    for catalogo in lista_catalogos: catalogos[catalogo.id] = catalogo.nombre

    # Genero formulario para los campos.
    # Si no se utiliza catálogo.
    formSimple = SQLFORM.factory(
                    Field('Nombre', requires=[IS_NOT_EMPTY(error_message="Por favor elija un nombre para el campo."),
                                              IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                    Field('Tipo', requires = IS_IN_SET(tipo_campos, zero="Seleccione...", error_message="Seleccione un tipo para el campo")),
                    Field('Obligatorio', widget=SQLFORM.widgets.boolean.widget),
                    submit_button = 'Agregar'
                    )

    # Si se utilizan catálogos.
    formMultiple = SQLFORM.factory(
                        Field('Catalogo', default='Seleccione...',
                               requires= IS_IN_SET(catalogos, zero=T('Seleccione...'),
                                         error_message = 'Debe elegir alguno de los catálogos.')),
                        labels = {'Catalogo' : 'Catálogo'},
                        submit_button = 'Agregar'
                    )

    formSimple.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formSimple.element(_type='submit')['_value']="Agregar"

    formMultiple.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formMultiple.element(_type='submit')['_value']="Agregar"

    return formSimple, formMultiple

#. --------------------------------------------------------------------------- .
'''
Metodo que aborta la creacion de un tipo_actividad en la vista de
agregar campos, no solo elimina los campos y las relaciones sino
que tambien elimina el tipo_actividad (que a este punto ya se
encuentra en la base)
'''
def eliminar_campo():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    id_tipo = int(request.args[0])
    id_campo = int(request.args[1])

    # Busco los productos que tengan asociado ese campo, y lo elimino.
    db(db.PRODUCTO_TIENE_CAMPO.id_campo == id_campo).delete()

    # Busco la relacion ACT_POSEE_CAMPO y la elimino
    db(db.ACT_POSEE_CAMPO.id_campo == id_campo).delete()

    # Busco el campo y lo elimno de los campos
    db(db.CAMPO.id_campo == id_campo).delete()


    redirect(URL('ver_tipo_actividad.html',args=[id_tipo]))

#. --------------------------------------------------------------------------- .
'''
 Funcion que envia un tipo actividad a la papelera
 el tipo es especificado por un parametr de URL
'''
def enviar_tipo_papelera():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    id_tipo = int(request.args[0])
    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()
    tipo.update(papelera=True)
    tipo.update_record()
    session.message = 'Tipo Enviado a la Papelera'
    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
def ver_tipo_actividad():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    id_tipo = request.args[0]

    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])

    campos_guardados = db(query).select(db.CAMPO.ALL)

    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()
    programa = db(db.PROGRAMA.id_programa == tipo.id_programa).select(db.PROGRAMA.ALL).first()

    # Formularios para agregar campos o catalogos
    formSimple, formMultiple = formulario_agregar_tipo_campos()
    formulario_editar_campo  = formularioEditarCampo()

    if formSimple.accepts(request.vars, session,formname="formSimple"):

        # Verifico si se seleccionó el campo "Obligatorio".
        if request.vars.Obligatorio == None:
           request.vars.Obligatorio = False

        # Se inserta el campo, en la base de datos, que se desea utilizar.
        db.CAMPO.insert(nombre = request.vars.Nombre,
                        obligatorio = request.vars.Obligatorio,
                        tipo_campo = request.vars.Tipo,
                        id_catalogo = None)

        # Se busca el id del campo.
        queryCampo = reduce(lambda a, b: (a&b),[db.CAMPO.nombre == request.vars.Nombre,
                                            db.CAMPO.tipo_campo == request.vars.Tipo,
                                            db.CAMPO.obligatorio == request.vars.Obligatorio])

        id_campo = db(queryCampo).select(db.CAMPO.id_campo).first()

        # Se almacena la relación entre el campo añadido y el tipo de actividad
        # correspondiente.
        db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = id_campo)

        # Se redirige a la vista permitiendo agregar más campos.
        redirect(URL('ver_tipo_actividad.html',args=[id_tipo]))

    if formMultiple.accepts(request.vars, session,formname="formMultiple"):

        query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])

        # Guardo los resultados de dicho query en 'campos_guardados'
        campos_guardados = db(query).select(db.CAMPO.ALL, db.ACT_POSEE_CAMPO.ALL)

        # Busco el id del catálogo que se deseó utilizar.
        id_catalogo = request.vars.Catalogo

        # Se determina si los campos del catálogo ya habían sido agregados
        for campo_guardado in campos_guardados :
            if str(campo_guardado.CAMPO.id_catalogo) == id_catalogo :
                session.message = "El catálogo seleccionado ya había sido agregado."
                redirect(URL('ver_tipo_actividad.html',args=[id_tipo]))


        campos_catalogo = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select(db.CAMPO_CATALOGO.ALL)

        # Duplico los campos del catálogo
        for campo in campos_catalogo:

            db.CAMPO.insert(nombre = campo.nombre,
                            obligatorio = campo.obligatorio,
                            tipo_campo = campo.tipo_campo,
                            id_catalogo = id_catalogo
                            )

            queryCampo = reduce(lambda a, b: (a&b),[db.CAMPO.nombre == campo.nombre,
                                                db.CAMPO.tipo_campo == campo.tipo_campo,
                                                db.CAMPO.obligatorio == campo.obligatorio,
                                                db.CAMPO.id_catalogo == id_catalogo])

            id_campo = db(queryCampo).select(db.CAMPO.id_campo).first()
            db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = id_campo)

        redirect(URL('ver_tipo_actividad.html',args=[id_tipo]))

    if formulario_editar_campo.accepts(request.vars, session,formname="formulario_editar_campo"):

        id_campo = request.vars.id_campo

        # Los atributos del campo son puestos por defecto en el formulario
        campo = db(db.CAMPO.id_campo == id_campo).select(db.CAMPO.ALL).first()

        campo.update_record(nombre      = request.vars.nombre,
                            tipo_campo  = request.vars.tipo_campo,
                            obligatorio = request.vars.obligatorio)

        # Se obtiene el id del tipo de actividad asociado al campo para
        # hacer un redirect

        redirect(URL("ver_tipo_actividad", args=[id_tipo]))

    formulario_editar_campo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar_campo.element(_type='submit')['_value']="Editar"

    return dict(campos = campos_guardados, tipo = tipo,
                admin = get_tipo_usuario(session), tipo_nombre = tipo.nombre,
                programa_nombre = programa.nombre,
                formSimple = formSimple, formMultiple = formMultiple,
                formulario_editar_campo=formulario_editar_campo)

def editar_tipo():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    id = request.args[0]        # Se identifica cual tipo de actividad se identificará.

    session.tipo_id_editar = id

    # Se busca el tipo de actividad en la base de datos.
    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id).select()[0]

    # Se obtienen todos los programas almacenados en la base de datos.
    lista_programas = db().select(db.PROGRAMA.ALL)
    programas = {}

    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas:
        programas[programa.id_programa] = programa.nombre

    # Para modificar un tipo de actividad se debe tener al menos un programa.
    formulario_editar_tipo = SQLFORM.factory(
                        Field('Nombre',
                              default = tipo.nombre,
                              requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                           IS_LENGTH(128)]),
                        Field('Tipo', default = tipo.tipo_p_r,
                              requires = IS_IN_SET({'P':'Evaluables por pares académicos', 'R':'No evaluables por pares académicos'},
                                                    zero=T('Seleccione...'),
                                                    error_message = 'Debes elegir entre "Evaluables por pares académicos" o "No evaluables por pares académicos"')),
                        Field('Descripcion', type="text",
                              default = tipo.descripcion,
                              requires = [IS_NOT_EMPTY(error_message='La descripción del tipo de actividad no puede quedar vacía.'),
                                          IS_LENGTH(2048)]),
                        Field('Programa', default = tipo.id_programa,
                              requires = IS_IN_SET(programas, zero="Seleccione...",
                                                   error_message = 'Debes elegir uno de los programas listados.')),
                        submit_button = 'Actualizar',
                        labels = {'Descripcion' : 'Descripción'}
                )

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados

    if formulario_editar_tipo.accepts(request.vars, session,formname="formulario_editar_tipo"):
        session.form_nombre = request.vars.Nombre
        tipo.nombre = request.vars.Nombre
        tipo.tipo_p_r = request.vars.Tipo
        tipo.descripcion = request.vars.Descripcion
        tipo.id_programa = request.vars.Programa
        tipo.update_record()                                 # Se actualiza el tipo de actividad.

        tipo_nombre = 'Evaluables por pares académicos' if tipo.tipo_p_r == 'P' else 'No evaluables por pares académicos'
        programa_nombre = programas[int(request.vars.Programa)]

        #redirect(URL('ver_tipo_actividad.html', args=[id, tipo_nombre, programa_nombre]))  # Se redirige a la vista del preview del T.A. modificado.

    # En caso de que el formulario no sea aceptado
    elif formulario_editar_tipo.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''

    formulario_editar_tipo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar_tipo.element(_type='submit')['_value']="Editar"


    return dict(tipo=tipo, formulario=formulario_editar_tipo, admin=get_tipo_usuario(session))

'''
Funcion que se encarga de modificar las caracteriticas de un
campo de un catalogo.
'''
def formularioEditarCampo():

    admin = get_tipo_usuario(session)
    
    if (admin==0):
        redirect(URL(c ="default",f="index"))
      
    formulario = SQLFORM.factory(
                    Field('nombre',
                          requires = [IS_NOT_EMPTY(error_message='El nombre del campo no puede quedar vacio.'),
                                      IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                    Field('tipo_campo',
                           requires = [IS_IN_SET(tipo_campos, zero='Seleccione...', error_message="Debe seleccionar un tipo para el campo.")],
                           widget = SQLFORM.widgets.options.widget),
                    Field('obligatorio', type='boolean',  default = False),
                    Field('id_campo', type="string" ,  default = ''),
                    submit_button='Guardar',
                    labels = {'nombre'      : 'Nombre',
                              'tipo_campo'  : 'Tipo',
                              'obligatorio' : 'Obligatorio'}
                    
                   )

    return formulario
