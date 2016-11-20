import os
import datetime
from funciones_siradex import get_tipo_usuario
import time

def index():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))
      
    backups = os.listdir("./applications/SiraDex/backup")

    form = formulario_restaurar_backup()

    if form.process(formname = "form", table_name='archivos').accepted:

        print form.vars.backup
    #        comando = "psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/backup/" + archivo

    #        resp = os.system(comando)

        redirect(URL('index'))

    elif form.errors:
        response.flash = 'el formulario tiene errores'


    return locals()

def generar_backup():

    admin = get_tipo_usuario(session)
    
    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))
      

    fecha = time.asctime(time.localtime(time.time()))
    archivo = "_".join(fecha.split()[1:]).replace(":","") + ".sql"
    comando = "pg_dump -d Siradex -U Siradex -h localhost -w > ./applications/SiraDex/backup/backup_" + archivo
    resp = os.system(comando)

    redirect(URL('index'))

def formulario_restaurar_backup():

    admin = get_tipo_usuario(session)
    
    if(admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))
      
    fields = []

    fields.append(Field("backup", 'upload', autodelete=True, uploadfolder="./applications/SiraDex/backup/", label=''))

    form=SQLFORM.factory(*fields,upload=URL('download')) 
    form.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    form.element(_type='submit')['_value']="Agregar"

    return form

def restaurar_backup():

    admin = get_tipo_usuario(session)
    
    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))
      
    archivo = request.args[0]

    comando = "psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/SQLScripts/dropSIRADEx.sql && psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/backup/" + archivo

    resp = os.system(comando)
    #resp = 0
    if (resp == 0):
        response.flash="Restaurado."
    else:
        response.flash="No se pudo restaurar."
    
    redirect(URL('index'))



def download():
    return response.download(request, db)

def eliminar():
    archivo = request.args[0]
    comando = "rm ./applications/SiraDex/backup/" + archivo
    resp = os.system(comando)
    redirect(URL('index'))    