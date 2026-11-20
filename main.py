from src.agente import verificar


def main():
    print("Agente antidesinformación. Escriba 'salir' para terminar.\n")
    while True:
        texto = input("Afirmación (o Enter si solo envía imagen): ").strip()
        if texto.lower() == "salir":
            break
        ruta = input("Ruta de imagen (Enter para omitir): ").strip().strip('"')
        if not texto and not ruta:
            continue
        print("\nAnalizando...\n")
        print(verificar(texto, ruta or None))
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()