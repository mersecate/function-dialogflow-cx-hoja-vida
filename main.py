from xhtml2pdf import pisa             # import python module
from google.cloud import storage
import uuid
import mysql.connector
from mysql.connector import connect, Error
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from google.cloud import firestore
from email.mime.application import MIMEApplication
import os
import ast
import io
import json

def gerar_pdf(request):
    

    # Importar secretos
    secretos = os.environ.get("secretos")
    secretos = ast.literal_eval(secretos)

    request_json = request.get_json()

    session_id_temp=request_json['sessionInfo']['session'].split('/')[-1]
    if "|" in session_id_temp:
      session_id = str(session_id_temp.split("|")[0])
    else:
      session_id = session_id_temp

    sessionInfo = request_json['sessionInfo'];
    parametrosSesion = sessionInfo['parameters'];
    ambiente = parametrosSesion['ambiente']

    notiene = ""

    if parametrosSesion['nombre']:
        nombre = parametrosSesion['nombre']
    else:
        nombre=notiene

    if parametrosSesion['cargo']:
        cargo = parametrosSesion['cargo']
    else:
        cargo = notiene

    if parametrosSesion['email']:
        email = parametrosSesion['email']
    else:
        email = notiene

    if parametrosSesion['telefono']:
        telefono = parametrosSesion['telefono']
    else:
        telefono = notiene

    # if parametrosSesion['ciudad']:
    #     ciudad = parametrosSesion['ciudad']
    # else:
    #     ciudad = notiene

    if parametrosSesion['nivelestudiomasalto']:
        nivelestudiomasalto = parametrosSesion['nivelestudiomasalto']
    else:
        nivelestudiomasalto = notiene

    if parametrosSesion['nivelestudiomasalto_titulo']:
        nivelestudiomasalto_titulo = parametrosSesion['nivelestudiomasalto_titulo']
    else:
        nivelestudiomasalto_titulo = notiene

    if parametrosSesion['nivelestudiomasalto_institucion']:
        nivelestudiomasalto_institucion = parametrosSesion['nivelestudiomasalto_institucion']
    else:
        nivelestudiomasalto_institucion = notiene

    if parametrosSesion['nivelestudiomasalto_formacion']:
        nivelestudiomasalto_formacion = str(int(round(parametrosSesion['nivelestudiomasalto_formacion'],0)))
    else:
        nivelestudiomasalto_formacion = notiene

    # try:
    #     if parametrosSesion['formacionuniversitaria']:
    #         formacionuniversitaria = parametrosSesion['formacionuniversitaria']
    #     else:
    #         formacionuniversitaria = notiene
    # except:
    #     formacionuniversitaria = notiene
    #     pass

    # try:
    #     if parametrosSesion['formacionuniversitaria_titulo']:
    #         formacionuniversitaria_titulo = parametrosSesion['formacionuniversitaria_titulo']
    #     else:
    #         formacionuniversitaria_titulo = notiene
    # except:
    #     formacionuniversitaria_titulo = notiene
    #     pass

    # try:
    #     if parametrosSesion['formacionuniversitaria_institucion']:
    #         formacionuniversitaria_institucion = parametrosSesion['formacionuniversitaria_institucion']
    #     else:
    #         formacionuniversitaria_institucion =notiene
    # except:
    #     formacionuniversitaria_institucion = notiene
    #     pass

    # try:
    #     if parametrosSesion['formacionuniversitaria_formacion']:
    #         formacionuniversitaria_formacion = parametrosSesion['formacionuniversitaria_formacion']
    #     else:
    #         formacionuniversitaria_formacion = notiene
    # except:
    #     formacionuniversitaria = notiene
    #     pass


    if parametrosSesion['experiencialaboral']:
        experiencialaboral = parametrosSesion['experiencialaboral']
    else:
        experiencialaboral = notiene

    if experiencialaboral != "No":
        experiencialaboral_empresa = parametrosSesion['experiencialaboral_empresa']
    else:
        experiencialaboral_empresa = notiene

    if experiencialaboral != "No":
        experiencialaboral_puesto = parametrosSesion['experiencialaboral_puesto']
    else:
        experiencialaboral_puesto = notiene

    if experiencialaboral != "No":
        experiencialaboral_fecha = str(int(round(parametrosSesion['experiencialaboral_fecha']['day'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_fecha']['month'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_fecha']['year'],0)))
        experiencialaboral_fecha_bd = str(int(round(parametrosSesion['experiencialaboral_fecha']['year'],0)))+"-"+str(int(round(parametrosSesion['experiencialaboral_fecha']['month'],0)))+"-"+str(int(round(parametrosSesion['experiencialaboral_fecha']['day'],0)))
    else:
        experiencialaboral_fecha =notiene
        

    if experiencialaboral != "No": 
        experiencialaboral_actualidad = parametrosSesion['experiencialaboral_actualidad']
    else:
        experiencialaboral_actualidad =notiene

    if experiencialaboral != "No": 
        if experiencialaboral_actualidad == "Sí":
            experiencialaboral_cese = "Actualidad"
            experiencialaboral_cese_bd = ""
            trabajandoMismoTrabajo = 1
        else:
            trabajandoMismoTrabajo = 0
            experiencialaboral_cese = str(int(round(parametrosSesion['experiencialaboral_cese']['day'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_cese']['month'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_cese']['year'],0)))
            experiencialaboral_cese_bd = str(int(round(parametrosSesion['experiencialaboral_cese']['year'],0)))+"-"+str(int(round(parametrosSesion['experiencialaboral_cese']['month'],0)))+"-"+str(int(round(parametrosSesion['experiencialaboral_cese']['day'],0)))
    else:
        experiencialaboral_cese = notiene

    if experiencialaboral != "No":
        if parametrosSesion['experiencialaboral_funciones'] == 'No quiero describir las funciones':
            experiencialaboral_funciones = notiene
        else:
            experiencialaboral_funciones = parametrosSesion['experiencialaboral_funciones']
    else:
        experiencialaboral_funciones = notiene

    if experiencialaboral != "No":
        if parametrosSesion['experiencialaboral_logros'] == 'No quiero describir los logros':
            experiencialaboral_logros = notiene
        else:
            experiencialaboral_logros = parametrosSesion['experiencialaboral_logros']
    else:
        experiencialaboral_logros = notiene


    # if experiencialaboral == "No":
    #     otra_experiencia = "No"
    # else:
    #     otra_experiencia = parametrosSesion['otra_experiencia']

    # if otra_experiencia != "No":
    #     experiencialaboral_empresa2 = parametrosSesion['experiencialaboral_empresa2']
    # else:
    #     experiencialaboral_empresa2 = notiene

    # if otra_experiencia != "No":
    #     experiencialaboral_puesto2 = parametrosSesion['experiencialaboral_puesto2']
    # else:
    #     experiencialaboral_puesto2 = notiene

    # if otra_experiencia != "No":
    #     experiencialaboral_fecha2 = str(int(round(parametrosSesion['experiencialaboral_fecha2']['day'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_fecha2']['month'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_fecha2']['year'],0)))
    # else:
    #     experiencialaboral_fecha2 = notiene

    # if otra_experiencia != "No":
    #     experiencialaboral_cese2 = str(int(round(parametrosSesion['experiencialaboral_cese2']['day'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_cese2']['month'],0)))+"/"+str(int(round(parametrosSesion['experiencialaboral_cese2']['year'],0)))
    # else:
    #     experiencialaboral_cese2 = notiene

    # if otra_experiencia == "No":
    #     experiencialaboral_funciones2 = notiene
    # else:
    #     if parametrosSesion['experiencialaboral_funciones2'] == 'No quiero describir las funciones':
    #         experiencialaboral_funciones2 = notiene
    #     else:
    #         experiencialaboral_funciones2 = parametrosSesion['experiencialaboral_funciones2']

    # if otra_experiencia == "No":
    #     experiencialaboral_logros2 =notiene
    # else:
    #     if parametrosSesion['experiencialaboral_logros2'] == 'No quiero describir los logros':
    #         experiencialaboral_logros2 =notiene
    #     else:
    #         experiencialaboral_logros2 = parametrosSesion['experiencialaboral_logros2']

    # try:
    #     if parametrosSesion['idioma']:
    #         idioma = parametrosSesion['idioma']
    #     else:
    #         idioma = notiene
    # except:
    #     idioma = notiene
    #     pass

    # if idioma == notiene:
    #     nivel_idioma = notiene
    # else:
    #     nivel_idioma = parametrosSesion['nivel_idioma']

    if parametrosSesion['perfil_professional'] == "No quiero describir un perfil profesional":
        perfil_professional = notiene
    else:
        perfil_professional = parametrosSesion['perfil_professional']
        
    # if parametrosSesion['poblaciones_vulnerables'] == "Yo no pertenezco a ninguna de estas poblaciones":
    #     poblaciones_vulnerables =notiene
    # else:
    #     poblaciones_vulnerables = parametrosSesion['poblaciones_vulnerables']

    # if parametrosSesion['poblaciones_etnicas'] == "No pertenezco a ninguna de estas poblaciones étnicas":
    #     poblaciones_etnicas =notiene
    # else:
    #     poblaciones_etnicas = parametrosSesion['poblaciones_etnicas']
        
    # if parametrosSesion['poblaciones_discapacidad'] == "No tengo ningun tipo de discapacidad":
    #     poblaciones_discapacidad = notiene 
    # else:
    #     poblaciones_discapacidad = parametrosSesion['poblaciones_discapacidad']

    if experiencialaboral == "No":
        html_experiencialaboral = ""
    else:
        html_experiencialaboral = f"""<tr> <td> <div> <h3 style="line-height: 0; padding-top: 5px;">{experiencialaboral_puesto}</h3> </div> <div style="padding-bottom: 3px;"><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;" >{experiencialaboral_empresa}</span></div> <div style="display: flex;"> <span>{experiencialaboral_fecha} - {experiencialaboral_cese}</span> </div> <ul style="padding-bottom: 5px;"> <li> {experiencialaboral_funciones} </li> </ul> </td> </tr> <tr> <td> <div style = "border-top: dashed grey 1px; border-bottom: dashed grey 1px; padding-top: 10px; padding-bottom: 10px;"> <span>{experiencialaboral_logros}</span> </div> </td> </tr>"""
    
    # if otra_experiencia == "Sí":
    #     html_otra_experiencia = f"""<tr> <td> <div> <h3 style="line-height: 0; padding-top: 5px;">{experiencialaboral_puesto2}</h3> </div> <div style="padding-bottom: 3px;"><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;" >{experiencialaboral_empresa2}</span></div> <div style="display: flex;"> <span>{experiencialaboral_fecha2} - {experiencialaboral_cese2}</span> </div> <ul style="padding-bottom: 5px;"> <li> {experiencialaboral_funciones2} </li> </ul> </td> </tr> <tr> <td> <div style ="border-top: dashed grey 1px; border-bottom: dashed grey 1px; padding-top: 10px; padding-bottom: 10px;"> <span>{experiencialaboral_logros2}</span> </div> </td> </tr>"""
    # else:
    #     html_otra_experiencia = ""

    # if formacionuniversitaria == "Sí":
    #     html_formacionuniversitaria = f"""<tr> <td style="width: 800px;"> <div> <h3 style="line-height: 0; padding-top: 5px">{formacionuniversitaria_titulo}</h3> </div> <div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">{formacionuniversitaria_institucion}</span></div> <div style="padding-top: 5px;"> {formacionuniversitaria_formacion} </div> </td> </tr>"""
    # else:
    #     html_formacionuniversitaria = ""

    # if idioma != notiene:
    #     html_idioma = f"""<div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">{idioma}</span></div> <div> <ul> <li>{nivel_idioma}</li> </ul> </div>"""
    # else:
    #     html_idioma = ""
    
    if perfil_professional == notiene:
        html_perfil_profissional = ""
    else:
        html_perfil_profissional = f"""<table style="width: 800px;"> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">PERFIL PROFESIONAL</h3> </div> </td> </tr> <tr> <td style = "padding-top: 5px;"> <span>{perfil_professional}</span> </td> </tr> </table>"""


    # if poblaciones_vulnerables == notiene:
    #     html_poblaciones_vulnerables = ""
    # else:
    #     html_poblaciones_vulnerables = f"""<ul> <li>{poblaciones_vulnerables}</li> </ul>"""

    # if poblaciones_etnicas == notiene:
    #     html_poblaciones_etnicas = ""
    # else:
    #     html_poblaciones_etnicas = f"""<ul> <li>{poblaciones_etnicas}</li> </ul>"""

    # if poblaciones_discapacidad == notiene:
    #     html_poblaciones_discapacidad = ""
    # else:
    #     html_poblaciones_discapacidad = f"""<ul> <li>{poblaciones_discapacidad}</li> </ul>"""

    # if poblaciones_vulnerables != notiene or poblaciones_etnicas != notiene or poblaciones_discapacidad != notiene:
    #     html_poblaciones = f"""<table style="width: 800px; "> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">POBLACIÓN</h3> </div> </td> </tr> <tr> <td> <div style="padding-top: 5px;"> {html_poblaciones_vulnerables} {html_poblaciones_etnicas} {html_poblaciones_discapacidad} </div> </td> </tr> </table>"""
    # else:
    #     html_poblaciones = ""


    #source_html = f"""<!DOCTYPE html><html lang="pt-br"><head> <title>Hoja de vida</title> <meta charset="utf-8"> <link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&display=swap" rel="stylesheet"> <link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet"></head><header> <div style="margin-top: 25px;"> <table style="width: 800px; padding: 0;"> <tr> <td style="width: 800px; padding: 0;"> <div style="padding-left: 30px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;"><span>{nombre}</span></div> <div style="padding-left: 30px; margin-top: 5px; font-weight: 600; font-size: 16pt; color: #30539B;"><span>{cargo}</span></div> <div style="padding-left: 30px; margin-top:5px; padding-bottom: 5px;"> <div> <span>{email}</span> </div> <div> <span>{telefono}</span> </div> <div> <span>{ciudad}</span> </div> </td> </tr> </table> </div></header><body style="font-size: 14px; font-family: 'Barlow Semi Condensed', sans-serif; color: #4e4e4e; font-weight: 500; margin: 0;" > <div style="margin-left: 30px; padding-top: 10px;"> <table style="width: 800px; "> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 10px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EXPERIENCIA</h3> </div> </td> </tr> {html_experiencialaboral} {html_otra_experiencia} </table> <table style="width: 800px;"> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); padding-top: 10px; width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EDUCACIÓN</h3> </div> </td> </tr> <tr> <td style="width: 800px;"> <div> <h3 style="line-height: 0; padding-top: 5px">{nivelestudiomasalto} - {nivelestudiomasalto_titulo}</h3> </div> <div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">{nivelestudiomasalto_institucion}</span></div> <div style="padding-top: 5px;"> {nivelestudiomasalto_formacion} </div> </td> </tr> {html_formacionuniversitaria} </table> {html_perfil_profissional} <table style="width: 800px; "> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">IDIOMA</h3> </div> </td> </tr> <tr> <td style = "padding-top: 5px;"> <div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">Español</span></div> {html_idioma} </td> </tr> </table> {html_poblaciones} </div> <div style=" margin-left: 175px; padding-top: 30px;">Hoja de Vida generada por la Secretaría de Desarrollo Económico - Bogotá</div></body></html>"""
    source_html = f"""<!DOCTYPE html><html lang="pt-br"> <head> <title>Hoja de vida</title> <meta charset="utf-8"> <link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&display=swap" rel="stylesheet"> <link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet"> </head> <header> <div style="margin-top: 25px;"> <table style="width: 800px; padding: 0;"> <tr> <td style="width: 800px; padding: 0;"> <div style="padding-left: 30px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;"><span>{nombre}</span></div> <div style="padding-left: 30px; margin-top: 5px; font-weight: 600; font-size: 16pt; color: #30539B;"><span>{cargo}</span></div> <div style="padding-left: 30px; margin-top:5px; padding-bottom: 5px;"> <div> <span>{email}</span> </div> <div> <span>{telefono}</span> </div> </td> </tr> </table> </div> </header> <body style="font-size: 14px; font-family: 'Barlow Semi Condensed', sans-serif; color: #4e4e4e; font-weight: 500; margin: 0;" > <div style="margin-left: 30px; padding-top: 10px;"> <table style="width: 800px; "> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 10px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EXPERIENCIA</h3> </div> </td> </tr> {html_experiencialaboral} </table> <table style="width: 800px;"> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); padding-top: 10px; width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EDUCACIÓN</h3> </div> </td> </tr> <tr> <td style="width: 800px;"> <div> <h3 style="line-height: 0; padding-top: 5px">{nivelestudiomasalto} - {nivelestudiomasalto_titulo}</h3> </div> <div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">{nivelestudiomasalto_institucion}</span></div> <div style="padding-top: 5px;"> {nivelestudiomasalto_formacion} </div> </td> </tr> </table> {html_perfil_profissional} </div> <div style=" margin-left: 175px; padding-top: 30px;">Hoja de Vida generada por la Secretaría de Desarrollo Económico - Bogotá</div> </body></html>"""
    
    
    storage_client = storage.Client()
    bucket = storage_client.bucket("storage-hojadevida-hml")
    file_name = str(uuid.uuid4())+".pdf"
    blob = bucket.blob(file_name)



    with blob.open("wb") as result_file:
        #f.write("teste")
        
        #result_file = open(output_filename, "w+b")

        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
                source_html,                # the HTML to convert
                dest=result_file)           # file handle to recieve result

    # close output file
        result_file.close()                 # close output file



    
    token_result = generateToken(file_name)
    url_file = "https://us-west1-bogotatrabaja-hml.cloudfunctions.net/function-dialogflow-get-file?token="+token_result+"&namefile="+file_name

    jsonResponse = {
        "fulfillment_response": {
            "messages": [
            {
                "payload": {
                "richContent": [
                [
                {
                    "text": "Hoja de vida resumida",
                    "icon": {
                    "color": "#1E88E5",
                    "type": "article"
                    },
                    "link": url_file,
                    "type": "button"
                }
                ]
            ]
            }
            }
            ]
        }
        }

    print(jsonResponse) 
    #REALIZA AS INSERÇÕES/EDIÇÕES NO BD
    session_id_int = int(session_id)


    if ambiente != "portal":
        #if ambiente == "DEV":
        #    host_conexao = "34.168.40.198"
        #    print("Está em DEV ",host_conexao)
        #    senha_conexao = os.environ.get("password_dev", "")
        if ambiente == "HML":
            host_conexao = secretos["dgflow_mysql_host_HML"]
            senha_conexao = secretos["dgflow_mysql_password_HML"]
            print("Está em HML ",host_conexao)
        elif ambiente == "PROD":
            host_conexao = secretos["dgflow_mysql_host_PROD"]
            senha_conexao = secretos["dgflow_mysql_password_PROD"]
            print("Está em PROD ",host_conexao)
        
        try:
            with connect(
                host=host_conexao,
                user='chatbot',
                password=senha_conexao,
            ) as connection:
                #UPDATE DE COMPLEMENTOS: CARGO E CELULAR
                db_update_complementos = f"UPDATE `agata-develop`.user_complemento SET celular = '{telefono}', cargo= '{cargo}' WHERE id_users='{session_id}'"  
                with connection.cursor() as cursor:
                    cursor.execute(db_update_complementos)
                    connection.commit()
                    
                
                #VERIFICAÇÃO SE USUÁRIO JÁ INICIOU UM CURRÍCULO, CASO NÃO TENHA INICIADO, INICIA UMA INSTÂNCIA DE CURRÍCULO:
                #db_tem_curriculo = f"SELECT * FROM `agata-develop`.user_curriculo WHERE id_users='{session_id}'"  
                db_tem_curriculo = f"SELECT * FROM `agata-develop`.user_curriculo WHERE id_users=%s"
                with connection.cursor() as cursor:
                    cursor.execute(db_tem_curriculo, (session_id,))
                    result = cursor.fetchall()
                    if len(result)>0:
                        id_curriculo = str(result[0][0])
                        print("id curriculo:" + id_curriculo)
                        db_update_curriculo = f"UPDATE `agata-develop`.user_curriculo SET perfil_laboral = '{perfil_professional}' WHERE id_users='{session_id}'"  
                        cursor.execute(db_update_curriculo)
                        connection.commit()
                    else:
                        db_insere_curriculo = f"""INSERT INTO `agata-develop`.user_curriculo (id_users, estado_civil, tipo_doc_adicional,
                            numero_doc_adicional, sexo, pais_nascimento, nacionalidad,
                            perfil_laboral, departamento_nacimiento, municipio_nacimiento,
                            libreta_militar, tipo_libreta, numero_libreta,
                            reconoce_focalizada, jefe_hogar, id_Afrocolombianos,
                            id_Indigenas, id_Negros, id_Palenqueros, id_Raizales, id_Rrom,
                            id_Fisica, id_Cognitiva, id_Sordoceguera, id_Multiple,
                            id_Psicosocial, id_Auditiva, id_Estuvo, id_Personas,
                            id_Retornado, id_Vend_informales, id_Problema, id_Epilepsia,
                            id_Consumo, id_Transtorno, id_Victima, id_visual,
                            id_victima_conflicto_armado, id_victima_violencia_genero,
                            id_vendedor_informal, id_reciclador, id_problacion_rural,
                            id_problacion_libertad_3_meses, id_personas_probreza,
                            id_persona_victima_trata, id_persona_trans,
                            id_persona_act_sexuales, id_persona_migrante, id_persona_mayor_50,
                            id_persona_joven, id_persona_habitabilidad, id_jovem_mayor,
                            otro_telefono, observaciones, pais_retornado, pais_residencia,
                            departamento_residencia, municipio_residencia, bairro_residencia,
                            pertence, prestador_preferencia, punta_atencion, local,
                            id_coordenada, id_coordenada_02, id_coordenada_03,
                            id_coordenada_04, id_coordenada_05, id_coordenada_06,
                            id_coordenada_07, id_coordenada_08, id_coordenada_09,
                            tipo_complemento, complemento, codigo_postal,
                            direccion_residencia, situacion_laboral_actual,
                            aspiracion_salarial, Interes_ofertas_teletrabajo,
                            posibilidad_trasladarse, possibilidade_viajar, conduces_carro,
                            categoria_licencia_carro, conduces_moto, categoria_licencia_moto,
                            Prop_medio_transporte, desc_url, finalizado) VALUES ({session_id_int}, NULL, NULL, NULL, NULL, NULL, NULL, '{perfil_professional}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)"""
                        cursor.execute(db_insere_curriculo)
                        connection.commit()
                        id_curriculo = str(cursor.lastrowid)
                        print("id curriculo:" +id_curriculo)
                id_curriculo = int(id_curriculo)

                #INSERE NA BASE DE DATOS LA INFOMACIÓN DE NIVEL MAS ALTO DE ESTUDIO
                with connection.cursor() as cursor:
                   db_insere_nivel_educativo = f"""INSERT INTO `agata-develop`.curriculo_nivel_educativo (id_user_curriculo, interessadoPractica, nivelEducativo, 
                       tituloObtenido, tituloHomologado, areaDesempeno,
                       nucleoConocimiento, Institucion, paisDelCurso, estadoDelCurso,
                       fechafinalizacion, idObservaciones) VALUES ({id_curriculo}, 0, '{nivelestudiomasalto}', '{nivelestudiomasalto_titulo}', '', '', '', '{nivelestudiomasalto_institucion}', '', '', '{nivelestudiomasalto_formacion}', '')"""
                   cursor.execute(db_insere_nivel_educativo)
                   connection.commit()
                print("Nivel educativo atualizado")
                
                if experiencialaboral != "No":
                    experiencialaboral_funciones_logros = experiencialaboral_funciones+" "+experiencialaboral_logros
                    #INSERE NA BASE DE DATOS LA INFOMACIÓN DE EXPERIENCIA LABORAL
                    with connection.cursor() as cursor:
                        db_insere_experiencia_laboral = f"""INSERT INTO `agata-develop`.curriculo_experiencia_laboral (id_user_curriculo, funcionesLogros, tpExperienciaLaboral,
                        productoServicio, cuaPersonasTrabajan, sector, cargo,
                        cargoEquivalente, nombreEmpresa, telefonoEmpresa, paisEmpresa,
                        fechaIngresso, trabajandoMismoTrabajo, fechaRetiro) VALUES ({id_curriculo}, '{experiencialaboral_funciones_logros}', '', '', '', '', '{experiencialaboral_puesto}', '', '{experiencialaboral_empresa}', '', '', '{experiencialaboral_fecha_bd}', {trabajandoMismoTrabajo}, '{experiencialaboral_cese_bd}')"""
                        cursor.execute(db_insere_experiencia_laboral)
                        connection.commit()
                    print("Experiencia atualizada")

                connection.close()
        except Exception as e:
            print('Error: '+str(e))


    #ENVIO DO EMAIL AO CANDIDATO:
    url = "https://storage.googleapis.com/storage-hojadevida-hml/"+str(file_name)
    sender_name = "Bogotá Trabaja"
    sender_email = "proyectoempleo@desarrolloeconomico.gov.co"

    receiver = email
    password = secretos["dgflow_email_password"]

    # Create an instance of MIMEMultipart which can include multiple parts.
    # `alternative` means only one part will be shown and it's last in first out.
    message = MIMEMultipart("alternative")

    # The headers should be set to the root MIMEMultipart instance.
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver
    message["Subject"] = "Hoja de vida - VCC"
    
    # AJUSTE ENVIO DE CORREO DE FORMA ASINCRONA

    storage_client = storage.Client()
    bucket = storage_client.bucket('storage-hojadevida-hml')
    blob = bucket.blob(file_name)
    stream = io.BytesIO()
    blob.download_to_file(stream)
    #
    part = MIMEApplication(stream.getvalue(),Name=file_name)
    part['Content-Disposition'] = 'attachment; filename="%s"' % file_name


    # Create another leaf part, which is also an instance of MIMEText.
    html_markup = f"""<h1 style="color: #02266C;">¡Hola, {nombre}!</h1> <p>Espero que te encuentres bien.</p> <p>Soy Chatico, tu asistente virtual de empleo.</p> <p>Abajo encontrarás el enlace a tu hoja de vida que generé para ti.</p> <p style="text-align: center; margin-top: 20px;"> <a href="{url}" style="display: inline-block; padding: 10px 20px; background-color: #02266C; color: #fff; text-decoration: none; font-weight: bold;">Hoja de vida resumida</a> </p> <p>Saludos cordiales,</p> <p>Chatico</p>"""
    # For this one, we need to change the type to `html`.
    mime_html = MIMEText(html_markup, "html")
    message.attach(mime_html)
    message.attach(part)

    with smtplib.SMTP_SSL(
        host="smtp.gmail.com", port=465, context=ssl.create_default_context()
    ) as server:
        server.login(sender_email, password)

        server.sendmail(
            from_addr=sender_email,
            to_addrs=receiver,
            msg=message.as_string(),
        )

    
    return jsonResponse

def generateToken(filename):
    documentID=""
    data = {"fileName": filename}
    db = firestore.Client() 
    #doc_ref = db.collection("curriv").document(documentID)    
    #doc_ref.set(data)
    update_time, doc_ref  = db.collection("curriv").add(data)      
    documentID=doc_ref.id
    return documentID
