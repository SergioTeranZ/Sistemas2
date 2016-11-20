# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario

tipo_campos = ['Fecha', 'Telefono', 'Texto Corto','Documento','Cantidad Entera','Cantidad Decimal', 'Texto Largo', 'Cedula']


'''
Funcion que se encarga de obtener los datos para mostrar los catalogos
que existen en el sistema.
'''

def vGestionarCatalogos():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    #Si hay que agregar un campo a un catalogo

    #Obtenemos todos los catalogos.
    listaCatalogos = db().select(db.CATALOGO.ALL)
    catalogos = []

    #Para cada catalogo, obtenemos sus campos.
    for catalogo in listaCatalogos:
        campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == catalogo.id).select()
        catalogos.append([catalogo, campos_guardados])

    #chequeamos si se esta gestionando un catalogo en particular
    catalogo_actual = None;
    if request.args:
        catalogo_actual = int(request.args[0])
    else:
        #Si no es ninguno en especifico,
        #Tomamos como actual el primer catalogo de la lista, si Existe.
        if catalogos != []:
            catalogo_actual = catalogos[0][0].id_catalogo

    #Formulario para agregar un catalogo.
    formulario_agregar_catalogo = AgregarCatalogo()
    formulario_agregar_campo    = AgregarCampo()
    formulario_editar_campo     = EditarCampo()
    formulario_cambiar_nombre   = cambiarNombreCatalogo()

    if formulario_agregar_catalogo.process(formname = "formulario_agregar_catalogo").accepted:
        # Creamos el catalogo y obtenemos su id, para pasarlo al controlador de agregar campo.
        id_catalogo = db.CATALOGO.insert(nombre = request.vars.nombre)['id_catalogo']
        redirect(URL('vGestionarCatalogos',args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    else:
        message = 'Error en el Formulario de Agregar Catalogo'

    #Formulario para agregar un campo a un catalogo
    if formulario_agregar_campo.process(formname = "formulario_agregar_campo").accepted:
        nombre_campo_nuevo = request.vars.nombre
        id_catalogo        = request.vars.id_catalogo
        nombre_repetido    = False
        campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select()
        for campo in campos_guardados:
            if campo.nombre == nombre_campo_nuevo:
                nombre_repetido = True
                break

        # Si el nombre no esta repetido, lo eliminamos.
        if nombre_repetido:
            message = 'Ya existe el campo'
        else:
            db.CAMPO_CATALOGO.insert(id_catalogo = id_catalogo,
                                     nombre =  nombre_campo_nuevo,
                                     tipo_campo = request.vars.tipo_campo,
                                     obligatorio = request.vars.obligatorio)
            message = ""
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vGestionarCatalogos',args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    else:
        message = 'Error en el Formulario de Agregar Campo'

    if formulario_editar_campo.process(formname = "formulario_editar_campo").accepted:
        nombre_nuevo = request.vars.nombre
        id_catalogo  = request.vars.id_catalogo
        id_campo     = int(request.vars.id_campo_cat)
        nombre_repetido    = False

        #Bucamos los campos que esten guardados
        campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select()

        #Si existe un campo que tenga el mismo nombre
        #Y no sea el campo que estamos modificando.
        #Entonces existe un campo con nombre repetido.

        for campo in campos_guardados:
            if (campo.nombre == nombre_nuevo and
                campo.id_campo_cat != id_campo):
                nombre_repetido = True
                break

        # Si el nombre no esta repetido, modificamos el campo
        if nombre_repetido:
            session.message = 'Ya existe un campo llamado "' + nombre_nuevo + '" en el catalogo.'
        else:
            #Actualizamos el campo
            db.CAMPO_CATALOGO[id_campo] = dict(nombre      = nombre_nuevo,
                                               tipo_campo  = request.vars.tipo_campo,
                                               obligatorio = request.vars.obligatorio)

            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vGestionarCatalogos',args=[id_catalogo]))
    else:
        message = 'Error en el Formulario de Editar Campo'

    if formulario_cambiar_nombre.process(formname = "formulario_cambiar_nombre").accepted:
        nombre_nuevo = request.vars.nombre
        id_catalogo  = request.vars.id_catalogo

        #Actualizamos el nombre
        db.CATALOGO[id_catalogo] = dict(nombre = nombre_nuevo)
        redirect(URL('vGestionarCatalogos',args=[id_catalogo]))
    else:
        message = 'Error en el Formulario de Editar Nombre Catalogo'


    formulario_agregar_catalogo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_agregar_catalogo.element(_type='submit')['_value']="Agregar"

    formulario_agregar_campo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_agregar_campo.element(_type='submit')['_value']="Agregar"

    formulario_editar_campo.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar_campo.element(_type='submit')['_value']="Editar"

    formulario_cambiar_nombre.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_cambiar_nombre.element(_type='submit')['_value']="Renombrar Catálogo"

    return dict(catalogos                   = catalogos,
                catalogo_actual             = catalogo_actual,
                formulario_agregar_catalogo = formulario_agregar_catalogo,
                formulario_agregar_campo    = formulario_agregar_campo,
                formulario_editar_campo     = formulario_editar_campo,
                formulario_cambiar_nombre   = formulario_cambiar_nombre,
                admin = admin)

'''
Funcion que se encarga de agregar un catalogo a la
lista de catalogos existentes, en caso de que no exista
uno con el mismo nombre, se encarga de crearlo y almacenarlo
en la base de datos.
'''
def AgregarCatalogo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    formulario = SQLFORM.factory(
                        Field('nombre',
                              requires = [IS_NOT_EMPTY(error_message='El nombre del catalogo no puede quedar vacio.'),
                                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                          IS_NOT_IN_DB(db, 'CATALOGO.nombre', error_message="Ya existe un catalogo con ese nombre.")]),
                              submit_button='Agregar',
                              labels={'nombre':'Nombre'})

    return formulario

'''
Funcion que se encarga de mostrar los campos del catalogo,
permite crear y elminiar campos relacionados con el catalogo indicado.
'''
def AgregarCampo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Genero formulario para los campos
    formulario = SQLFORM.factory(
                    Field('nombre',
                          requires = [IS_NOT_EMPTY(error_message='El nombre del campo no puede quedar vacio.'),
                                      IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                    Field('tipo_campo',
                           requires = [IS_IN_SET(tipo_campos, zero='Seleccione...', error_message="Debe seleccionar un tipo para el campo.")],
                           widget = SQLFORM.widgets.options.widget),
                    Field('obligatorio', type='boolean', default = False),
                    Field('id_catalogo', type='string', readable=False),
                    labels = {'nombre'      : 'Nombre',
                              'tipo_campo'  : 'Tipo',
                              'obligatorio' : 'Obligatorio'},
                    submit_button='Agregar'
                   )

    return formulario


'''
Funcion que se encarga de eliminar un catalogo, los campos
que este posee y todas las relaciones entre ellos.
'''
def eliminarCatalogo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Obtengo el id del Catalogo a eliminar
    id_catalogo = request.args[0]

    #eliminamos todos los campos de ese catalogo
    campos_del_catalogo = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).delete()

    #Buscamos todas las actividades que tengan relacionado este catalogo
    #y eliminamos las referencias a este.
    campos_en_tipos_actividades = db(db.CAMPO.id_catalogo == id_catalogo).select()
    for campo in campos_en_tipos_actividades:
        campo.id_catalogo = None
        campo.update_record()

    #eliminarmos el catalogo.
    del db.CATALOGO[id_catalogo]

    redirect(URL('vGestionarCatalogos.html'))

'''
Funcion que se encarga de modificar las caracteriticas de un
campo de un catalogo.
'''
def EditarCampo():

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
                    Field('obligatorio', type='boolean', default = False),
                    Field('id_catalogo', type="string", default = ''),
                    Field('id_campo_cat', type="string", default = ''),
                    labels = {'nombre'      : 'Nombre',
                              'tipo_campo'  : 'Tipo',
                              'obligatorio' : 'Obligatorio'},
                    submit_button='Guardar'
                   )

    return formulario

'''
Funcion que se encarga de eliminar un campo del catalogo,
eliminando todas las relaciones existentes e instancias
del catalogo.
'''
def eliminarCampos():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Obtengo el id del campo que se eliminara
    id_campo_cat = request.args[0]
    id_catalogo  = db(db.CAMPO_CATALOGO.id_campo_cat == id_campo_cat).select().first().id_catalogo

    # Elimino el campo del catalogo. Esto no afecta los tipos de actividades
    # Que estan definidas ya, ni los productos ya listos.
    del db.CAMPO_CATALOGO[id_campo_cat]

    redirect(URL('vGestionarCatalogos',args=[id_catalogo]))

def cambiarNombreCatalogo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    formulario = SQLFORM.factory(
                        Field('nombre',
                              requires = [IS_NOT_EMPTY(error_message='El nombre del catalogo no puede quedar vacio.'),
                                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                                          IS_NOT_IN_DB(db, 'CATALOGO.nombre', error_message="Ya existe un catalogo con ese nombre.")]),
                        Field('id_catalogo', type='string'),
                              submit_button='Cambiar Nombre',
                              labels={'nombre':'Nuevo Nombre'})
    return formulario
