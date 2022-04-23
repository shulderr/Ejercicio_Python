import pyodbc
import smtplib


def menu():
    print("--------- Menu ---------")
    print(" 1-> Agregar Nuevo Registro",
          "\n 2-> Eliminar Registro",
          "\n 3-> Ver Registros",
          "\n 4-> Enviar Correos",
          "\n 5-> Salir")
    opc = int(input("Digite Una Opcion: "))
    return opc


def conexion():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=GERALT;DATABASE=python;Trusted_Connection=yes;')
        print("Conexion Exitosa")
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
    print("Registro Agregado Con Exito")


def eliminar_registro():
    conx = conexion()
    del_cursor = conx.cursor()
    query = consulta_eliminar()
    del_cursor.execute(query)
    del_cursor.commit()
    del_cursor.close()
    conx.commit()
    print("Registro Eliminado Con Exito")


def ver_registros():
    query = "select * from Registro;"
    conx = conexion()
    ver_cursor = conx.cursor()
    ver_cursor.execute(query)
    registro = ver_cursor.fetchone()
    while registro:
        print(registro)
        registro = ver_cursor.fetchone()
    ver_cursor.close()
    conx.close()
    input()


def menu_filtro():
    print("----- Como Desea filtrar Para Enviar Los Correos -----")
    print(" 1-> Mayores De 30 Años",
          "\n 2-> Menores De 30 Años")
    opc = input("Digite Una Opcion")
    return opc


def datos_clientes():
    datos = []
    conx = conexion()
    query = "select Nombre,Edad,Correo from Registro;"
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
    if opc == 1:
        opc = 29
        for n in registros:
            datos = n
            if datos[1] <= opc:
                print(n)
                clientes.append(n)
    elif opc == 2:
        opc = 30
        for n in registros:
            datos = n
            if datos[1] >= opc:
                print(n)
                clientes.append(n)
    else:
        print("Se Ha digitado Una Opcion No Valida")
    return clientes


def envio_correo():
    edades = ["Menor", "Mayor"]
    variable = ""
    registros = filtro()
    for n in registros:
        cliente = n
        if cliente[1] <= 29:
            variable = edades[0]
        elif cliente[1] >= 30:
            variable = edades[1]
        nombre = cliente[0]
        edad = cliente[1]
        mail = cliente[2]
        mensaje = f"Hola {nombre}, Este correo te llega por que eres {variable} de 30 anios"
        asunto = "Prueba Correo"
        mensaje = 'Subject: {}\n\n{}'.format(asunto, mensaje)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('joungkingz@gmail.com', 'onlyswedish')
        server.sendmail('joungkingz@gmail.com', mail, mensaje)
        server.quit()
        print("Correo Enviado Exitosamente a: ",
              f"\n Nombre: {nombre}, Correo: {mail}, Edad: {edad}")
        input()


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
        print("Programa Finalizado")
        break
    elif opcion > 5:
        print("Opcion Ingresada No Valida")
