import yaml
import os

def generate_docker_compose(num_services):
    """
    Genera un archivo docker-compose.yml con el número especificado de servicios API.
    
    Args:
        num_services (int): Número de servicios API a generar
    """
    
    # Estructura base del docker-compose
    compose = {
        'version': '3.8',
        'services': {},
        'networks': {
            'blockchain_net': {
                'driver': 'bridge'
            }
        },
        'volumes': {
            'blockchain_data': {}
        }
    }

    # Generar servicios dinámicamente
    for i in range(1, num_services + 1):
        service_name = f'api{i}'
        
        # Configuración de cada servicio
        service_config = {
            'build': '.',  # Usa el Dockerfile en el directorio actual
            'ports': [f"{8000+i}:8000"],  # Puerto dinámico para cada servicio
            'networks': ['blockchain_net'],  # Conecta a la red blockchain
            'volumes': [
                '/var/run/docker.sock:/var/run/docker.sock',  # Acceso al daemon Docker
                'blockchain_data:/app/data'  # Volumen compartido para la blockchain
            ],
            'environment': {
                'CONTAINER_NAME': service_name  # Nombre del contenedor para identificación
            }
        }
        
        # Agregar servicio al compose
        compose['services'][service_name] = service_config

    # Asegurar que el archivo se guarde con la indentación correcta
    try:
        # Guardar el archivo docker-compose.yml
        with open('docker-compose.yml', 'w') as file:
            yaml.dump(compose, file, sort_keys=False, default_flow_style=False)
        return True
    except Exception as e:
        print(f"Error al generar el archivo: {str(e)}")
        return False

def validate_input(num):
    """
    Valida que el número de servicios sea válido
    
    Args:
        num (str): Número ingresado por el usuario
    Returns:
        bool: True si es válido, False si no
    """
    try:
        num = int(num)
        return 1 <= num <= 100  # Límite de 100 servicios por razones prácticas
    except ValueError:
        return False

def main():
    """Función principal del script"""
    print("=== Generador de Docker Compose para Blockchain ===")
    
    while True:
        num_services = input("\nIngrese el número de servicios API a crear (1-100): ")
        
        if not validate_input(num_services):
            print("Error: Por favor ingrese un número válido entre 1 y 100")
            continue
            
        num_services = int(num_services)
        
        if generate_docker_compose(num_services):
            print(f"\n✅ Archivo docker-compose.yml generado exitosamente con {num_services} servicios")
            print(f"📍 Los servicios usarán los puertos del {8001} al {8000 + num_services}")
            print("\nPara iniciar los servicios ejecute:")
            print("docker-compose up -d")
        else:
            print("\n❌ Error al generar el archivo docker-compose.yml")
        
        break

if __name__ == "__main__":
    main()