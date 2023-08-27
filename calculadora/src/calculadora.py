import time
from src import operaciones

def calcular():
    print("Bienvenido a la calculadora")
    
    print("Ingrese un numero:")
    a = int(input())
    print("Ingrese otro numero:")
    b = int(input())
    
    print("""
          Seleccione la operacion a realizar:
          1 --> Sumar
          2 --> Restar
          3 --> Multiplicar
          4 --> Dividir
          """)
    option = input()
    print("Calculating...")
    time.sleep(2)
    result = 0
    match option:
        case "1":
            result = operaciones.suma(a, b)
        case "2":
            result = operaciones.resta(a, b)
        case "3":
            result = operaciones.multiplicacion(a, b)
        case "4":
            result = operaciones.division(a, b)
        case _:
            print("Opcion no valida")
            return
    print(f"""
            El resultado es --> {result}
        """)