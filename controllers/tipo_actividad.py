# -*- coding: utf-8 -*-
#. --------------------------------------------------------------------------- .
'''
Vista de Gestionar Tipo Actividad, tiene las opciones:
- Agregar Tipo
- Modificar Tipo
- Eliminar Tipo
- Papelera (No funcional)
'''
def gestionar():
    # Obtengo datos de los tipo_actividades en base de datos para generar
    # tabla que los muestre
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.id_tipo != None, db.TIPO_ACTIVIDAD.papelera == False])

    ids = db(query).select(db.TIPO_ACTIVIDAD.id_tipo)
    nombres = db(query).select(db.TIPO_ACTIVIDAD.nombre)
    descripcion = db(query).select(db.TIPO_ACTIVIDAD.descripcion)
    programas = db(query).select(db.TIPO_ACTIVIDAD.id_programa)

    tipos = db(query).select(db.TIPO_ACTIVIDAD.nombre, db.TIPO_ACTIVIDAD.descripcion, db.TIPO_ACTIVIDAD.id_tipo)

    # Decido que mensaje se va a mostrar
    if(session.message not in ['Tipo Eliminado', 'Tipo agregado exitosamente']):
        session.message = ''

    return dict(ids=ids,nombres=nombres,descripcion=descripcion, programas = programas, tipos=tipos, admin = get_tipo_usuario())

#. --------------------------------------------------------------------------- .
'''
    Permite añadir un nuevo tipo de actividad.
'''
def agregar_tipo():
    
    # Se obtienen todos los programas almacenados en la base de datos.
    lista_programas = db().select(db.PROGRAMA.ALL)
    programas = []
    
    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas: programas.append(programa.nombre)
    
    # AQUI VA UN CONDICIONAL.
    # Para agregar un tipo de actividad se debe tener al menos un programa.
    formulario = SQLFORM.factory(
                        Field('Nombre',
                               requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('([A-zÀ-ÿŸ])([A-zÀ-ÿŸ0-9" "])*', error_message="El nombre del tipo de actividad debe comenzar con una letra."),
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
                        labels = {'Descripcion' : 'Descripción'},
                )
    
    hayPrograma = len(programas) != 0
    
    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if hayPrograma and formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        programa = db(db.PROGRAMA.nombre == request.vars.Programa).select()
        id_programa = programa[0].id_programa
        db.TIPO_ACTIVIDAD.insert(nombre = request.vars.Nombre,
                                 tipo_p_r = request.vars.Tipo,
                                 descripcion = request.vars.Descripcion,
                                 id_programa = id_programa
                                 )
        redirect(URL('agregar_tipo_campos.html'))
    elif not hayPrograma :
        session.message = 'Lo sentimos, no existen programas.'
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Lo sentimos, todos los campos son obligatorios.'
    # Metodo GET
    else:
        session.message = ''
    
    return dict(formulario=formulario, admin = get_tipo_usuario(), mensaje=session.message)

#. --------------------------------------------------------------------------- .
'''
Vista con el formulario para agregar campos al tipo actividad,
tambien tiene una tabla con los campos que ya han sido agregados
'''
def agregar_tipo_campos():
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    nombre_tipo = session.form_nombre
    tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'imagen', 'cantidad entera', 'cantidad decimal']
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO.ALL, db.ACT_POSEE_CAMPO.ALL)
    
    # Busco los catalogos disponibles
    catalogos = db().select(db.CATALOGO.nombre, db.CATALOGO.id_catalogo)
    nombres_catalogos = ['---']
    for i in range(0, len(catalogos)):
        nombres_catalogos.append(catalogos[i].nombre)
    
    # Busco el id del tipo_actividad
    id_tipo = db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).select(db.TIPO_ACTIVIDAD.id_tipo)[0].id_tipo
    
    # Genero formulario para los campos
    form = SQLFORM.factory(
                    Field('Nombre', requires=IS_NOT_EMPTY()),
                    Field('Tipo', requires=IS_IN_SET(tipo_campos)),
                    Field('Obligatorio', widget=SQLFORM.widgets.boolean.widget),
                    Field('Catalogo', requires=IS_IN_SET(nombres_catalogos), default='---'),
                    labels = {'Catalogo' : 'Catálogo'},
                    submit_button = 'Agregar'
                    )
    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del catalogo en caso de que haya uno
        indice = -1
        for i in range(0, len(nombres_catalogos)):
            
            if(nombres_catalogos[i] == request.vars.Catalogo):
                indice = i
        
        # Agrego el campo a la base
        if request.vars.Obligatorio == None:
            request.vars.Obligatorio = False
        
        if indice == -1:
            db.CAMPO.insert(nombre = request.vars.Nombre,
                            obligatorio = request.vars.Obligatorio,
                            tipo_campo = request.vars.Tipo,
                            id_catalogo = None
                            )
        else:
            db.CAMPO.insert(nombre = request.vars.Nombre,
                            obligatorio = request.vars.Obligatorio,
                            tipo_campo = request.vars.Tipo,
                            id_catalogo = None
                            )
            
            id_catalogo = catalogos[indice-1].id_catalogo
            
            queryCampo = reduce(lambda a, b: (a&b),[db.CAMPO.nombre == request.vars.Nombre,
                                                db.CAMPO.tipo_campo == request.vars.Tipo,
                                                db.CAMPO.obligatorio == request.vars.Obligatorio])
            
            id_campo = db(queryCampo).select(db.CAMPO.id_campo).first()
            db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = id_campo)
            
            
            
            #Tengo que duplicar los campos del catálogo
            
            
            camposParaDuplicar = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select(db.CAMPO_CATALOGO.ALL)
            for campo in camposParaDuplicar :
                
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
                
            
            redirect(URL('agregar_tipo_campos.html'))
        
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el objeto de tipo ACT_POSEE_CAMPO a la base
        # (es la relacion entre el campo y el tipo)
        idd_campo = db(db.CAMPO.nombre == request.vars.Nombre).select(db.CAMPO.id_campo)[0].id_campo
        db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = idd_campo)
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('agregar_tipo_campos.html'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        session.message = ''
    
    return dict(form = form, campos = campos_guardados, admin = get_tipo_usuario())

#. --------------------------------------------------------------------------- .
'''
Metodo auxiliar usado para agregar el mensaje de exito
al agregar un tipo actividad, solo guarda el mensaje y redirige a
la pagina de gestionar
'''
def agregar_tipo_aux():

    session.message = 'Tipo agregado exitosamente'
    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
'''
Metodo que aborta la creacion de un tipo_actividad en la vista de
agregar campos, no solo elimina los campos y las relaciones sino
que tambien elimina el tipo_actividad (que a este punto ya se
encuentra en la base)
'''
def eliminar_campos():
    # Obtengo el nombre del tipo_actividad
    nombre_tipo = session.form_nombre

    # Construyo query para obtener la relacion entre los campos y el tipo
    # actividad que quiero eliminar
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados en 'aux'
    aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        db(db.CAMPO.id_campo == row.id_campo).delete()

    # Borro el tipo actiidad
    db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).delete()

    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
'''
 Funcion que envia un tipo actividad a la papelera
 el tipo es especificado por un parametr de URL
'''
def enviar_tipo_papelera():
    id_tipo = int(request.args[0])
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).update(papelera=True)
    session.message = 'Tipo Enviado a la Papelera'
    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
'''
 Vista de gestion de la papelera
'''
def gestionar_archivo_historico():
    aux = db(db.TIPO_ACTIVIDAD.papelera == True).select(db.TIPO_ACTIVIDAD.nombre,
                                                        db.TIPO_ACTIVIDAD.descripcion,
                                                        db.TIPO_ACTIVIDAD.id_tipo)

    return dict(tipos_papelera = aux,admin=get_tipo_usuario())

#. --------------------------------------------------------------------------- .
'''
 Metodo que elimina un tipo actividad de la base de datos
 de manera definitiva
'''
def eliminar_tipo_papelera():
    id_tipo = int(request.args[0])
    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.papelera == True,
                                          db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo]
                   )
    # Guardo los reusltados en 'aux'
    aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

    # Borro las relaciones
    if (len(aux) > 0):
        db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

    # Borro los campos
    for row in aux:
        db(db.CAMPO.id_campo == row.id_campo).delete()

    # Borro el tipo_activdad
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).delete()

    # Guardo mensaje de exito
    session.message = 'Tipo Eliminado'
    redirect(URL('gestionar_archivo_historico.html'))

#. --------------------------------------------------------------------------- .
'''
 Metodo que restaura un tipo actividad de la papelera
'''
def restaurar_tipo():
    id_tipo = int(request.args[0])
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).update(papelera=False)
    session.message = 'Tipo Restaurado'
    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
def ver_tipo_actividad():
    id_tipo = int(request.args[0])
    
    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    
    campos_guardados = db(query).select(db.CAMPO.ALL)
    
    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()
    programa = db(db.PROGRAMA.id_programa == tipo.id_programa).select(db.PROGRAMA.ALL).first()
    
    return dict(campos = campos_guardados, tipo = tipo, admin = get_tipo_usuario(), tipo_nombre = tipo.nombre, programa_nombre = programa.nombre)
    
#. --------------------------------------------------------------------------- .
def eliminar_campo():
    id_campo = int(request.args[0])

    db(db.ACT_POSEE_CAMPO.id_campo == id_campo).delete()
    db(db.CAMPO.id_campo == id_campo).delete()

    redirect(URL('agregar_tipo_campos.html'))

#. --------------------------------------------------------------------------- .
def editar_tipo():
    
    admin = get_tipo_usuario()  # Obtengo el tipo del usuario actual.
    id = request.args[0]        # Se identifica cual tipo de actividad se identificará.
    
    # Se busca el tipo de actividad en la base de datos.
    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id).select()[0]
    
    # Se obtienen todos los programas almacenados en la base de datos.
    lista_programas = db().select(db.PROGRAMA.ALL)
    programas = {}
    
    # Se crea un diccionario para almacenar unicamente los nombres de los programas almacenados.
    for programa in lista_programas:
        programas[programa.id_programa] = programa.nombre
    
    # Para modificar un tipo de actividad se debe tener al menos un programa.
    formulario = SQLFORM.factory(
                        Field('Nombre',
                              default = tipo.nombre,
                              requires = [IS_NOT_EMPTY(error_message='El nombre del tipo de actividad no puede quedar vacío.'),
                                           IS_MATCH('([A-zÀ-ÿŸ])([A-zÀ-ÿŸ0-9" "])*', error_message="El nombre del tipo de actividad debe comenzar con una letra."),
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
                        labels = {'Descripcion' : 'Descripción'},
                )
    
    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        tipo.nombre = request.vars.Nombre
        tipo.tipo_p_r = request.vars.Tipo
        tipo.descripcion = request.vars.Descripcion
        tipo.id_programa = request.vars.Programa
        tipo.update_record()                                 # Se actualiza el tipo de actividad.
        
        tipo_nombre = 'Evaluables por pares académicos' if tipo.tipo_p_r == 'P' else 'No evaluables por pares académicos'
        programa_nombre = programas[int(request.vars.Programa)]
        
        redirect(URL('ver_tipo_actividad.html', args=[id, tipo_nombre, programa_nombre]))  # Se redirige a la vista del preview del T.A. modificado.
    
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
    
    return dict(tipo=tipo, formulario=formulario, admin=get_tipo_usuario())

#. --------------------------------------------------------------------------- .
#"""
#   Método que permite editar un campo cuyo id es request.args[0]
#"""
def editar_campo():
    
    admin = get_tipo_usuario()  # Obtengo el tipo del usuario actual.
    
    id_campo = request.args[0]
    
    # Los atributos del campo son puestos por defecto en el formulario
    campo = db(db.CAMPO.id_campo == id_campo).select(db.CAMPO.ALL).first()
    
    tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'imagen', 'cantidad entera', 'cantidad decimal']
    
    formulario = SQLFORM.factory(
                    Field('Nombre', requires=IS_NOT_EMPTY(), default=campo.nombre),
                    Field('Tipo', requires=IS_IN_SET(tipo_campos), default=campo.tipo_campo),
                    Field('Obligatorio', widget=SQLFORM.widgets.boolean.widget, default=campo.obligatorio),
                    submit_button = 'Editar'
                    )
    
    if formulario.accepts(request.vars, session):
        
        campo.update_record(nombre = request.vars.Nombre,
                            tipo_campo = request.vars.Tipo,
                            obligatorio = request.vars.obligatorio)
        
        
        # Se obtiene el id del tipo de actividad asociado al campo para
        # hacer un redirect
        
        relacionActividadCampo = db(db.ACT_POSEE_CAMPO.id_campo == id_campo).select(db.ACT_POSEE_CAMPO.id_tipo_act).first()
        redirect(URL("ver_tipo_actividad.html", args=[relacionActividadCampo.id_tipo_act]))
        
    elif formulario.errors :
        
        mensaje = "Ocurrió un error con el formulario."
        
    else :
        mensaje = ""
    
    return dict(formulario = formulario, mensaje=mensaje, admin=admin)

#. --------------------------------------------------------------------------- .
def get_tipo_usuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))

    return admin

#. --------------------------------------------------------------------------- .
