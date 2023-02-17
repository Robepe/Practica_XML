import re
from datetime import datetime
import os.path
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

fichero = "./tienda.xml" # ruta fichero xml
idDisco = 1 # variables globales para la asignacion de ID
idVenta = 1

"""
Metodo que al comenzar el programa, comprueba la existencia del fichero
En caso de no existir, lo crea con la estructura inicial
"""
def inicializar():
	if (not os.path.exists(fichero)):
		root = ET.Element('tienda')
		discos = ET.SubElement(root, 'discos')
		ventas = ET.SubElement(root, 'ventas')
		guardarXml(root, 'tienda.xml')
		print("Fichero creado con exito")


# Metodo que toma un elemento "crudo" y lo devuelve con un formato estilizado
def prettify(elem):
	from xml.dom import minidom #importamos el modulo minidom

	rough_string = ET.tostring(elem, 'utf-8') 		# Utilizamos la funcion tostring() de ElementTree para pasar de'elem' a 'String
	reparsed = minidom.parseString(rough_string) 	# minidom parsea el String
	return '\n'.join([line for line in reparsed.toprettyxml(indent='\t').split('\n') if line.strip()])		#indentamos con 'toprettyxml', filtramos las lineas vacias con 'split' y unimos las lineas restantes con 'join'
	

# Metodo que recoge por parametro una raiz y un fichero en el que almacenarla
def guardarXml(arbol,fichero):
	salida = prettify(arbol)	# aplicamos el estilo
	file = open(fichero,"w")	# abrimos y sobreescribimos el fichero
	file.write(salida)
	file.close()				# escribimos y cerramos el fichero


# Metodo que lee de un fichero y extrae el arbol o raiz en el escrito
def leerXml(fichero):
	arbol = ET.parse(fichero)	# parseo a 'elem'
	raiz = arbol.getroot()		
	return raiz					# ubicamos y devolvemos la raiz de elementos

# Metodo que recoge un String y valida tanto la longitud como la presencia de caracteres no deseados
def validarString(string):
	y = string.strip()
	for intento in range(5):
		if ((len(y) < 1) or (len(y) > 40)):
			print("\nEntrada invalida: minimo un caracter, maximo 20 caracteres\nPruebe de nuevo:")
			y = str(input()).strip()
		else:
			return y

	print("-" * 20, "Operacion Cancelada", "-" * 20)
	return False

# Método que recoge un String, para eliminar caracteres en blanco, y lo convierte a un Integer (POR DEFECTO SI NO SE ESPECIFICA, ES SIN DECIMALES)
def validarInteger(x, decimales = False):
	if not decimales:
		for intento in range(5):
			y = x.strip()	# eliminamos los posibles espacios vacios al inicio y final
			try:
				z = int(y)	# tratamos de castear el valor proporcionado a la variable 'z'
				return z	# de ser posible, se retorna la variable 'z'
			except ValueError:
				print("\nEntrada no valida: introduzca exclusivamente numeros entre 0 y 9:\n")
				x = input()	# de no serlo, volvemos a pedir una cifra
		print("\nOperacion cancelada\n")
	else:
		for intento in range(5):
			y = x.strip()
			try:
				z = float(y)
				return z
			except ValueError:
				print("\nEntrada no valida: introduzca exclusivamente numeros entre 0 y 9: (en caso de necesitar decimales, recuerde utilizar '.')\n")
				x = input()
		print("\nOperacion cancelada\n")

# Metodo que recoge una cadena y comprueba que contenga las caracteristicas de un DNI
def validarDNI(dni):
	contador = 0
	pat = re.compile("[0-9]{8}[A-Z]")	# Patron establecido a cumplirse (8 numeros de 0 a 9 y una sola letra mayuscula de la A a la Z)
	mat = pat.match(dni)				# variable que comprueba si hay "Match" con el patron anteriormente establecido

	while(not mat): # En caso de error:
		print("\nFormato de DNI no valido. Pruebe con 8 numeros y una letra")
		newStr = str(input())	# Pedimos otra cadena para comprobarla nuevamente
		dni = newStr.strip()	# eliminamos los posibles campos vacios
		mat = pat.match(dni)	# Comprobamos de nuevo
		contador += 1
		if (contador == 5):		# en caso de fallar 5 veces, cancelamos la operacion
			return

	return dni
"""
Metodo que comprueba que, dada una cantidad demandada, y un stock existente, el stock nunca sea menor que 0
Una vez validada, retornamos la cantidad
"""
def validarStock(cantidad, stock):
	contador = 0

	while True:
		if (cantidad > stock) and (cantidad > 0): 				# Si la cantidad demandada es mayor a la existente
			print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
			cantidad = validarInteger(str(input()), False)		# Pedimos una nueva cantidad
			contador += 1
			if (contador == 5): 								# en caso de fallar 5 veces, cancelamos la operacion
				print("-" * 20, "Operacion Cancelada", "-" * 20)
				return 0
		else:
			return cantidad


# Metodo que lee el fichero XML y proporciona un ID a cada Disco
def genIdDisco():
	raiz = leerXml(fichero) # Obtenemos la raiz
	global idDisco 			#modificamos la variable global

	if len(raiz[0]) > 0:	# si existen discos, se recoge el valor del ultimo id y se le suma 1
		idDisco = int(raiz[0][-1].attrib['id']) + 1

# Metodo que lee el fichero XML y proporciona un ID a cada Venta
def genIdVenta():
	raiz = leerXml(fichero)
	global idVenta

	if len(raiz[1]) > 0:
		idVenta = int(raiz[1][-1].attrib['id']) + 1

# Metodo que devuelve la Fecha y la Hora local
def setFecha():
	now = datetime.now() 				#almacenamos una variable de tipo 'datetime'

	fecha = now.strftime("%d/%m/%Y")	#proporcionamos un formato a la fecha
	hora = now.strftime("%H:%M:%S")		#proporcionamos un formato a la hora

	return fecha, hora					# retornamos la fecha y la hora formateadas

# Metodo de tipo 'bool', que comprueba si existen hijos en nodo/raiz proporcionado por parametro
def comprobarNodos(raiz):
	check = raiz.findall('./*') 	# busca todo tipo de etiquetas que partan del nodo proporcionado y lo almacena en 'check'

	if check:
		return True
	else:
		return False

# Metodo de tipo 'bool' destinado a comprobar una seleccion de tipo (S/N)
def confirmarOperacion():
	while True:
		opcion = (str(input().strip().lower()))
		if (opcion == "s"):				# de ser 's' o 'S', retornamos True
			return True
		elif (opcion == "n"):			# de ser 'n' o 'N', retornamos False
			return False
		else:
			print("\nOperacion no reconocida")	# de no estar contemplada la respuesta, reiniciamos el bucle
			
"""			
Metodo de tipo 'bool' que dado un diccionario por parametro
compara si los valores 'Titulo', 'Autor' y 'Ano' ya existen en el fichero XML
"""
def comprobarRedundancia(diccionario = {}):
	raiz = leerXml(fichero)								# Obtenemos la raiz del fichero xml
	subraiz = raiz[0]									# Dividimos esta en la parte interesada (queremos operar con la seccion Discos)
	check = comprobarNodos(subraiz)						# comprobamos que existan hijos en Discos
	infoDiscos = {'Titulo':[], 'Autor':[], 'Anio':[]}	# Declaramos un diccionario en el que leer y almacenar todos los titulos, autores, y anos

	if check: 											# De existir hijos:
		for disco in subraiz:							# Bucle for para navegar por todos los discos existentes
			titulo = disco.find("titulo")				# Almacenamos los valores de 'Titulo', 'Autor', 'Ano'
			autor = disco.find("autor")
			anio = disco.find("anio")

			infoDiscos['Titulo'].append(titulo.text)	#Introducimos dichos valores en el diccionario
			infoDiscos['Autor'].append(autor.text)
			infoDiscos['Anio'].append(anio.text)

			if((diccionario['Titulo'] in infoDiscos['Titulo'])		# En caso de coincidir un nuevo Disco en los 3 campos
			 and (diccionario['Autor'] in infoDiscos['Autor'])		# con uno ya existente, retornamos False 
			  and (diccionario['Anio'] in infoDiscos['Anio'])):
				return False
			else:													# Mientras coincidan 2 o menos, es valido y retornamos True
				return True
			
	else:		# Si no existen hijos, la comprobacion es innecesaria y retornamos True
		return True


# Metodo para crear un elemento Disco, dentro de Discos, con todos los datos requeridos
def anadirDisco():
	raiz = leerXml(fichero)								# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]									# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	fecha = setFecha()[0]								# Recogemos el primer valor retornado por el metodo 'setFecha' para utilizarlo a la hora de comparar el ano
	anioActual = int(fecha.split("/")[-1])				# Dividimos el ano '(dd/mm/yy)' por '/' y seleccionamos el ultimo valor, obteniendo asi 'yy'
	
	terminar = False
	while not terminar:									# Bucle  para anadir Discos hasta que el usuario desee
		genIdDisco()									# llamamos al metodo 'genIdDisco' para asignar los valores de todos los IDdisco
		disco = ET.SubElement(subraiz,"disco")			# Establecemos el SubElemento 'disco', hijo de 'discos'
		disco.set('id', str(idDisco))					# Establecemos el ID de 'disco'
		titulo = ET.SubElement(disco,"titulo")			# Establecemos el SubElemento 'titulo', hijo de 'disco'
		autor = ET.SubElement(disco,"autor")			# ...
		formato = ET.SubElement(disco,"formatos")
		cd = ET.SubElement(formato,"CD")				# Establecemos el SubElemento 'CD', hijo de 'formato'
		dvd = ET.SubElement(formato,"DVD")				# ...
		vinilo = ET.SubElement(formato,"Vinilo")
		cassette = ET.SubElement(formato,"Cassette")
		anio = ET.SubElement(disco,"anio")
		genero = ET.SubElement(disco, "genero")
		precio = ET.SubElement(disco, "precio")
			
		print("Introduce el titulo: ")					# Rellenamos los campos de las etiquetas creadas
		titulo.text = validarString(str(input()))		# Validamos mediante el uso de 'validarString' (comprobamos por espacios vacios)

		print("Introduce el autor: ")
		autor.text = validarString(str(input()))

		flag = False									# Bucle para repetir la repetir la pregunta/respuesta en caso de ser incorrecta
		contador = 0									# En caso de ser 's', procedemos a rellenar el Stock, de ser 'n', se asigna de manera automatica el valor de 0 a todo el stock
		while(not flag):
			print("¿Desea anadir stock en este momento? (S/N)")
			opt = validarString(str(input()))

			if (opt.lower() == 's'):
				print("Introduzca la cantidad de discos disponibles en formato CD:")
				cd.text = str(validarInteger(str(input()), False))								#Validamos mediante 'validarInteger' en su modalidad sin decimales
				print("Introduzca la cantidad de discos disponibles en formato DVD:")
				dvd.text = str(validarInteger(str(input()), False))
				print("Introduzca la cantidad de discos disponibles en formato Vinilo:")
				vinilo.text = str(validarInteger(str(input()), False))
				print("Introduzca la cantidad de discos disponibles en formato Cassette:")
				cassette.text = str(validarInteger(str(input()), False))
				flag = True																		# declaramos el final del bucle
			elif (opt.lower() == 'n'):
				cd.text = '0'
				dvd.text = '0'
				vinilo.text = '0'
				cassette.text = '0'
				flag = True
			else:
				print("\nOperacion no reconocida\n")
				contador += 1
				if (contador == 5):																# en caso de fallar 5 veces, cancelamos la operacion
					print("\nOperacion cancelada\n")
					break

		flag = False			# reiniciamos el valor de flag para reutilizarlo
		contador = 0
		while (not flag):		# bucle para validar el Ano del disco
			print("Introduce el anio: ")
			anio.text = str(validarInteger(str(input()), False))		# modalidad sin decimales

			if (int(anio.text) < 1900 or int(anio.text) > anioActual):	# si el ano no esta entre '1900' y el ano actual, no es valido'
				print("\nAnio introducido no valido, pruebe con un ano entre 1900 y el actual\n")
				contador += 1
				if (contador == 5): 		# en caso de fallar 5 veces, cancelamos la operacion
					print("\nOperacion cancelada\n")
					break
			else:
				flag = True					# finalizamos el bucle

		print("Introduce el genero: ")
		genero.text = validarString(str(input()))

		print("Introduce el precio: ")
		precio.text = str(validarInteger(str(input()), True))		# Para el precio, utilizamos 'validarInteger' en su modalidad con decimales

		infoNewDisco = {'Titulo': titulo.text, 'Autor': autor.text, 'Anio': anio.text}		# declaramos un diccionario en el que almacenamos el Titulo, Autor y ano del nuevo disco

		validacion = comprobarRedundancia(infoNewDisco)										# Validamos que no exista ya un disco con los valores introducidos en el alta,
		if validacion:																		# y pasamos el diccionario recien creado al metodo 'comprobarRedundancia'. Si esta nos
			print("\n¿Estas seguro de anadir el disco? (S/N) : \n")
			confirmacion = confirmarOperacion()												# Si el disco no es repetido, pedimos confirmacion al usuario para grabar el disco
			if confirmacion:
				guardarXml(raiz, fichero)													# de ser afirmativa la respuesta, grabamos todos los elementos al fichero
				print("\nDisco anadido con exito\n¿Desea anadir otro Disco? (S/N)")
				repeticion = confirmarOperacion()											# preguntamos si quiere repetir el proceso del alta
				if not repeticion:															# de ser 'n', salimos de la funcion, en caso contrario, 'Terminar' sigue siendo 'False'
					print("Alta finalizada")
					return

			else:
				print("\nOperacion cancelada")												# En caso de negativa a la hora de guardar el disco, terminamos la funcion
				return
		else:
			print("\nDisco ya existente\n")													# Si el disco introducido ya existe, salimos de la funcion
			return
				
# Metodo mediante el cual eliminamos un 'disco' y sus subelementos del fichero xml
def eliminarDisco():
	raiz = leerXml(fichero)					# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]						# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)			# Comprobamos que existan hijos de 'discos'
	encontrado = False						# variable de tipo 'bool' para controlar si el disco fue encontrado o no

	if check:		#De existir algun disco (hijos de 'discos'):
		print("Introduzca el ID del disco a eliminar: ")
		opt = validarString(str(input()))									# Pedimos un 'id'

		for disco in subraiz:												# Para cada 'disco' en 'discos'
			if disco.get('id') == opt:										# comparamos el id introducido con los id de los discos
				print("\n¿Estas seguro de eliminar el disco? (S/N) :\n")
				confirmacion = confirmarOperacion()							# si hay una coincidencia, se pide confirmacion
				if confirmacion:
					subraiz.remove(disco)									# de confirmarse, eliminamos el 'disco'
					encontrado = True
					guardarXml(raiz, fichero)								# guardamos el arbol xml actualizado
					print("\nDisco eliminado con exito\n")
				else:
					print("\nOperacion cancelada")							# en caso de no confirmar, se aborta la operacion
					return

		if (not encontrado):												# en caso de no encontrarse ninguna coincidencia
				print("\nDisco no encontrado")

	else:
		print("\nActualmente no existen discos almacenados")				# si no existen discos, se notifica

# Metodo para modificar los campos de discos ya existentes
def modificarDisco():
	raiz = leerXml(fichero)				# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]					# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)		# Comprobamos que existan hijos de 'discos'
	fecha = setFecha()[0]				# Recogemos el primer valor retornado por el metodo 'setFecha' para utilizarlo a la hora de comparar el ano
	anioActual = int(fecha.split("/")[-1])
	flag = False
	encontrado = False

	if check:			#De existir algun disco (hijos de 'discos'):
		print("Introduzca el ID del disco a modificar: ")
		opt = validarString(str(input()))								# Pedimos un 'id'

		for disco in subraiz:											# Para cada 'disco' en 'discos'
			if disco.get('id') == opt:									# comparamos el id introducido con los id de los discos
				encontrado = True

				titulo = disco.find("titulo")							# identificamos los elementos presentes en 'disco'
				autor = disco.find("autor")
				formato = disco.find("formato")
				anio = disco.find("anio")
				genero = disco.find("genero")
				precio = disco.find("precio")
				
				print("\nSeleccione el apartado a modificar: \n\n1.-\tTitulo\n2.-\tAutor\n3.-\tAnio\n4.-\tGenero\n5.-\tPrecio\n6.-\tModificar todo\n\n0.-\tCancelar")
				opt = validarString(str(input()))						# Seleccionamos una opcion

				while (not flag):										# Bucle para poder repetir operaciones
					try:
						if (opt == '1'):								# opcion 1: 'Titulo'
							print("Introduce el nuevo titulo: ")
							titulo = disco.find('titulo')				# buscamos la etiqueta 'titulo'
							titulo.text = validarString(str(input()))	# validamos y damos un nuevo valor a 'titulo

							print("\n¿Confirmar operacion?(S/N)\n")
							confirmacion = confirmarOperacion()
							if confirmacion:							# al confirmar guardamos, al cancelar, abortamos la operacion
								flag = True
								guardarXml(raiz, fichero)
								print("\nDisco modificado con exito\n")
							else:
								print("\nOperacion cancelada\n")
								return

						elif (opt == '2'):								#opcion 2: 'Autor'
							print("Introduce el nuevo autor: ")
							autor = disco.find('autor')
							autor.text = validarString(str(input()))

							print("\n¿Confirmar operacion?(S/N)\n")
							confirmacion = confirmarOperacion()
							if confirmacion:
								flag = True
								guardarXml(raiz, fichero)
								print("\nDisco modificado con exito\n")
							else:
								print("\nOperacion cancelada\n")
								return
									
						elif (opt == '3'):								# opcion 3: 'anio'
							flag = False
							contador = 0
							while (not flag):							# bucle para validar el Ano del disco
								print("Introduce el nuevo anio: ")
								anio.text = str(validarInteger(str(input()), False))		# modalidad sin decimales

								if (int(anio.text) < 1900 or int(anio.text) > anioActual):	# si el ano no esta entre '1900' y el ano actual, no es valido'
									print("\nAnio introducido no valido, pruebe con un ano entre 1900 y el actual\n")
									contador += 1
									if (contador == 5): 				# en caso de fallar 5 veces, cancelamos la operacion
										print("\nOperacion cancelada\n")
										break
								else:
									print("\n¿Confirmar operacion?(S/N)\n")
									confirmacion = confirmarOperacion()
									if confirmacion:					# al confirmar guardamos, al cancelar, abortamos la operacion
										guardarXml(raiz, fichero)
										flag = True
										print("\nDisco modificado con exito\n")
									else:
										print("\nOperacion cancelada\n")
										return
									
						elif (opt == '4'):							# opcion 4: genero (igual que 1 y 2)
							print("Introduce el nuevo genero: ")
							genero = disco.find('genero')
							genero.text = validarString(str(input()))

							print("\n¿Confirmar operacion?\n")
							confirmacion = confirmarOperacion()
							if confirmacion:
								flag = True
								guardarXml(raiz, fichero)
								print("\nDisco modificado con exito\n")
							else:
								print("\nOperacion cancelada\n")
								flag = True
								return
									
						elif (opt == '5'):							# opcion 5: precio (igual que 1, 2 y 4)
							print("Introduce el nuevo precio: ")
							precio = disco.find('precio')
							precio.text = str(validarInteger(str(input()), True))		# modalidad con decimales

							print("\n¿Confirmar operacion?\n")
							confirmacion = confirmarOperacion()
							if confirmacion:
								flag = True
								guardarXml(raiz, fichero)
								print("\nDisco modificado con exito\n")
							else:
								print("\nOperacion cancelada\n")
								flag = True
								return
									
						elif (opt == '6'):							#opcion 6: todos (igual que las opciones anteriores, con una unica confirmacion al final)
							print("Introduce el nuevo titulo: ")
							titulo = disco.find('titulo')
							titulo.text = validarString(str(input()))

							print("Introduce el nuevo autor: ")
							autor = disco.find('autor')
							autor.text = validarString(str(input()))

							flag = False
							contador = 0
							while (not flag):
								print("Introduce el nuevo anio: ")
								anio.text = str(validarInteger(str(input()), False))

								if (int(anio.text) < 1900 or int(anio.text) > anioActual):
									print("\nAnio introducido no valido, pruebe con un ano entre 1900 y el actual\n")
									contador += 1
									if (contador == 5):
										print("\nOperacion cancelada\n")
										break
								else:
									flag = True

							print("Introduce el nuevo genero: ")
							genero = disco.find('genero')
							genero.text = validarString(str(input()))

							print("Introduce el nuevo precio: ")
							precio = disco.find('precio')
							precio.text = str(validarInteger(str(input()), True))
							
							print("\n¿Confirmar operacion? (S/N)\n")
							confirmacion = confirmarOperacion()
							if confirmacion:							# Al confirmar guardamos todos los cambios en el fichero
								flag = True
								guardarXml(raiz, fichero)
								print("\nDisco modificado con exito\n")
							else:
								print("\nOperacion cancelada\n")		# En caso de no hacerlo, se aborta la operacion
								flag = True
								return
									
						elif (opt == '0'):								# Al seleccionar el campo a modificar, 0 cancela la operacion
							break
					except ValueError:									# en caso de introducir un tipo de dato diferente al esperado
						print("Entrada no valida")

		if (not encontrado):											# en caso de seleccionar un disco inexistente
			print("\nDisco no encontrado")

# Metodo que busca y muestra por pantalla un 'disco' con todos sus atributos y elementos
def buscarDisco():
	raiz = leerXml(fichero)					# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]						# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)			# Comprobamos que existan hijos de 'discos'
	encontrado = False

	if check:		# En caso de existir discos:
		print("Introduzca el ID del disco a buscar: ")
		opt = validarString(str(input()))				# Buscamos discos por 'id'

		for disco in subraiz:							# Para cada disco en discos
			if disco.get('id') == opt:					# Si existe una coincidencia
				encontrado = True
				print("\nDisco",disco.get('id'),":")	
				for data in disco:						# para cada etiqueta en disco
					if data.tag == 'formatos':			# si una etiqueta se llama 'formatos', imprimira cada 'formato' en 'formatos'
						print("\t",data.tag, ": ")
						for formato in data:
							print("\t\t",formato.tag, ": ", formato.text)
					else:
						print("\t",data.tag, ": ", data.text) # si no se llama 'formatos' imprime de manera estandar (nombre: contenido)
						

		if (not encontrado):
			print("\nDisco no encontrado")
			
	else:
		print("\nActualmente no existen discos almacenados")

# Metodo para mostrar por pantalla todos los discos almacenados
def mostrarDiscos():
	raiz = leerXml(fichero)				# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]					# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)		# Comprobamos que existan hijos de 'discos'

	if check:														# Si existen hijos:
		for disco in subraiz:										# Para cada 'Disco' en 'Discos'
			print("\nDisco",disco.get('id'),":")
			for data in disco:										# Para cada subelemento de disco
				if data.tag == 'formatos':							# si este subelemento se llama 'formatos'
					print("\t",data.tag, ": ")
					for formato in data:							# imprimimos cada 'formato' en 'formatos'
						print("\t\t",formato.tag, ": ", formato.text)
				else:
					print("\t",data.tag, ": ", data.text)			# si no se llama 'formatos' imprime de manera estandar (nombre: contenido)
	else:
		print("\nActualmente no existen discos almacenados")

#Metodo que permite modificar el stock de un Disco determinado
def restockDiscos():
	raiz = leerXml(fichero)					# Obtenemos la raiz del fichero XML (tienda)
	subraiz = raiz[0]						# Acotamos el "area de accion" en Discos, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)			# Comprobamos que existan hijos de 'discos'
	encontrado = False
	ok = False

	if check:			# Si existen discos:
		print("Introduzca el ID del disco a modificar su Stock: ")
		opt = validarString(str(input()))							# Seleccionamos un disco mediante su id

		for disco in subraiz:										# Para cada disco en discos
			if disco.get('id') == opt:								# si coincide el id
				encontrado = True
				print("\nStock actual: \n")							# mostramos el stock actual
				print("\tCD: ",disco[2][0].text)
				print("\tDVD: ",disco[2][1].text)
				print("\tVinilo: ",disco[2][2].text)
				print("\tCassette: ",disco[2][3].text)

				print("\n¿Desea modificar el Stock de este disco? (S/N)\n")
				confirmacion = confirmarOperacion()					# Pedimos confirmacion
				if confirmacion:									# si la respuesta es afirmativa
					flag = False
					while (not flag):								# bucle para anadir varios tipos de stock
						print("\nSeleccione el formato que desea modificar: \n\n1.-\tCD\n2.-\tDVD\n3.-\tVinilos\n4.-\tCassettes\n5.-\tTodo\n\n0.-\tSalir")

						
					opt = validarInteger(str(input()), False)		# Seleccionamos una opcion por teclado
					if (opt == 1):									# OPCION 1: CD
						contador = 0
						ok = False
						while(not ok):								# bucle para no retornar al menu en caso de introducir cantidades no permitida
							print("\nIntroduzca el numero de CD a anadir/restar: \n")
							cantidad = validarInteger(str(input()), False)		# Validamos la entrada por teclado
							newCantidad = (int(disco[2][0].text) + cantidad)	# Realizamos la operacion aritmetica
							if (newCantidad > 0):								# comprobamos si el stock es 0 o mayor
								print("\nNuevo Stock CD: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
								confirmacion = confirmarOperacion()				# En caso de ser correcto, pedimos la confirmacion del usuario
								if confirmacion:
									disco[2][0].text = str(newCantidad)			# Actualizamos el valor de la etiqueta
									guardarXml(raiz, fichero)					# Grabamos los cambios en el fichero
									print("\nStock modificado correctamente\n")
									ok = True
								else:
									print("\nOperacion de restock cancelada\n")
									ok = True
							else:												# Si el stock termina siendo negativo, se notifica el error, se aumenta el contador y volvemos a iniciar el bucle
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:								# Si fallamos 5 veces, se cancela la operacion
									print("\nOperacion cancelada\n")
									return

					elif (opt == 2):											# OPCION 2: DVD (Conservamos la estructura de la opcion anterior)
						contador = 0
						ok = False
						while(not ok):
							print("\nIntroduzca el numero de DVD a anadir/restar: \n")
							cantidad = validarInteger(str(input()), False)
							newCantidad = (int(disco[2][1].text) + cantidad)
							if (newCantidad > 0):
								print("\nNuevo Stock DVD: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
								confirmacion = confirmarOperacion()
								if confirmacion:
									disco[2][1].text = str(newCantidad)
									guardarXml(raiz, fichero)
									print("\nStock modificado correctamente\n")
									ok = True
									flag = True
								else:
									print("\nOperacion de restock cancelada\n")
									ok = True
									flag = True
							else:
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return

					elif (opt == 3):											# OPCION 3: Vinilos (Conservamos la estructura de la opcion anterior)
						contador = 0
						ok = False
						while(not ok):
							print("\nIntroduzca el numero de Vinilos a anadir/restar: \n")
							cantidad = validarInteger(str(input()), False)
							newCantidad = (int(disco[2][2].text) + cantidad)
							if (newCantidad > 0):
								print("\nNuevo Stock Vinilos: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
								confirmacion = confirmarOperacion()
								if confirmacion:
									disco[2][2].text = str(newCantidad)
									guardarXml(raiz, fichero)
									print("\nStock modificado correctamente\n")
									ok = True
									flag = True
								else:
									print("\nOperacion de restock cancelada\n")
									ok = True
									flag = True
							else:
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return

					elif (opt == 4):											# OPCION 4: Cassettes (Conservamos la estructura de la opcion anterior)
						contador = 0
						ok = False
						while(not ok):
							print("\nIntroduzca el numero de Cassettes a anadir/restar: \n")
							cantidad = validarInteger(str(input()), False)
							newCantidad = (int(disco[2][3].text) + cantidad)
							if (newCantidad > 0):
								print("\nNuevo Stock Cassettes: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
								confirmacion = confirmarOperacion()
								if confirmacion:
									disco[2][3].text = str(newCantidad)
									guardarXml(raiz, fichero)
									print("\nStock modificado correctamente\n")
									ok = True
									flag = True
								else:
									print("\nOperacion de restock cancelada\n")
									ok = True
									flag = True
							else:
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return

					elif (opt == 5):											# OPCION 5: Todos
						contador = 0
						ok = False
						while(not ok):											# bucle para no retornar al menu en caso de introducir cantidades no permitida
							print("\nIntroduzca el numero de CD a anadir/restar: \n")
							cantidadCD = validarInteger(str(input()), False)		# Validamos la cantidad demandada
							newCantidadCD = (int(disco[2][0].text) + cantidadCD)	# Actualizamos el stock, permitiendo valores tanto positivos como negativos
							if (newCantidadCD < 0):									# Si el stock termina siendo menor que 0:
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:									# En caso de introducir una cantidad no permitida, contador se autoincrementa en 1,
									print("\nOperacion cancelada\n")				# al llegar a 5, se cancela la operacion
									return
							else:
								ok = True											# Si la cantidad es correcta, salimos del bucle dedicado a 'CD' y pasamos al siguiente

						ok = False
						contador = 0
						while(not ok):													# Utilizamos la misma estructura que en el bucle anterior, esta vez para determinar
							print("\nIntroduzca el numero de DVD a anadir/restar: \n")	# la cantidad de DVD anadida/restada
							cantidadDVD = validarInteger(str(input()), False)
							newCantidadDVD = (int(disco[2][1].text) + cantidadDVD)
							if (newCantidadDVD < 0):
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return
							else:
								ok = True

						ok = False
						contador = 0
						while(not ok):														# Utilizamos la misma estructura que en el bucle anterior, esta vez para determinar
							print("\nIntroduzca el numero de Vinilos a anadir/restar: \n")	# la cantidad de Vinilos anadida/restada
							cantidadVin = validarInteger(str(input()), False)
							newCantidadVin = (int(disco[2][2].text) + cantidadVin)
							if (newCantidadVin < 0):
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return
							else:
								ok = True

						ok = False
						contador = 0
						while(not ok):															# Utilizamos la misma estructura que en el bucle anterior, esta vez para determinar
							print("\nIntroduzca el numero de Cassettes a anadir/restar: \n")	# la cantidad de Cassettes anadida/restada
							cantidadCas = validarInteger(str(input()), False)
							newCantidadCas = (int(disco[2][3].text) + cantidadCas)
							if (newCantidadCas < 0):
								print("\nError: El Stock nunca puede ser negativo, revise la cantidad demandada/modificada y pruebe de nuevo: \n")
								contador += 1
								if contador == 5:
									print("\nOperacion cancelada\n")
									return
							else:
								ok = True

						# Imprimimos el resultado de todos los formatos tras la operacion
						print("\nNuevo Stock: \n\tCD: ",newCantidadCD,"\n\tDVD: ",newCantidadDVD,"\n\tVinilo: ",newCantidadVin,"\n\tCassette: ",newCantidadCas,"\n¿Confirmar cambios? (S/N)\n")
						confirmacion = confirmarOperacion()				# Pedimos confirmacion al usuario
						if confirmacion:								# En caso de ser afirmativo, sobreescribimos las etiquetas correspondientes
							disco[2][0].text = str(newCantidadCD)
							disco[2][1].text = str(newCantidadDVD)
							disco[2][2].text = str(newCantidadVin)
							disco[2][3].text = str(newCantidadCas)
							guardarXml(raiz, fichero)					# Sobreescribimos el fichero con los nuevos valores
							print("\nNuevo stock anadido correctamente\n")
							flag = True
						else:
							print("\nOperacion de restock cancelada\n")
							flag = True									# En caso de no confirmar la operacion, salimos del bucle sin guardar los cambios

					elif (opt == 0):
						flag = True										# OPCION 0: Salir
					else:
						print("\nEntrada no valida\n")
				else:
					print("\nOperacion cancelada")
					return

		if (not encontrado):
			print("\nDisco no encontrado")								# En caso de no existir el disco, lo notificamos
			
	else:
		print("\nActualmente no existen discos almacenados")


def nuevaVenta():
	raiz = leerXml(fichero)								# Obtenemos la raiz del fichero XML (tienda)
	subraizDiscos = raiz[0]								# Dividimos la raiz en 'Discos'
	subraizVentas = raiz[1]								# y en 'Ventas'
	encontrado = False
	check = comprobarNodos(subraizDiscos)				# Comprobamos la existencia de hijos(en este caso, de 'Discos')
	fecha_hora = setFecha()								# almacenamos la fecha y la hora en la variable 'fecha_hora'

	genIdVenta()										# Generamos el ID de la venta
	venta = ET.SubElement(subraizVentas,"venta")		# Establecemos el SubElemento 'Venta', hijo de 'Ventas'
	venta.set('id', str(idVenta))						# Establecemos el ID de 'venta' con el valor de la variable global modificada
	articulos = ET.SubElement(venta,"articulos")		
	dni = ET.SubElement(venta,"dni")					# Establecemos el SubElemento 'dni', hijo de 'venta'
	fecha = ET.SubElement(venta,"fecha")				# Establecemos el SubElemento 'fecha', hijo de 'venta'
	fecha.text = fecha_hora[0]							# Establecemos el valor del elemento 'Fecha'
	hora = ET.SubElement(venta,"hora")					# Establecemos el SubElemento 'hora', hijo de 'venta'
	hora.text = fecha_hora[1]							# Establecemos el valor del elemento 'Hora'
	importe = ET.SubElement(venta,"importe")			# Establecemos el SubElemento 'importe', hijo de 'venta'

	if check:											# En caso de existir discos, proseguimos con la venta
		terminar = False								# Bucle con la finalidad de proporcionarnos la opcion de seleccionar otro
		while (not terminar):							# disco para anadir a una misma venta
			mostrarDiscos()								# mostramos todos los discos existentes									
			print("\nSeleccione el ID del Disco que desea vender: (0 para cancelar)\n")
			opt = validarString(str(input()))			# Introducimos y validamos el ID
			if (int(opt) == 0):							# 0 para retroceder
				print("\nVenta Cancelada\n")
				return

			for disco in subraizDiscos:						#Para 'disco' en 'discos':
				if disco.get('id') == opt:					# si el 'id' de algun disco coincide con el input del usuario
					encontrado = True						
					print("\nStock actual: \n")				#Mostramos el Stock actual de dicho disco
					print("\tCD: ",disco[2][0].text)
					print("\tDVD: ",disco[2][1].text)
					print("\tVinilo: ",disco[2][2].text)
					print("\tCassette: ",disco[2][3].text)

					flag = False
					while (not flag):						# Bucle para permitir seleccionar varios Stocks en una misma venta 
						
						articulo = ET.SubElement(articulos, "articulo")			# Creamos un elemento 'articulo', hijo de 'articulos'
						articulo.set("titulo", disco.find('titulo').text)		# Establecemos sus atributos: (attrib 'titulo' = 'titulo del disco seleccionado')
						articulo.set("precio_unit", disco.find('precio').text)	# (attrib 'precio_unit' = 'precio del disco seleccionado')
						
						print("\nSeleccione el formato a vender: \n\n1.-\tCD\n2.-\tDVD\n3.-\tVinilos\n4.-\tCassettes\n\n0.-\tCancelar")

						try:								# Utilizamos 'Try' para capturar posibles errores al introducir datos
							opt = int(input())				# Introducimos la opcion deseada
							if (opt == 1):					
								print("\nIntroduzca el numero de CD a vender: (0 para cancelar)\n")
								cantidad = validarStock(validarInteger(str(input()), False), int(disco[2][0].text)) 	# Validamos Integer, y a su vez validamos el Stock
								if (not cantidad == 0):																	# En caso de seleccionar 0, cancelamos la operacion
									if (cantidad):																		# Si la cantidad demandada es valida
										newCantidad = (int(disco[2][0].text) - cantidad)								# Se actualiza el stock restante
										print("\nStock demandado: ",cantidad,"\nStock CD restante: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")		# informamos del stock y pedimos confirmacion
										confirmacion = confirmarOperacion()
										if confirmacion:																		# En caso de confirmarse la operacion
											articulo.set("formato", disco[2][0].tag)											# Creamos un nuevo atributo para 'articulo' con el tipo de disco adquirido
											articulo.text = str(cantidad)														# Establecemos el numero de ejemplares para ese articulo (disco y formato)
											importe.text = str(cantidad * float(disco[5].text))									# Calculamos y recogemos el precio de ese articulo, con esa cantidad
											disco[2][0].text = str(newCantidad)													# Actualizamos en la subraiz de discos la nueva cantidad tras la venta
											guardarXml(raiz, fichero)															# guardamos, con el fin de conservar almacenados, el tipo, cantidad y precio del primer articulo
											print("\nStock retirado correctamente\n¿Desea comprar otro formato? (S/N))\n")
											repetirStock = confirmarOperacion()
											if not repetirStock:																# Estructura para determinar si queremos otro articulo del mismo disco (ej: otro formato distinto)
												flag = True
												print("\n¿Desea comprar otro disco diferente? (S/N)\n")
												repetirVenta = confirmarOperacion()
												if not repetirVenta:															# Estructura para determinar si queremos comprar un disco diferente
													terminar = True
										else:
											print("\nOperacion cancelada\n")													# En caso de no confirmar, cancelamos la operacion
											flag = True
								else:
									print("\nOperacion cancelada\n")															# Si introducimos una cantidad de 0, cancelamos la adquisicion del formato actual
									flag = True

							elif (opt == 2):																					# Repetimos la misma estructura que en 'CD'
								print("\nIntroduzca el numero de DVD a vender: (0 para cancelar)\n")
								cantidad = validarStock(validarInteger(str(input()), False), int(disco[2][1].text))
								if (not cantidad == 0):
									if (cantidad):
										newCantidad = (int(disco[2][1].text) - cantidad)
										print("\nStock demandado: ",cantidad,"\nStock CD restante: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
										confirmacion = confirmarOperacion()
										if confirmacion:
											articulo.set("formato", disco[2][1].tag)
											articulo.text = str(cantidad)
											importe.text = str(cantidad * float(disco[5].text))
											disco[2][1].text = str(newCantidad)
											guardarXml(raiz, fichero)
											print("\nStock retirado correctamente\n¿Desea comprar otro formato? (S/N))\n")
											repetirStock = confirmarOperacion()
											if not repetirStock:
												flag = True
												print("\n¿Desea comprar otro disco diferente? (S/N)\n")
												repetirVenta = confirmarOperacion()
												if not repetirVenta:
													terminar = True
										else:
											print("\nOperacion cancelada\n")
											flag = True
								else:
									print("\nOperacion cancelada\n")
									flag = True

							elif (opt == 3):																					# Repetimos la misma estructura que en 'CD' y 'DVD'
								print("\nIntroduzca el numero de Vinilos a vender: (0 para cancelar)\n")
								cantidad = validarStock(validarInteger(str(input()), False), int(disco[2][2].text))
								if (not cantidad == 0):
									if (cantidad):
										newCantidad = (int(disco[2][2].text) - cantidad)
										print("\nStock demandado: ",cantidad,"\nStock CD restante: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
										confirmacion = confirmarOperacion()
										if confirmacion:
											articulo.set("formato", disco[2][2].tag)
											articulo.text = str(cantidad)
											importe.text = str(cantidad * float(disco[5].text))
											disco[2][2].text = str(newCantidad)
											guardarXml(raiz, fichero)
											print("\nStock retirado correctamente\n¿Desea comprar otro formato? (S/N))\n")
											repetirStock = confirmarOperacion()
											if not repetirStock:
												flag = True
												print("\n¿Desea comprar otro disco diferente? (S/N)\n")
												repetirVenta = confirmarOperacion()
												if not repetirVenta:
													terminar = True
										else:
											print("\nOperacion cancelada\n")
											flag = True
								else:
									print("\nOperacion cancelada\n")
									flag = True

							elif (opt == 4):																					# Repetimos la misma estructura que en las opciones anteriores
								print("\nIntroduzca el numero de Cassettes a vender: (0 para cancelar)\n")
								cantidad = validarStock(validarInteger(str(input()), False), int(disco[2][3].text))
								if (not cantidad == 0):
									if (cantidad):
										newCantidad = (int(disco[2][3].text) - cantidad)
										print("\nStock demandado: ",cantidad,"\nStock CD restante: ", newCantidad,"\n¿Confirmar cambios? (S/N)\n")
										confirmacion = confirmarOperacion()
										if confirmacion:
											articulo.set("formato", disco[2][3].tag)
											articulo.text = str(cantidad)
											importe.text = str(cantidad * float(disco[5].text))
											disco[2][3].text = str(newCantidad)
											guardarXml(raiz, fichero)
											print("\nStock retirado correctamente\n¿Desea comprar otro formato? (S/N))\n")
											repetirStock = confirmarOperacion()
											if not repetirStock:
												flag = True
												print("\n¿Desea comprar otro disco diferente? (S/N)\n")
												repetirVenta = confirmarOperacion()
												if not repetirVenta:
													terminar = True
										else:
											print("\nOperacion cancelada\n")
											flag = True
								else:
									print("\nOperacion cancelada\n")
									flag = True

							elif (opt == 0):
								flag = True
							else:
								print("\nEntrada no valida\n")
						except ValueError:
							print("\nOperacion no reconocida\n")

			if (not encontrado):
				print("\nDisco no encontrado")
	
		print("\nIntroduzca su DNI, por favor: \n")					# Una vez el usuario haya terminado de anadir a la venta los discos
		dni.text = validarDNI(str(input()))							# y formatos deseados, se pide que introduzca su DNI. Este tambien sera validado

		importeTotal = 0											# Declaramos una variable para almacenar el importe total de la venta
		for articulo in subraizVentas[-1][0]:						# Recorremos el elemento articulo de la ultima venta
			precioUnidad = float(articulo.get('precio_unit'))		# Obtenemos el precio de cada articulo extrayendo la informadion de su atributo 'precio_unit'
			cantidad = int(articulo.text)							# Obtenemos la cantidad comprada
			importeTotal += precioUnidad * cantidad					# Sumamos al importe el resultado de multiplicar precio por cantidad, en cada articulo de nuestra venta
			print(importeTotal)

		importe.text = str(importeTotal)							# Establecemos el importe de la venta con el resultado

		print("\n" ,"/" * 20, "Detalles Venta", "/" * 20, "\n")
		venta = subraizVentas[-1]									# Mostramos por pantalla la ultima venta realizada (en este caso, sera la que estemos realizando en este momento,
		print("\nVenta",venta.get('id'),":")						# ya que hemos utilizado 'articulos' para guardar informacion esencial)
		for data in venta:											# recorremos los subnodos de venta:
			if data.tag == 'articulos':								# si alguno se llama 'articulos'
				print("\t",data.tag, ": ")
				for articulo in data:								# imprimimos todos los articulos con toda su informacion
					print("\n\t\tTitulo: ", articulo.get('titulo'), "\n\t\tFormato: ", articulo.get('formato'), "\n\t\tCantidad: ", articulo.text, "\n\t\tPrecio: ", articulo.get('precio_unit'), "\n")
			else:
				print("\t",data.tag, ": ", data.text)				# de no ser el elemento 'articulos' se imprime de manera normal (nombre: contenido)

		print("\n¿Confirmar Venta? (S/N)\n")
		confVenta = confirmarOperacion()							# Pedimos confirmacion de la venta
		if confVenta:												
			guardarXml(raiz, fichero)								# en caso afirmativo, se sobreescribe con los datos actualizados nuestra nueva venta
			print("\nVenta registrada\n")
		else:
			del(subraizVentas[-1])									# en caso negativo, eliminaremos la ultima venta (la actual)
			guardarXml(raiz, fichero)
	else:								#En su defecto, notificamos que han de existir discos obligatoriamente
		print("\nActualmente no existen discos almacenados\nPara realizar una venta, asegurese de que existen Discos disponibles\n")

# Metodo para mostrar todas las ventas existentes
def historialVentas():
	raiz = leerXml(fichero)					# Obtenemos la raiz del arbol xml
	subraiz = raiz[1]						# Acotamos el "area de accion" en Ventas, de manera que es mas simple operar en el
	check = comprobarNodos(subraiz)			# Comprobamos la existencias de hijos en el nodo 'ventas'

	if check:										# Si existen:
		for venta in subraiz:						# Para cada venta en subraiz ('ventas'):
			print("\nVenta",venta.get('id'),":")
			for data in venta:						# Para cada elemento en venta:
				if data.tag == 'articulos':			# si el nombre del elemento es 'articulos':
					print("\t",data.tag, ": ")
					for articulo in data:			# para cada elemento en 'articulos':
						print("\n\t\tTitulo: ", articulo.get('titulo'), "\n\t\tFormato: ", articulo.get('formato'), "\n\t\tCantidad: ", articulo.text, "\n\t\tPrecio: ", articulo.get('precio_unit'), "\n")
				else:								# En caso de no llamarse 'articulos', imprimimos los datos de manera "estandar" (Nombre: contenido)
					print("\t",data.tag, ": ", data.text)
	else:									# Si no existen ventas:
		print("\nActualmente no existen ventas registradas")

# Metodo que muestra las opciones dentro del menu discos
def submenuDiscos():
	flag = False
	while (not flag):			# Bucle para mantenernos dentro del menu en caso de introducir un dato erroneo
		print("\n","-"*40," MENU DISCOS ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Anadir disco\n2.- Eliminar disco\n3.- Modificar disco\n4.- Buscar disco\n5.- Mostrar discos\n6.- Restock de discos\n\n0.- Atras")

		try:											# Utilizamos 'Try' para capturar posibles errores al introducir datos
			opt = int(input())							# Introducimos la opcion deseada
			if (opt == 1):
				anadirDisco()
			elif (opt == 2):
				eliminarDisco()
			elif (opt == 3):
				modificarDisco()
			elif (opt == 4):
				buscarDisco()
			elif (opt == 5):
				mostrarDiscos()
			elif (opt == 6):
				restockDiscos()
			elif (opt == 0):
				flag = True								# Salimos del bucle y volvemos al Menu
			else:
				print("\nEntrada no valida\n")			# En caso de introducir un valor fuera de los recogidos
		except ValueError:
			print("\nOperacion no reconocida\n")		# En caso de introducir un valor distinto al esperado


def submenuVentas():
	flag = False
	while (not flag):			# Bucle para mantenernos dentro del menu en caso de introducir un dato erroneo
		print("\n","-"*40," MENU VENTAS ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Nueva Venta\n2.- Historial ventas\n\n0.- Atras")

		try:											# Utilizamos 'Try' para capturar posibles errores al introducir datos
			opt = int(input())							# Introducimos la opcion deseada
			if (opt == 1):
				nuevaVenta()
			elif (opt == 2):
				historialVentas()
			elif (opt == 0):							# Salimos del bucle y volvemos al Menu
				flag = True
			else:
				print("\nEntrada no valida\n")			# En caso de introducir un valor fuera de los recogidos
		except ValueError:
			print("\nOperacion no reconocida\n")		# En caso de introducir un valor distinto al esperado


def menu():
	flag = False
	while (not flag):			# Bucle para mantenernos dentro del menu en caso de introducir un dato erroneo
		print("\n","-"*40," Tienda de Discos ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- DISCOS\n2.- VENTAS\n\n0.- Salir")
		
		try:											# Utilizamos 'Try' para capturar posibles errores al introducir datos
			opt = int(input())							# Introducimos la opcion deseada
			if (opt == 1):
				submenuDiscos()
			elif (opt == 2):
				submenuVentas()
			elif (opt == 0):							# Salimos del bucle y volvemos al Menu
				print("\n¿Seguro que quiere cerrar el programa? (S/N) :\n")
				confirmacion = confirmarOperacion()		# Pedimos confirmacion para salir del programa
				if confirmacion:						# Si la respuesta es afirmativa, nos despedimos, y salimos del bucle
					print("\nHasta la vista :)\n")
					flag = True
				else:									# Si la respuesta es negativa, mostramos un mensaje, y seguimos en el bucle
					print("\nNos alegra que se quede :)\n")
			else:
				print("\nEntrada no valida\n")			# En caso de introducir un valor fuera de los recogidos
		except ValueError:
			print("\nOperacion no reconocida\n")		# En caso de introducir un valor distinto al esperado


inicializar()
menu()
