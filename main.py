import pyodbc
import smtplib
import time


def menu():
    print("\033[;33m" + "--------- Menu ---------" + "\033[0;m")
    print("\033[;33m" + "1->" + "\033[0;m" + " Agregar Nuevo Registro")
    print("\033[;33m" + "2->" + "\033[0;m" + " Eliminar Registro")
    print("\033[;33m" + "3->" + "\033[0;m" + " Ver Registros")
    print("\033[;33m" + "4->" + "\033[0;m" + " Enviar Correos")
    print("\033[;33m" + "5->" + "\033[0;m" + " Salir")
    opc = int(input("Digite Una Opcion: "))
    return opc


def conexion():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=GERALT;DATABASE=python;Trusted_Connection=yes;')
        print("\033[;32m" + "Conexion Exitosa" + "\033[0;m")
        return connection
    except Exception as ex:
        print(f"Error al Conectar Con La Base De Datos {ex}")


def consulta_agregar():
    nombre = input("Ingrese El Nombre: ")
    cedula = input(f"Ingrese La Cedula De {nombre}: ")
    correo = input(f"Ingrese El Correo De {nombre}: ")
    edad = input(f"Ingrese La Edad De {nombre}: ")
    ciudad = input(f"Ingrese La ciudad Donde Reside {nombre}: ")
    producto = input(f"Ingrese El Producto Comprado Por {nombre}: ")
    fecha_venta = input("Ingrese La Fecha De Venta Separada Por '/': ")
    query = "insert into Registro(Nombre, Cedula, Correo, Edad, Ciudad, Producto, Fecha_Venta) values ('" + nombre + "','" + cedula + "','" + correo + "','" + edad + "','" + ciudad + "','" + producto + "','" + fecha_venta + "') "
    return query


def consulta_eliminar():
    dato = input("Escriba El nombre De La persona Para eliminar el Registro: ")
    query = "delete from Registro where Nombre='" + dato + "'"
    return query


def agregar_registro():
    conect = conexion()
    agg_cursor = conect.cursor()
    query = consulta_agregar()
    agg_cursor.execute(query)
    agg_cursor.commit()
    agg_cursor.close()
    conect.close()
    print("\033[;32m" + "Registro Agregado Con Exito" + "\033[0;m")
    input("\033[;33m" + "Enter Para Continuar" + "\033[0;m") 


def eliminar_registro():
    conx = conexion()
    del_cursor = conx.cursor()
    query = consulta_eliminar()
    del_cursor.execute(query)
    del_cursor.commit()
    del_cursor.close()
    conx.commit()
    print("\033[;32m" + "Registro Eliminado Con Exito" + "\033[0;m")
    input("\033[;33m" + "Enter Para Continuar" + "\033[0;m") 


def ver_registros():
    clientes = []
    query = "select * from Registro;"
    conx = conexion()
    ver_cursor = conx.cursor()
    ver_cursor.execute(query)
    registro = ver_cursor.fetchone()
    while registro:
        lista = list(registro)
        clientes.append(lista)
        registro = ver_cursor.fetchone()
    ver_cursor.close()
    for n in clientes:
        print(n)
    conx.close()
    input("\033[;33m" + "Enter Para Continuar" + "\033[0;m")


def menu_filtro():
    opciones = []
    print("----- Como Desea filtrar Para Enviar Los Correos -----")
    print(" 1-> Mayores De 30 A??os",
          "\n 2-> Menores De 30 A??os",
          "\n 3-> Digitar Rango")
    opc = int(input("Digite Una Opcion: "))
    opciones.append(opc)
    if opc == 3:
        var1 = int(input("Digite El Primer Valor: "))
        opciones.append(var1)
        var2 = int(input("Digite El Segundo Valor: "))
        opciones.append(var2)
    return opciones


def datos_clientes():
    datos = []
    conx = conexion()
    query = "select Nombre,Edad,Correo,Ciudad from Registro;"
    ver_cursor = conx.cursor()
    ver_cursor.execute(query)
    registro = ver_cursor.fetchone()
    while registro:
        lista = list(registro)
        datos.append(lista)
        registro = ver_cursor.fetchone()
    conx.close()
    return datos


def filtro():
    clientes = []
    opc = menu_filtro()
    registros = datos_clientes()
    if opc[0] == 1:
        var = 30
        for n in registros:
            datos = n
            if datos[1] >= var:
                datos.append(30)
                datos.append(30)
                print(n)
                clientes.append(n)
    elif opc[0] == 2:
        var = 29
        for n in registros:
            datos = n
            if datos[1] <= var:
                datos.append(30)
                datos.append(30)
                print(n)
                clientes.append(n)
    elif opc[0] == 3:
        for n in registros:
            datos = n
            if datos[1] >= opc[1] and datos[1] <= opc[2]:
                datos.append(opc[1])
                datos.append(opc[2])
                print(n)
                clientes.append(n)
        if len(clientes) == 0:
            print("\033[;31m" + "No Hay Registros Dentro Del Rango Solicitado" + "\033[0;m")
            input("\033[;33m" + "Enter Para Continuar" + "\033[0;m")           
    else:
        print("\033[;31m" + "Se Ha digitado Una Opcion No Valida" + "\033[0;m")
        input("\033[;33m" + "Enter Para Continuar" + "\033[0;m") 
    return clientes


def envio_correo():
    edades = ["Menores De 30", "Mayores De 30"]
    registros = filtro()
    for n in registros:
        cliente = n
        rango1 = cliente[4]
        rango2 = cliente[5]
        if cliente[1] >= cliente[4] and cliente[1] <= cliente[5]:
            variable = f"Entre los {rango1} y los {rango2}"
        elif cliente[1] <= 29:
            variable = edades[0]
        elif cliente[1] >= 30:
            variable = edades[1]
        fecha = str(time.strftime("%d/%m/%Y"))
        nombre = cliente[0]
        edad = cliente[1]
        mail = cliente[2]
        ciudad = cliente[3]
        mensaje = f"{ciudad}, {fecha}. \n\n Hola {nombre}. \n\n Cordial Saludo. \n\n Este Correo Te llega Por Que Estas En El Rango De Edades {variable}"
        asunto = "Prueba Correo"
        mensaje = 'Subject: {}\n\n{}'.format(asunto, mensaje)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('joungkingz@gmail.com', 'onlyswedish')
        server.sendmail('joungkingz@gmail.com', mail, mensaje)
        server.quit()
        print("Correo Enviado Exitosamente a: ",
              f"\n Nombre: {nombre}, Correo: {mail}, Edad: {edad}")
    input("\033[;33m" + "Enter Para Continuar" + "\033[0;m")


def bucle():
    while True:
        opcion = menu()
        if opcion == 1:
            agregar_registro()
        elif opcion == 2:
            eliminar_registro()
        elif opcion == 3:
            ver_registros()
        elif opcion == 4:
            envio_correo()
        elif opcion == 5:
            print("\033[;32m" + "Programa Finalizado" + "\033[0;m")
            break
        elif opcion > 5 or opcion < 1:
            print("\033[;31m" + "Opcion Ingresada No Valida" + "\033[0;m")


bucle()