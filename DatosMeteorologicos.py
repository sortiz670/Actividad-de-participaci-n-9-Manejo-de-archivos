import math

class DatosMeteorologicos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.direcciones_viento = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90,
            'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
            'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270,
            'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }

    def procesar_datos(self):
        temperaturas, humedades, presiones, velocidades_viento, grados_viento = [], [], [], [], []
        registro_actual = {}
        with open(self.nombre_archivo, 'r') as archivo:
            for linea in archivo:
                if linea.strip() == '':
                    if registro_actual:
                        
                        if 'Temperatura' in registro_actual:
                            temperaturas.append(float(registro_actual['Temperatura']))
                        if 'Humedad' in registro_actual:
                            humedades.append(float(registro_actual['Humedad']))
                        if 'Presion' in registro_actual:
                            presiones.append(float(registro_actual['Presion']))
                        if 'Viento' in registro_actual:
                            velocidad, direccion = registro_actual['Viento'].split(',')
                            velocidades_viento.append(float(velocidad))
                            grados_viento.append(self.direcciones_viento[direccion.strip()])
                        registro_actual = {}
                else:
                    clave, valor = linea.split(':', 1)  
                    registro_actual[clave.strip()] = valor.strip()

        
        temperatura_promedio = sum(temperaturas) / len(temperaturas)
        humedad_promedio = sum(humedades) / len(humedades)
        presion_promedio = sum(presiones) / len(presiones)
        velocidad_promedio_viento = sum(velocidades_viento) / len(velocidades_viento)

        
        suma_seno = sum(math.sin(math.radians(grado)) for grado in grados_viento)
        suma_coseno = sum(math.cos(math.radians(grado)) for grado in grados_viento)
        promedio_angulo = math.atan2(suma_seno, suma_coseno)
        promedio_grados = math.degrees(promedio_angulo) % 360
        direccion_predominante = min(self.direcciones_viento, key=lambda k: abs(self.direcciones_viento[k] - promedio_grados))

        return (temperatura_promedio, humedad_promedio, presion_promedio, velocidad_promedio_viento, direccion_predominante)


datos = DatosMeteorologicos('datos_meteorologicos.txt')
resultados = datos.procesar_datos()
print(f"Temperatura promedio: {resultados[0]}°C")
print(f"Humedad promedio: {resultados[1]}%")
print(f"Presión promedio: {resultados[2]} hPa")
print(f"Velocidad promedio del viento: {resultados[3]} km/h")
print(f"Dirección predominante del viento: {resultados[4]}")
