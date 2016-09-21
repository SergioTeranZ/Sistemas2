# -*- coding: utf-8 -*-
# try something like

def get_tipo_usuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL(c = "default",f="index"))
        if session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            elif(session.usuario["tipo"] == "Bloqueado"):      
                admin = -1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
        
    return admin

'''
Funcion que se encarga de obtener los datos para mostrar los catalogos
que existes en el sistema.
'''
def vGestionarCatalogo():
    # Obtengo el tipo del usuario para permitir el acceso a la visa
    # Limpio el Session del sistema.
    admin = get_tipo_usuario()
    session.nombreMostrar = ""
    session.nombreModificar = ""
    message = session.message
    session.message = ""
    # Se obtienen los nombres de todos los catalogos y se pasan al html.
    aux = db(db.CATALOGO).select(db.CATALOGO.nombre)
    return dict(admin = admin, catalogos = aux, message = message)

'''
Funcion que se encarga de agregar un catalogo a la
lista de catalogos existentes, en caso de que no exista
uno con el mismo nombre, se encarga de crearlo y almacenarlo
en la base de datos.
'''
def vAgregarCatalogo():
    # Se obtiene el tipo de usuario.
    admin = get_tipo_usuario()
    # Se crea un formulario para introducir un nombre
    forma=SQLFORM(
        db.CATALOGO,
        button=['Agregar'],
        fields=['nombre'],
        submit_button='Agregar',
        labels={'nombre':'Nombre'})
    if forma.accepts(request.vars, session):
        session.catAgregar = request.vars.nombre
        session.msgErr = 0
        redirect(URL('vAgregarCampos.html'))
    # En caso de que el formulario no sea aceptado
    elif forma.errors:
        session.message = 'Error en el formulario'
    else:
        session.message = ''
    return(dict(forma = forma, admin = admin))
    
'''
Funcion que se encarga de agregar un campo al catalogo,
crearlo y relacionarlo con el catalogo indicado.
'''
def vAgregarCampos():
    admin = get_tipo_usuario()
    # Obtengo el nombre del catalogo desde el objeto global 'session'
    nombreCat = session.catAgregar
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese catalogo
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL,db.CATALOGO.ALL)
    # Busco el id del catalogo
    id_cat = db(db.CATALOGO.nombre == nombreCat).select()[0].id_catalogo
    # Genero formulario para los campos
    form = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_cat', 'eliminar'],
                   labels = {'tipo_cat' : 'Tipo'}
                   )
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el campo al catalogo en caso de que no exista.
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        query2 = reduce(lambda a, b: (a&b), [db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,
                                             db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat])
        if len(db(query2).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vAgregarCampos'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    else:
        if(not(session.msgErr)):
            session.message = ''

    return dict(form = form, campos_guardados = campos_guardados,admin = admin)

'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux():
    session.message = 'Catalogo agregado exitosamente'
    redirect(URL('vGestionarCatalogo.html'))

    
'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux2():
    session.message = 'Catalogo editado exitosamente'
    redirect(URL('vGestionarCatalogo.html'))

'''
Funcion que se encarga de eliminar un catalogo, los campos
que este posee y todas las relaciones entre ellos.
'''
def eliminarCampos():
    # Obtengo el nombre del Catalogo
    if len(request.args)!=0:
        nombreCat = request.args[0]
        valorStr = ""
        for i in range(0,len(request.args[0])):
            if(request.args[0][i] == "_"):
                valorStr += " "
            else:
                valorStr += request.args[0][i]
        nombreCat = valorStr
    else:
        nombreCat = session.catAgregar
    # Construyo query para obtener la relacion entre los campos y el catalogo
    # que debo eliminar
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    
    # Guardo los resultados en 'aux'
    aux = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)
    
    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        aux2 = db(db.CAMPO.despliega_cat == aux[0].id_catalogo).select()
        db(db.VALORES_CAMPO_CATALOGO.id_catalogo == aux[0].id_catalogo).delete()
        if(len(aux2) >0):
            db(db.ACT_POSEE_CAMPO.id_campo == aux2[0]['id_campo']).delete()
        db(db.CATALOGO_TIENE_CAMPO.id_catalogo == aux[0].id_catalogo).delete()
        db(db.CAMPO.despliega_cat == aux[0].id_catalogo).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        query2 = reduce(lambda a,b: (a&b),[db.CAMPO_CATALOGO.id_campo_cat == row.id_campo_cat])
        aux3 = db(query2).select(db.CAMPO_CATALOGO.ALL)
        db(db.CAMPO_CATALOGO.id_campo_cat == aux3[0].id_campo_cat).delete()
        
    
    # Borro el catalogo
    db(db.CATALOGO.nombre == nombreCat).delete()
    
    redirect(URL('vGestionarCatalogo.html'))
    
'''
Funcion que se encarga de agregar valores a los
campos de un catalogo, en caso de que no exista
otra instancia con el mismo valor.
'''
def vAgregarElementoCampo():
    # Obtengo el tipo del usuario y el nombre del catalogo.
    admin = get_tipo_usuario()
    nombreCat = request.args[0]
    valorStr = ""
    for i in range(0,len(request.args[0])):
        if(request.args[0][i] == "_"):
            valorStr += " "
        else:
            valorStr += request.args[0][i]
    nombreCat = valorStr
    
    # Busco los campos asociados al catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    # Creo 2 arreglos para almacenar los campos y los id de cada campo.
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])

    # Obtengo el id del catalogo actual.
    id_cat = db(db.CATALOGO.nombre == nombreCat).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    iterador = len(cmpo)
    # Obtengo los ids de los campos
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    # Creo un arreglo con todos los campos del formulario.
    arreglo = []
    for i in range (0,len(cmpo)):
        arreglo += [ Field("pr"+str(i),'string', label=T(str(cmpo[i]))) ]
    if(len(arreglo) > 0):
        forma = SQLFORM.factory(
            *arreglo)
    else:
        session.message = "El catalogo no posee campos"
        redirect(URL('vGestionarCatalogo.html'))
    
    if len(request.vars)>0:
        for i in range(0,iterador):
            valor = request.vars["pr"+str(i)]
            
            # Genero un query para revisar si el valor existe en alguna instancia del campo.
            query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_cat,
                                                 db.VALORES_CAMPO_CATALOGO.id_campo_cat == ids[i]])
            if(len(db(query2).select()) > 0):
                session.nombreMostrar = nombreCat
                session.message = "El valor de un campo esta duplicado"
                redirect(URL('vMostrarCatalogo.html'))
                
        # Almaceno los valores en cada uno de los campos
        for i in range(0,iterador):
            valor = request.vars["pr"+str(i)]
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = ids[i], id_catalogo = id_cat, valor = valor)
        session.nombreMostrar = nombreCat
        redirect(URL('vMostrarCatalogo.html'))

    return (dict(forma = forma, admin = admin))

'''
Funcion encargada de mostrar todas las instancias
de los campos de un catalogo en una tabla.
'''
def vMostrarCatalogo():
    admin = get_tipo_usuario()
    # Obtengo el nombre del catalogo a mostrar
    if(session.nombreMostrar != ""):
        nombreCat = session.nombreMostrar
    else:
        nombreCat = request.args[0]
        valorStr = ""
        for i in range(0,len(request.args[0])):
            if(request.args[0][i] == "_"):
                valorStr += " "
            else:
                valorStr += request.args[0][i]
        nombreCat = valorStr
    
    # Creo 2 queries para buscar los campos que contiene el catalogo
    # y los valores de cada uno de ellos.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                       db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                       db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])
    
    # Guardo los resultados del los queries creados
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL)
    id_campos = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)
    valores_campos = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    nroCampos = len(campos_guardados)
    nroValores = len(valores_campos)

    # Calculo el numero de filas que debera mostrar la tabla.
    if(nroCampos != 0):
        nroFilas = nroValores/nroCampos
    else:
        nroFilas = 0
    
    # Arreglos auxiliares para almacenar las filas y las columnas de la tabla
    filas = []
    columnas = []
    j = 0
    # Creo las columnas de la tabla (Los valores de cada campo)
    for i in range(0,len(id_campos)):
        arr = []
        id_act = id_campos[i]['id_campo_cat']
        for j in range(0,len(valores_campos)):
            if(valores_campos[j]['id_campo_cat'] == id_act):
                arr.append(valores_campos[j])
        columnas.append(arr)
    j = 0
    # Creo las filas que se mostraran en la tabla.
    for i in range(0,nroFilas):
        aux = []
        for j in range(0,len(columnas)):
            aux.append(columnas[j][i])
        filas.insert(-1,aux)
    # Guardo las filas globalmente para poder acceder a ellas de forma sencilla y eficiente.
    session.filas = filas
    return dict(campos_guardados = campos_guardados,filas = filas, admin = admin, nombre = nombreCat)

'''
Funcion que se encarga de modificar el valor de una
instancia de los campos de un catalogo.
'''
def vModificarCampos():
    # Obtengo el tipo de usuario y el nombre del campo a modificar.
    admin = get_tipo_usuario()
    valorStr = ""
    for i in range(0,len(request.args[0])):
        if(request.args[0][i] == "_"):
            valorStr += " "
        else:
            valorStr += request.args[0][i]
    # Busco el diccionario al cual esta asociado la fila de campos que deseo modificar.
    for j in session.filas[int(request.args[1])]:
        if j['valor']==valorStr:
            diccionario = j
            dcc = session.filas[int(request.args[1])]

    # Creo un query para sacar los campos que tiene el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    # Guardo los resultados del query en aux
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    nombreCat = db(query).select(db.CATALOGO.nombre)[0]['nombre']
    # Arreglos auxiliares para guardar los nombres y ids de los campos respectivamente.
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])

    id_cat = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    
    # Ids de los campos
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    print(ids[0])
    arreglo = []
    df =None
    # Almaceno los campos a mostrar en el formulario
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']
        if df != None:
            arreglo += [ Field("pr"+str(i),'string',default= df, label=T(str(cmpo[i]))) ]
    forma = SQLFORM.factory(
        *arreglo)
    # Reviso si ningun valor esta duplicado para luego insertarlo en la base.
    if len(request.vars)>0:
        for i in range(0,len(cmpo)):
            for f in dcc:
                if(f['id_campo_cat'] == ids[i]):
                    df = f['valor']
            valor = request.vars["pr"+str(i)]
            if(valor != df):
                query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_cat,
                                                     db.VALORES_CAMPO_CATALOGO.id_campo_cat == ids[i]])
                if(len(db(query2).select()) > 0):
                    session.nombreMostrar = nombreCat
                    session.message = "El valor de un campo esta duplicado"
                    redirect(URL('vMostrarCatalogo.html'))
        for i in range(0,len(cmpo)):
            for f in dcc:
                if(f['id_campo_cat'] == ids[i]):
                    df = f['valor']
            valor = request.vars["pr"+str(i)]
            db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = ids[i], id_catalogo = id_cat, valor = valor)
        session.nombreMostrar = nombreCat
        redirect(URL('vMostrarCatalogo.html'))
    return (dict(forma = forma, admin = admin))

'''
Funcion que se encarga de eliminar una instancia
de los campos de un catalogo.
'''
def eliminarValorCampo():
    # Obtengo el tipo del usuario y el nombre del campo a eliminar.
    admin = get_tipo_usuario()
    valorStr = ""
    for i in range(0,len(request.args[0])):
        if(request.args[0][i] == "_"):
            valorStr += " "
        else:
            valorStr += request.args[0][i]
    for dic in session.filas:
        for i in dic:
            if i['valor']==valorStr:
                diccionario = i
                dcc = dic
    # Geero un query para buscar los campos que tiene el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    # Arreglos auxiliares para guardar los campos y los ids respectivamente.
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])
    id_cat = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    
    # Ids de los campos
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    # Voy eliminando el valor de cada campo de la fila seleccionada
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']
        db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
    session.nombreMostrar = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.nombre)[0]['nombre']
    redirect(URL('vMostrarCatalogo.html'))

'''
Funcion que se encarga de modificar un catalogo
permitiendo agregar o eliminar campos del mismo.
'''
def vModificarCatalogo():
    # Obtengo el tipo del usuario conectado.
    admin = get_tipo_usuario()
    # Obtengo el nombre del catalogo a modificar.
    if(session.nombreModificar != ""):
        nombreCat = session.nombreModificar
    else:
        nombreCat = request.args[0]
        valorStr = ""
        for i in range(0,len(request.args[0])):
            if(request.args[0][i] == "_"):
                valorStr += " "
            else:
                valorStr += request.args[0][i]
        nombreCat = valorStr
    
    # Creo 2 querys para buscar los valores de los campos y los campos que hay en el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])

    # Guardo los resultados de dichos queries
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO.ALL)
    valores = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    campos = db(query).select(db.CAMPO_CATALOGO.ALL)

    if(len(campos) > 0):
        total = len(valores)/len(campos)
    else:
        total = 0
    # Busco el id del catalogo
    id_cat = db(db.CATALOGO.nombre == nombreCat).select()[0].id_catalogo

    # Genero formulario para los campos
    form = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_cat', 'eliminar'],
                   labels = {'tipo_cat' : 'Tipo'}
                   )
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el campo en caso de que este no exista.
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        query2 = reduce(lambda a, b: (a&b), [db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,
                                             db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat])
        if len(db(query2).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            valor_aux = " "
            for i in range(0,total):
                db.VALORES_CAMPO_CATALOGO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo, valor = valor_aux*(i+1))
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        session.nombreModificar = nombreCat
        redirect(URL('vModificarCatalogo'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        if(not(session.msgErr)):
            session.message = ''

    return dict(form = form, campos_guardados = campos_guardados,admin = admin)

'''
Funcion que se encarga de eliminar un campo del catalogo,
eliminando todas las relaciones existentes e instancias 
del catalogo.
'''
def eliminarCampos2():
    # Obtengo el nombre del catalogo
    if len(request.args)!=0:
        nombreCat = request.args[0]
    else:
        nombreCat = session.catAgregar

    # Elimino todas las relaciones relacionadas con el campo
    db(db.CATALOGO_TIENE_CAMPO.id_campo_cat == request.args[1]).delete()
    db(db.VALORES_CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()

    db(db.CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()
    session.nombreModificar = nombreCat
    
    redirect(URL('vModificarCatalogo.html'))
