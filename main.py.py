"""Sistema Antifraude para Transacciones.

Módulo principal que gestiona el cálculo de riesgo, la clasificación y la
persistencia de transacciones financieras en formato JSON.
"""

import json
import os


class Transaccion:
    """Representa una transacción financiera y calcula su nivel de riesgo."""

    def __init__(
        self,
        id: int,
        titular: str,
        valor: float,
        hora: int,
        pais: str,
        dispositivo_conocido: bool,
        puntaje_riesgo: int | None = None,
        clasificacion: str | None = None,
    ):
        self.id = id
        self.titular = titular
        self.valor = valor
        self.hora = hora
        self.pais = pais
        self.dispositivo_conocido = dispositivo_conocido

        # Si no se proveen al instanciar (p. ej. desde JSON), se calculan automáticamente
        if puntaje_riesgo is None:
            self.puntaje_riesgo = self.calcular_riesgo()
        else:
            self.puntaje_riesgo = puntaje_riesgo

        if clasificacion is None:
            self.clasificacion = self.clasificar()
        else:
            self.clasificacion = clasificacion

    def calcular_riesgo(self) -> int:
        """Calcula el puntaje de riesgo evaluando las 4 reglas de negocio."""
        puntaje = 0

        # Regla 1: Valor >= $2.000.000 (+30 puntos)
        if self.valor >= 2000000:
            puntaje += 30

        # Regla 2: Hora entre 0 y 5 (+20 puntos)
        if 0 <= self.hora <= 5:
            puntaje += 20

        # Regla 3: País diferente de Colombia (+25 puntos)
        if self.pais.strip().lower() != "colombia":
            puntaje += 25

        # Regla 4: Dispositivo NO conocido (+30 puntos)
        if not self.dispositivo_conocido:
            puntaje += 30

        return puntaje

    def clasificar(self) -> str:
        """Asigna la categoría según el puntaje acumulado."""
        if self.puntaje_riesgo < 30:
            return "NORMAL"
        elif self.puntaje_riesgo <= 59:
            return "SOSPECHOSA"
        else:
            return "ALTO RIESGO"

    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario serializable en JSON."""
        return {
            "id": self.id,
            "titular": self.titular,
            "valor": self.valor,
            "hora": self.hora,
            "pais": self.pais,
            "dispositivo_conocido": self.dispositivo_conocido,
            "puntaje_riesgo": self.puntaje_riesgo,
            "clasificacion": self.clasificacion,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Transaccion":
        """Reconstruye un objeto Transaccion desde un diccionario."""
        return cls(
            id=datos["id"],
            titular=datos["titular"],
            valor=datos["valor"],
            hora=datos["hora"],
            pais=datos["pais"],
            dispositivo_conocido=datos["dispositivo_conocido"],
            puntaje_riesgo=datos.get("puntaje_riesgo"),
            clasificacion=datos.get("clasificacion"),
        )

    def __str__(self) -> str:
        """Representación legible en texto para consola."""
        return (
            f"ID: {self.id} | Titular: {self.titular} | "
            f"Puntaje de riesgo: {self.puntaje_riesgo} | Clasificación: {self.clasificacion}"
        )


def cargar_transacciones(
    nombre_archivo: str = "transacciones.json",
) -> list[Transaccion]:
    """Carga los datos guardados en JSON si el archivo existe."""
    transacciones = []
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as file:
                datos = json.load(file)
                for item in datos:
                    transacciones.append(Transaccion.from_dict(item))
        except Exception as e:
            print(f"Error al leer el archivo {nombre_archivo}: {e}")
    return transacciones


def guardar_transacciones(
    transacciones: list[Transaccion],
    nombre_archivo: str = "transacciones.json",
) -> None:
    """Guarda la lista de transacciones en el archivo JSON."""
    lista_dicts = [t.to_dict() for t in transacciones]
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            json.dump(lista_dicts, file, indent=4, ensure_ascii=False)
        print(f"-> Datos guardados exitosamente en '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")


def pedir_booleano(mensaje: str) -> bool:
    """Solicita y valida respuestas afirmativas o negativas por consola."""
    while True:
        res = input(mensaje).strip().lower()
        if res in ["s", "si", "sí", "true", "1"]:
            return True
        elif res in ["n", "no", "false", "0"]:
            return False
        print("  ❌ Entrada inválida. Ingrese 's' para Sí o 'n' para No.")


def main():
    transacciones = cargar_transacciones()

    # Si es la primera ejecución y el JSON no existe, creamos los casos iniciales
    if not transacciones:
        casos_prueba = [
            Transaccion(1, "Laura Gómez", 3500000, 2, "Colombia", False),
            Transaccion(2, "Carlos Pérez", 500000, 14, "Colombia", True),
            Transaccion(3, "Ana Torres", 2500000, 10, "Perú", True),
        ]
        transacciones.extend(casos_prueba)
        guardar_transacciones(transacciones)

    while True:
        print("\n=== SISTEMA ANTIFRAUDE — MENÚ PRINCIPAL ===")
        print("1. Registrar nueva transacción")
        print("2. Listar todas las transacciones")
        print("3. Salir y guardar")

        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR NUEVA TRANSACCIÓN ---")

            nuevo_id = (
                max([t.id for t in transacciones], default=0) + 1
                if transacciones
                else 1
            )

            while True:
                titular = input("Nombre del titular: ").strip()
                if titular:
                    break
                print("  ❌ El titular no puede estar vacío.")

            while True:
                try:
                    valor = float(input("Valor monetario: "))
                    if valor > 0:
                        break
                    print("  ❌ El valor debe ser mayor a cero.")
                except ValueError:
                    print("  ❌ Ingrese un valor numérico válido.")

            while True:
                try:
                    hora = int(input("Hora de la operación (0-23): "))
                    if 0 <= hora <= 23:
                        break
                    print("  ❌ La hora debe estar entre 0 y 23.")
                except ValueError:
                    print("  ❌ Ingrese un número entero válido.")

            while True:
                pais = input("País de origen: ").strip()
                if pais:
                    break
                print("  ❌ El país no puede estar vacío.")

            dispositivo = pedir_booleano("¿Es un dispositivo conocido? (s/n): ")

            nueva_t = Transaccion(
                id=nuevo_id,
                titular=titular,
                valor=valor,
                hora=hora,
                pais=pais,
                dispositivo_conocido=dispositivo,
            )

            transacciones.append(nueva_t)
            guardar_transacciones(transacciones)

            print(f"\n✅ Registrada exitosamente:\n{nueva_t}")

        elif opcion == "2":
            print("\n==============================================")
            print("      LISTA DE TRANSACCIONES REGISTRADAS      ")
            print("==============================================")
            if not transacciones:
                print("No hay transacciones registradas.")
            else:
                for t in transacciones:
                    print(t)
            print("==============================================")

        elif opcion == "3":
            guardar_transacciones(transacciones)
            print("Programa finalizado correctamente.")
            break

        else:
            print("  ❌ Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()