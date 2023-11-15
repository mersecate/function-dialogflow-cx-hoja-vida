import os
import ast
import asyncio

from mysql.connector import connect

from utils import *

# Function to generate a PDF document based on input data
def gerar_pdf(request):
    # Retrieve secrets from environment variables
    secretos = os.environ.get("secretos")
    secretos = ast.literal_eval(secretos)

    # Extract JSON data from the incoming request
    request_json = request.get_json()

    # Extract session information from the request
    session_id_temp=request_json['sessionInfo']['session'].split('/')[-1]
    if "|" in session_id_temp:
      session_id = str(session_id_temp.split("|")[0])
    else:
      session_id = session_id_temp

    sessionInfo = request_json['sessionInfo']
    parametrosSesion = sessionInfo['parameters']
    ambiente = parametrosSesion['ambiente']

    # Define function_name and bucket_name based on the environment
    if ambiente == "HML":
        function_name = "projects/bogotatrabaja-hml/locations/us-west1/functions/function-dialogflow-cx-send-email"
        bucket_name = "storage-hojadevida-hml"
    elif ambiente == "PROD":
        function_name = "projects/bogotatrabaja-prd/locations/us-west1/functions/function-dialogflow-cx-send-email"
        bucket_name = "storage-hojadevida-prod"

    # Extracting user information from the request parameters
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
        nivelestudiomasalto_formacion = str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['day'],0)))+"/"+str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['month'],0)))+"/"+str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['year'],0)))
        nivelestudiomasalto_formacion_bd = str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['year'],0)))+"-"+str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['month'],0)))+"-"+str(int(round(parametrosSesion['nivelestudiomasalto_formacion']['day'],0)))
    else:
        nivelestudiomasalto_formacion = notiene

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
    if parametrosSesion['perfil_professional'] == "No quiero describir un perfil profesional":
        perfil_professional = notiene
    else:
        perfil_professional = parametrosSesion['perfil_professional']
        
    if experiencialaboral == "No":
        html_experiencialaboral = ""
    else:
        html_experiencialaboral = f"""<tr> <td> <div> <h3 style="line-height: 0; padding-top: 5px;">{experiencialaboral_puesto}</h3> </div> <div style="padding-bottom: 3px;"><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;" >{experiencialaboral_empresa}</span></div> <div style="display: flex;"> <span>{experiencialaboral_fecha} - {experiencialaboral_cese}</span> </div> <ul style="padding-bottom: 5px;"> <li> {experiencialaboral_funciones} </li> </ul> </td> </tr> <tr> <td> <div style = "border-top: dashed grey 1px; border-bottom: dashed grey 1px; padding-top: 10px; padding-bottom: 10px;"> <span>{experiencialaboral_logros}</span> </div> </td> </tr>"""
    
    if perfil_professional == notiene:
        html_perfil_profissional = ""
    else:
        html_perfil_profissional = f"""<table style="width: 800px;"> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">PERFIL PROFESIONAL</h3> </div> </td> </tr> <tr> <td style = "padding-top: 5px;"> <span>{perfil_professional}</span> </td> </tr> </table>"""

    source_html = f"""<!DOCTYPE html><html lang="pt-br"> <head> <title>Hoja de vida</title> <meta charset="utf-8"> <link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&display=swap" rel="stylesheet"> <link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet"> </head> <header> <div style="margin-top: 25px;"> <table style="width: 800px; padding: 0;"> <tr> <td style="width: 800px; padding: 0;"> <div style="padding-left: 30px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;"><span>{nombre}</span></div> <div style="padding-left: 30px; margin-top: 5px; font-weight: 600; font-size: 16pt; color: #30539B;"><span>{cargo}</span></div> <div style="padding-left: 30px; margin-top:5px; padding-bottom: 5px;"> <div> <span>{email}</span> </div> <div> <span>{telefono}</span> </div> </td> </tr> </table> </div> </header> <body style="font-size: 14px; font-family: 'Barlow Semi Condensed', sans-serif; color: #4e4e4e; font-weight: 500; margin: 0;" > <div style="margin-left: 30px; padding-top: 10px;"> <table style="width: 800px; "> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); width: 800px;"> <h3 style="line-height: 1; padding-top: 10px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EXPERIENCIA</h3> </div> </td> </tr> {html_experiencialaboral} </table> <table style="width: 800px;"> <tr> <td> <div style="border-bottom: solid 2px rgb(238, 199, 71); padding-top: 10px; width: 800px;"> <h3 style="line-height: 1; padding-top: 15px; font-weight: 600; font-size: 16pt; color: #000000; font-family: 'PT Serif', serif;">EDUCACIÓN</h3> </div> </td> </tr> <tr> <td style="width: 800px;"> <div> <h3 style="line-height: 0; padding-top: 5px">{nivelestudiomasalto} - {nivelestudiomasalto_titulo}</h3> </div> <div><span style = "font-weight: 600; color: #30539B; font-size: 18px; line-height: 50px;">{nivelestudiomasalto_institucion}</span></div> <div style="padding-top: 5px;"> {nivelestudiomasalto_formacion_bd} </div> </td> </tr> </table> {html_perfil_profissional} </div> <div style=" margin-left: 175px; padding-top: 30px;">Hoja de Vida generada por la Secretaría de Desarrollo Económico - Bogotá</div> </body></html>"""    

    # Create PDF and upload to storage
    file_name = create_and_upload_pdf(source_html, bucket_name)

    # Generate URL for the uploaded file
    url_file = generate_file_url(ambiente, file_name)

    # Create JSON response with the file URL
    jsonResponse = create_json_response(url_file)

    # Prepare email request information
    mail_request = {"email" : email, "nombre" : nombre, "file_name" : str(file_name), "bucket_name" : bucket_name}

    # Asynchronously send the generated PDF via email
    asyncio.run(send_mail(function_name, mail_request))

    # Convert session_id to an integer for database operations
    session_id_int = int(session_id)

    # Perform database operations based on the environment
    if ambiente != "portal":
        if ambiente == "HML":
            host_conexao = secretos["dgflow_mysql_host_HML"]
            senha_conexao = secretos["dgflow_mysql_password_HML"]
            print("It's in HML ",host_conexao)
        elif ambiente == "PROD":
            host_conexao = secretos["dgflow_mysql_host_PROD"]
            senha_conexao = secretos["dgflow_mysql_password_PROD"]
            print("It's in PROD ",host_conexao)

        # Try connecting to the database and performing updates/inserts
        try:
            with connect(
                host=host_conexao,
                user='chatbot',
                password=senha_conexao,
            ) as connection:
                # Update user complement information in the database
                db_update_complementos = f"UPDATE `agata-develop`.user_complemento SET celular = '{telefono}', cargo= '{cargo}' WHERE id_users='{session_id}'"  
                with connection.cursor() as cursor:
                    cursor.execute(db_update_complementos)
                    connection.commit()               
                
                # Check if the user has initiated a curriculum, if not, create one
                db_tem_curriculo = f"SELECT * FROM `agata-develop`.user_curriculo WHERE id_users=%s"
                with connection.cursor() as cursor:
                    cursor.execute(db_tem_curriculo, (session_id,))
                    result = cursor.fetchall()
                    if len(result)>0:
                        id_curriculo = str(result[0][0])
                        print("id curriculum:" + id_curriculo)
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
                        print("id curriculum:" +id_curriculo)
                id_curriculo = int(id_curriculo)

                # Insert highest education level information into the database
                with connection.cursor() as cursor:
                   db_insere_nivel_educativo = f"""INSERT INTO `agata-develop`.curriculo_nivel_educativo (id_user_curriculo, interessadoPractica, nivelEducativo, 
                       tituloObtenido, tituloHomologado, areaDesempeno,
                       nucleoConocimiento, Institucion, paisDelCurso, estadoDelCurso,
                       fechafinalizacion, idObservaciones) VALUES ({id_curriculo}, 0, '{nivelestudiomasalto}', '{nivelestudiomasalto_titulo}', '', '', '', '{nivelestudiomasalto_institucion}', '', '', '{nivelestudiomasalto_formacion_bd}', '')"""
                   cursor.execute(db_insere_nivel_educativo)
                   connection.commit()
                print("Educational level updated")
                
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
                    print("Work experience updated")

                connection.close()
        except Exception as e:
            print('Error: '+str(e))

    return jsonResponse


