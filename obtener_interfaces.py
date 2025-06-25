from netmiko import ConnectHandler
import json

# Datos del router
router = {
    "dispositivo_tipo": "cisco_ios",
    "host": "192.168.56.113",
    "usuario": "cisco",
    "contrasena": "cisco123!"
}

# Conexión
conexion = ConnectHandler(
    device_type=router["dispositivo_tipo"],
    host=router["host"],
    username=router["usuario"],
    password=router["contrasena"]
)

# Obtener interfaces
salida = conexion.send_command("show ip interface brief")
lineas = salida.splitlines()[1:]  # Saltar encabezado

# Convertir a lista de diccionarios
interfaces = []
for linea in lineas:
    partes = linea.split()
    if len(partes) >= 6:
        interfaz = {
            "nombre": partes[0],
            "ip": partes[1],
            "estado": partes[4],
            "protocolo": partes[5]
        }
        interfaces.append(interfaz)

# Mostrar opciones al usuario
print("\nInterfaces disponibles:")
for i, intf in enumerate(interfaces):
    print(f"{i+1}. {intf['nombre']}")

opcion = input("\nEscribe el número de la interfaz que quieres ver (o presiona Enter para ver todas): ")

if opcion.strip().isdigit() and 1 <= int(opcion) <= len(interfaces):
    seleccionada = interfaces[int(opcion) - 1]
    print("\nInformación seleccionada (JSON):")
    print(json.dumps(seleccionada, indent=2))
else:
    print("\nMostrando todas las interfaces en formato JSON:")
    print(json.dumps(interfaces, indent=2))

# Preguntar por el running-config
ver_config = input("\n¿Deseas ver el running-config? (S para sí, X para salir): ").strip().upper()

if ver_config == "S":
    config = conexion.send_command("show running-config")
    print("\n--- RUNNING CONFIG ---")
    print(config)
else:
    print("\nSaliendo...")

conexion.disconnect()


