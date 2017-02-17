# -*- coding: utf-8 -*-
from notificaciones import *
from funciones_siradex import get_tipo_usuario,get_tipo_usuario_not_loged

# Funcion para busquedas publicas
def busqueda():
    admin = get_tipo_usuario_not_loged(session)
    try:
        graficaPie = URL('busq_val','graficaPie')
        graficaBar = URL('busq_val','graficaBar')
        graficaLine = URL('busq_val','graficaLine')

        if (request.vars.Producto == ""):
            sql = "SELECT descripcion,nombre,id_tipo,id_producto FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto + "%\'"

        else:
            sql = "SELECT descripcion,nombre,id_tipo,id_producto FROM PRODUCTO WHERE plainto_tsquery('english','"+request.vars.Producto+"') @@ to_tsvector('english',coalesce(nombre,'') || ' '|| coalesce(descripcion,''))"

        if request.vars.Programa != None and\
           request.vars.TipoActividad != None and\
           request.vars.fecha != None and\
           request.vars.Autor != None:


            # Anadimos el filtro del usuario T-T T-N N-T N-N
            if request.vars.Autor != "all":
                sql += " AND usbid_usu_creador = " + request.vars.Autor

            # Anadimos el filtro del tipo de actividad
            if request.vars.Programa != "all" and request.vars.TipoActividad == "all":
                sql += " AND id_tipo IN (SELECT id_tipo FROM TIPO_ACTIVIDAD WHERE id_programa=" + str(request.vars.Programa)+ ")"

            elif request.vars.TipoActividad != "all":
                sql += " AND id_tipo=\'" + str(request.vars.TipoActividad)+"'"

            # Anadimos el filtro de la fecha
            if request.vars.fecha != "":
                sql += " AND fecha_realizacion <= '" + request.vars.fecha +"'"

        # Ahora dependiendo del usuario anadimos las restricciones del estado (no se contempla cuando
        # el usuario esta bloqueado porqu no deberia llegar aqui)
        if (session.usuario["tipo"] == "Usuario"):
            sql += " AND estado=\'Validado\';"
        elif (session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador"):
            sql += ";"

        print(sql)
        productos = db.executesql(sql)



        return locals()
    except:

        return locals()

# Mostrar productos
def ver_producto():

    admin = get_tipo_usuario_not_loged(session)

    id_producto = int(request.args(0))
    producto = db(db.PRODUCTO.id_producto == id_producto).select().first()
    usuario_producto = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()
    usuario_nombre = usuario_producto.nombres + " " + usuario_producto.apellidos
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == producto.id_tipo).select().first()
    programa_nombre = db(db.PROGRAMA.id_programa == tipo_actividad.id_programa).select().first().nombre

    #Obtenemos el nombre de los autores
    nombres_autores  = usuario_nombre #Primer autor siempre es el creador.
    autores = db(db.PARTICIPA_PRODUCTO.id_producto == id_producto).select()

    for autor in autores:
      autorAux = db(db.USUARIO.usbid == autor.usbid_usuario).select().first()
      nombres_autores  = nombres_autores + ', ' + autorAux.nombres +' '+ autorAux.apellidos

    query = "SELECT id_comprobante, descripcion FROM COMPROBANTE WHERE producto="+str(id_producto)+";"
    comprobantes = db.executesql(query)

    form = SQLFORM.factory(
            Field("Nombre_Producto", default=producto.nombre,writable = False),
            Field('Descripcion',default=producto.descripcion,writable = False),
            Field('Fecha_de_Relizacion', default=producto.fecha_realizacion,writable=False),
            Field('Lugar', default=producto.lugar,writable=False),
            readonly=True,
            labels = {'Descripcion' : 'Descripción',
                      'Fecha_de_Relizacion' : 'Fecha de Realización'})
           
    #Agregamos los otros elementos de los campos
    campos = db(db.PRODUCTO_TIENE_CAMPO.id_prod == producto.id_producto).select()

    elementos = []

    for campo_valor in campos:
        campo = db(db.CAMPO.id_campo == campo_valor.id_campo).select().first()
        nombre_campo = campo.nombre
        nombre_campo = nombre_campo.replace(" ", "_")

        try :
            if int(nombre_campo[0]):
                nombre_campo = "campo_"+nombre_campo
        except:
            pass

        elementos.append(Field(nombre_campo, default=campo_valor.valor_campo, writable=False))

    if len(elementos) != 0:
        form_datos = SQLFORM.factory(*elementos, readonly=True)

    form_validado = SQLFORM(
            db.PRODUCTO,
            fields=['nombre'],
            labels={'nombre':'Nuevo nombre'},
            col3={'nombre':'Este es el nombre que aparecera al momento de exportar las actividades'}

    )
    form_validado.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    form_validado.element(_type='submit')['_value']="Actualizar"



    ## Formulario para colocar la razon de rechazo de un producto.
    formulario_validar = SQLFORM.factory(
                          Field('nombre','string',
                                    requires=[IS_NOT_EMPTY(error_message="El nombre del producto no puede quedar vacío."),
                                              IS_LENGTH(50, error_message="El nombre del producto no puede superar los 50 caracteres.")]),
                          Field('id_producto',type="string"),
                          submit_button = 'Validar',
                          labels = {'nombre' : 'Nuevo Nombre'})

    formulario_validar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_validar.element(_type='submit')['_value']="Validar"

    ## Formulario para colocar la razon de rechazo de un producto.
    formulario_rechazar = SQLFORM.factory(
                          Field('razon', type="text"),
                          Field('id_producto_r', type="string", default=""),
                          submit_button = 'Agregar',
                          labels = {'razon' : 'Razón de Rechazo del Producto'})

    formulario_rechazar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_rechazar.element(_type='submit')['_value']="Rechazar"

    hayErrores = {}

    if formulario_validar.accepts(request.vars, session, formname="formulario_validar"):
        id_producto = request.vars.id_producto
        nuevo_nombre = request.vars.nombre

        #Actualizamos el nombre del producto
        db.PRODUCTO[id_producto] = dict(nombre = nuevo_nombre)
        #Validamos el producto
        validar(id_producto)
    else:
        hayErrores = formulario_validar.errors

    if formulario_rechazar.accepts(request.vars, session, formname="formulario_rechazar"):
        id_producto = request.vars.id_producto_r
        razon = request.vars.razon

        ## Enviamos notificacion de rechazo
        # obtenemos el producto a rehazar
        producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()

        # obtenemos el usuario que realizo el producto
        usuario = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()

        # parseamos los datos para la notificacion
        datos_usuario = {'nombres' : usuario.nombres}
        if usuario.correo_alter != None:
            datos_usuario['email'] = usuario.correo_alter
        else:
            datos_usuario['email'] = usuario.correo_inst

        producto = {'nombre': producto.nombre}

        # enviamos la notificacion
        enviar_correo_rechazo(mail, datos_usuario, producto, razon)

        # rechazamos efectimavamente el producto.
        rechazar(id_producto)

    ## Fin formulario de rechazo

    return locals()

# Vista de validaciones
def gestionar_validacion():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))


    # Hago el query Espera

    sqlValidadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Validado';"
    sqlEspera = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Por Validar';"
    sqlRechazadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='No Validado';"
    productosV= db.executesql(sqlValidadas)
    productosE = db.executesql(sqlEspera)
    productosR = db.executesql(sqlRechazadas)

    return locals()

# Metodo para validar un producto
def validar(id_producto):

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(url)

    db(db.PRODUCTO.id_producto == id_producto).update(estado='Validado')

    ## INICIO NOTIFICACION ##

    # obtenemos el producto a validar
    producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()

    # obtenemos el usuario que realizo el producto
    usuario = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()

    # parseamos los datos para la notificacion
    datos_usuario = {'nombres' : usuario.nombres}
    if usuario.correo_alter != None:
        datos_usuario['email'] = usuario.correo_alter
    else:
        datos_usuario['email'] = usuario.correo_inst

    producto = {'nombre': producto.nombre}

    # enviamos la notificacion
    enviar_correo_validacion(mail,datos_usuario, producto)

    ## FIN NOTIFICACION ##

    session.message = 'Producto validado exitosamente'
    redirect(URL('gestionar_validacion.html'))

# Metodo para rechazar una producto
def rechazar(id_producto):

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    db(db.PRODUCTO.id_producto == id_producto).update(estado='No Validado')
    session.message = 'Producto rechazado'
    redirect(URL('gestionar_validacion.html'))

def graficaPie():

    query = "select programa.nombre, programa.abreviacion, count(producto.nombre)" + \
    " from ((programa inner join tipo_actividad on programa.id_programa=tipo_actividad.id_programa)" + \
    " inner join producto on producto.id_tipo=tipo_actividad.id_tipo and producto.usbid_usu_creador=\'"+ session.usuario["usbid"] +\
    "\' and producto.estado=\'Validado\') group by programa.nombre, programa.abreviacion;"

    query2 = "select count(producto.nombre) from producto where producto.usbid_usu_creador=\'"+ session.usuario["usbid"]+"\' and producto.estado=\'Validado\';"

    datos = db.executesql(query)
    num_productos = db.executesql(query2)[0][0]

    import pygal
    pie_chart = pygal.Pie()
    for producto in datos:
        porcentaje = (producto[2]*100)//num_productos
        pie_chart.add(producto[1],[{'value':porcentaje, 'label':producto[0]}])
    return pie_chart.render()

def graficaBar():

    query = "select programa.nombre, programa.abreviacion, count(producto.nombre)" + \
    " from ((programa inner join tipo_actividad on programa.id_programa=tipo_actividad.id_programa)" + \
    " inner join producto on producto.id_tipo=tipo_actividad.id_tipo and producto.usbid_usu_creador=\'"+ session.usuario["usbid"] +\
    "\' and producto.estado=\'Validado\') group by programa.nombre, programa.abreviacion;"

    query2 = "select count(producto.nombre) from producto where producto.usbid_usu_creador=\'"+ session.usuario["usbid"]+"\' and producto.estado=\'Validado\';"

    datos = db.executesql(query)
    num_productos = db.executesql(query2)[0][0]

    import pygal
    bar_chart = pygal.Bar()
    for producto in datos:
        porcentaje = (producto[2]*100)//num_productos
        bar_chart.add(producto[1],[{'value':porcentaje, 'label':producto[0]}])
    return bar_chart.render()

def graficaLine():

    query = "select programa.nombre, programa.abreviacion, count(producto.nombre)" + \
    " from ((programa inner join tipo_actividad on programa.id_programa=tipo_actividad.id_programa)" + \
    " inner join producto on producto.id_tipo=tipo_actividad.id_tipo and producto.usbid_usu_creador=\'"+ session.usuario["usbid"] +\
    "\' and producto.estado=\'Validado\') group by programa.nombre, programa.abreviacion;"

    query2 = "select count(producto.nombre) from producto where producto.usbid_usu_creador=\'"+ session.usuario["usbid"]+"\' and producto.estado=\'Validado\';"

    datos = db.executesql(query)
    num_productos = db.executesql(query2)[0][0]

    import pygal
    line_chart = pygal.Line()
    for producto in datos:
        porcentaje = (producto[2]*100)//num_productos
        line_chart.add(producto[1],[{'value':porcentaje, 'label':producto[0]}])
    return line_chart.render()

def eliminar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

    archivo = request.args[0]
    comando = "rm ./applications/SiraDex/backup/" + archivo
    resp = os.system(comando)
    redirect(URL('index'))
