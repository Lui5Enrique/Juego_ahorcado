import random

def jugar_ahorcado():
    palabras = ['python', 'java', 'docker', 'linux', 'algoritmo', 'computacion', 'servidor']
    palabra_secreta = random.choice(palabras)
    letras_adivinadas = []
    intentos = 6

    print("=======================================")
    print("       ¡Bienvenido al AHORCADO!        ")
    print("=======================================")

    while intentos > 0:
        # Construir la palabra con las letras descubiertas o guiones
        estado_palabra = ""
        for letra in palabra_secreta:
            if letra in letras_adivinadas:
                estado_palabra += letra + " "
            else:
                estado_palabra += "_ "

        print(f"\nPalabra: {estado_palabra}")
        print(f"Te quedan {intentos} intentos.")

        # Verificar si ya ganó
        if "_" not in estado_palabra:
            print("\n¡Felicidades! Adivinaste la palabra exacta. 🎉")
            return

        entrada = input("Ingresa una letra: ").lower()

        # Validaciones simples
        if len(entrada) != 1 or not entrada.isalpha():
            print("Por favor, ingresa solo una letra válida.")
            continue
        
        if entrada in letras_adivinadas:
            print("Ya intentaste con esa letra, prueba con otra.")
            continue

        letras_adivinadas.append(entrada)

        # Comprobar si acertó o falló
        if entrada in palabra_secreta:
            print("¡Correcto!")
        else:
            print("Letra incorrecta.")
            intentos -= 1

    # Si sale del ciclo while y llega aquí, se quedó sin intentos
    print(f"\n ¡Perdiste! Te han ahorcado. La palabra era: {palabra_secreta}")

if __name__ == "__main__":
    jugar_ahorcado()