# Sistema Antifraude para Transacciones 🛡️

Sistema interactivo en consola desarrollado en Python para la evaluación y clasificación del riesgo de fraude en transacciones financieras.

## 🚀 Características

- **Evaluación de Riesgo**: Asigna un puntaje basado en 4 reglas de negocio (monto, hora, país de origen y dispositivo).
- **Clasificación**: Categoriza las transacciones en `NORMAL`, `SOSPECHOSA` o `ALTO RIESGO`.
- **Persistencia de Datos**: Guarda y carga la información en formato JSON automáticamente (`transacciones.json`).
- **Validaciones Integradas**: Control de entradas inválidas, valores negativos y campos vacíos.

## 📋 Reglas de Evaluación

| Criterio | Condición | Puntos |
| :--- | :--- | :--- |
| **Monto** | Mayor o igual a $2.000.000 | +30 |
| **Hora** | Operación realizada entre las 00:00 y las 05:00 | +20 |
| **País** | Diferente de Colombia | +25 |
| **Dispositivo** | No registrado/desconocido | +30 |

### Categorías de Riesgo
* **NORMAL**: 0 a 29 puntos.
* **SOSPECHOSA**: 30 a 59 puntos.
* **ALTO RIESGO**: 60 puntos o más.

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/tu-usuario/nombre-del-repositorio.git](https://github.com/tu-usuario/nombre-del-repositorio.git)
   cd nombre-del-repositorio
   ```

2. **Ejecutar el programa**:
   Asegúrate de tener instalado Python 3.8+:
   ```bash
   python main.py
   ```