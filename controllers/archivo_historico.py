'''
Modulo para la gestion del Archivo Historico
(Papelera).

Maneja elementos borrados de:
- Programas.
- Tipo de Actividades

'''

from funciones_siradex import get_tipo_usuario

#. --------------------------------------------------------------------------- .
'''
 Vista de gestion de la papelera
'''
def gestionar():
  
    admin = get_tipo_usuario(session)
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    if request.args:

        listaTipoActividades = db( (db.TIPO_ACTIVIDAD.papelera == True) &
                                   (db.TIPO_ACTIVIDAD.id_programa == request.args(0) ) ).select(db.TIPO_ACTIVIDAD.nombre
                                                                                    ,db.TIPO_ACTIVIDAD.descripcion
                                                                                    ,db.TIPO_ACTIVIDAD.id_tipo
                                                                                    ,db.TIPO_ACTIVIDAD.tipo_p_r
                                                                                    ,db.TIPO_ACTIVIDAD.id_programa
                                                                                    )
    else:
        listaTipoActividades = db(db.TIPO_ACTIVIDAD.papelera == True).select(db.TIPO_ACTIVIDAD.nombre
                                                                                    ,db.TIPO_ACTIVIDAD.descripcion
                                                                                    ,db.TIPO_ACTIVIDAD.id_tipo
                                                                                    ,db.TIPO_ACTIVIDAD.tipo_p_r
                                                                                    ,db.TIPO_ACTIVIDAD.id_programa
                                                                                    )

    listaProgramas = db(db.PROGRAMA.papelera == True).select()

    return dict(admin=get_tipo_usuario(session),
                listaTipoActividades=listaTipoActividades,
                listaProgramas = listaProgramas,
                mensaje = session.message)

#. --------------------------------------------------------------------------- .
'''
 Metodo que elimina un tipo actividad de la base de datos
 de manera definitiva
'''
def eliminar_tipo_papelera():
  
    admin = get_tipo_usuario(session)
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    id_tipo = int(request.args[0])

    # Determino si existen productos con ese tipo de actividad
    # Si existen, entonces no borro al tipo de actividad
    hayProductos = not db(db.PRODUCTO.id_tipo == id_tipo).isempty()
    if hayProductos :
        session.message = 'No se puede eliminar un \
                          tipo de actividad con \
                          productos asociados'

        return redirect(URL('gestionar.html'))

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
    redirect(URL('gestionar.html'))

#. --------------------------------------------------------------------------- .
'''
 Metodo que elimina un programa de la base de datos
 de manera definitiva
'''
def eliminar_programa_papelera():

    id_programa = int(request.args[0])

    # Determino si existen tipos de actividad con ese programa
    # Si existen, entonces no borro al programa
    hayTiposDeActividad = not db(db.TIPO_ACTIVIDAD.id_programa == id_programa).isempty()
    if hayTiposDeActividad :
        session.message = 'No se puede eliminar un \
                          programa con tipos de \
                          actividades asociados'

        return redirect(URL('gestionar.html'))

    db(db.PROGRAMA.id_programa == id_programa).delete()

    # Guardo mensaje de exito
    session.message = 'Programa Eliminado'
    redirect(URL('gestionar.html'))
#. --------------------------------------------------------------------------- .
'''
 Metodo que restaura un tipo actividad de la papelera
'''
def restaurar_tipo():
  
    admin = get_tipo_usuario(session)
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    id_tipo = request.args[0]
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()
    tipo_actividad.update(papelera=False)
    tipo_actividad.update_record()
    redirect(URL('gestionar.html'))

def restaurar_programa():
  
    admin = get_tipo_usuario(session)
    if (admin==0):
        redirect(URL(c ="default",f="index"))

    id_programa = request.args[0]
    programa = db(db.PROGRAMA.id_programa == id_programa).select().first()

    programa.papelera = False
    programa.update_record()
    session.message = 'Programa Restaurado.'
    redirect(URL('gestionar.html'))
