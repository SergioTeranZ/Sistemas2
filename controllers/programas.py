# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario

#import imp  
#foo = imp.load_source('module.funciones_siradex', 'funciones_siradex.py') 
'''
Vista de Gestionar Programas tiene las opciones:
- Agregar Programa
- Editar  Programa
- Por ahora, no se pueden eliminar programas.
'''

def agregar_programa():
  
    admin = get_tipo_usuario(session)
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    formulario = SQLFORM.factory(
                        Field('Nombre',
                              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                        Field('Abreviacion',
                              requires = [IS_NOT_EMPTY(error_message='La abreviacion del programa no puede quedar vacia.'),
                                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                        Field('Descripcion', type="text",
                              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción',
                                  'Nombre' : 'Nombre del Programa'},
                        )

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        db.PROGRAMA.insert(nombre = request.vars.Nombre,
                           abreviacion = request.vars.Abreviacion,
                           descripcion = request.vars.Descripcion
                           )
        redirect(URL('gestionar_programas.html'))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en los datos del formulario, por favor intente nuevamente.'
    # Metodo GET
    else:
        session.message = ''

    return dict(formulario=formulario, admin = admin)

# Permitiria Modificar o Desactivar Programas
# del sistema Siradex.
def gestionar_programas():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Obtengo todos los programas almacenados en la base de datos.
    programas = db(db.PROGRAMA.papelera == False).select()

    # Para agregar un programa.
    formulario = SQLFORM.factory(
        Field('Nombre',
              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                          IS_LENGTH(256),
                          IS_NOT_IN_DB(db, 'PROGRAMA.nombre', error_message="Ya existe un programa con ese nombre.")]),
        Field('Abreviacion',
                requires = [IS_NOT_EMPTY(error_message='La abreviacion del programa no puede quedar vacia.'),
                            IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
        Field('Descripcion', type="text",
              requires=[IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.'),
                        IS_LENGTH(2048)]),
        submit_button = 'Agregar',
        labels = {'Descripcion' : 'Descripción',
                  'Nombre' : 'Nombre del Programa',
                  'Abreviacion' : 'Abreviacion del Programa'},
        )
    formulario.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario.element(_type='submit')['_value']="Agregar"

    # Para editar un programa.
    formulario_editar  = SQLFORM.factory(
        Field('Nombre',
              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales."),
                          IS_LENGTH(256),
                          IS_NOT_IN_DB(db(db.PROGRAMA.id_programa != request.vars['id_programa']), 'PROGRAMA.nombre',
                                            error_message= ('Ya existe un programa con el nombre "' + request.vars['Nombre'] + '".') if not(request.vars['Nombre'] is None) else 'Ya existe un programa con el nombre ')]),
        Field('Abreviacion',
                requires = [IS_NOT_EMPTY(error_message='La abreviacion del programa no puede quedar vacia.'),
                            IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),        
        Field('Descripcion', type="text",
              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
        Field('id_programa', type="string"),
        submit_button = 'Agregar',
        labels = {'Descripcion' : 'Descripción',
                  'Nombre' : 'Nombre del Programa',
                  'Abreviacion' : 'Abreviacion del Programa'},
        )
    formulario_editar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar.element(_type='submit')['_value']="Editar"

    # MÉTODO POST FORMULARIO AGREGAR:
    # En caso de que los datos del formulario agregar estén correctos:
    if formulario.accepts(request.vars, session, formname="formulario"):
        # Se agrega el programa deseado a la base de datos.
        db.PROGRAMA.insert(nombre = request.vars.Nombre,
                            abreviacion = request.vars.Abreviacion,
                           descripcion = request.vars.Descripcion)
        # Se redirige a la vista de getión de programas.
        redirect(URL('gestionar_programas.html'))
    # En caso de que el formulario no sea aceptado:
    elif (formulario.errors):
        session.message = "Los datos del programa son inválidos. Intentelo nuevamente."

    # Se verifica si los campos están llenos correctamente.
    if formulario_editar.accepts(request.vars, session, formname="formulario_editar"):
        id_programa = request.vars.id_programa
        programa = db(db.PROGRAMA.id_programa == id_programa).select().first()
        session.form_nombre = request.vars.Nombre
        programa.nombre = request.vars.Nombre
        programa.abreviacion = request.vars.Abreviacion
        programa.descripcion = request.vars.Descripcion
        programa.update_record()                    # Se actualiza el programa.

        redirect(URL('gestionar_programas.html'))   # Se redirige a la vista de gestión.

    # En caso de que el formulario no sea aceptado
    elif formulario_editar.errors:
        session.message = 'Error en los datos del formulario, por favor intente nuevamente.'

    # MÉTODO POST FORMULARIO EDITAR:
    return dict(admin=admin, programas=programas, hayErroresAgregar=formulario.errors,
                hayErroresEditar=formulario_editar.errors, formulario=formulario,
                formulario_editar=formulario_editar)

def eliminar_programa():
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    id_programa = request.args[0]

    programa = db(db.PROGRAMA.id_programa == id_programa).select()[0]

    programa.papelera           = True
    programa.modif_fecha        = request.now
    programa.usbid_usu_modificador = session.usuario['usbid']
    programa.update_record()
    redirect(URL('gestionar_programas.html'))

def editar_programa():

    admin = get_tipo_usuario(session) # Obtengo el tipo del usuario actual.

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    id = request.args[0]        # Se identifica cual programa se identificará.

    # Se busca el programa en la base de datos.
    programa = db(db.PROGRAMA.id_programa == id).select()[0]

    # Se presenta el formulario donde se modificarán los valores del programa.
    formulario = SQLFORM.factory(
                        Field('Nombre',
                              default = programa.nombre,
                              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                                          IS_MATCH('^[A-zÀ-ÿŸ\s]*$', error_message="Use solo letras, sin numeros ni caracteres especiales.")]),
                        Field('Abreviacion',
                            requires = [IS_NOT_EMPTY(error_message='La abreviacion del programa no puede quedar vacia.')]),
                        Field('Descripcion', type="text",
                              default = programa.descripcion,
                              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
                        submit_button = 'Actualizar',
                        labels = {'Descripcion' : 'Descripción',
                                  'Nombre' : 'Nombre del Programa',
                                  'Abreviacion' : 'Abreviacion del Programa'}
                        )

    # Se verifica si los campos están llenos correctamente.
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        programa.nombre = request.vars.Nombre
        programa.abreviacion = request.vars.Abreviacion
        programa.descripcion = request.vars.Descripcion
        programa.update_record()                    # Se actualiza el programa.
        redirect(URL('gestionar_programas.html'))   # Se redirige a la vista de gestión.

    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en los datos del formulario, por favor intente nuevamente.'
    # Metodo GET
    else:
        session.message = ''

    return dict(formulario=formulario, admin = admin)
