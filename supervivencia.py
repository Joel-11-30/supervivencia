import random
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy import stats
from datetime import datetime

CARAMEL_TYPES = ['limon', 'huevo', 'pera']
NUM_PEOPLE = 10  # Valor por defecto

# ---------- FUNCIONES LÓGICAS DEL JUEGO ----------
def can_make_chupetin(inv):
    return inv['limon'] >= 2 and inv['huevo'] >= 2 and inv['pera'] >= 2

def make_chupetin(inv, pasos):
    inv['limon'] -= 2
    inv['huevo'] -= 2
    inv['pera'] -= 2

    faltantes = get_faltantes_para_proxima_combinacion(inv)
    extra = []
    for dulce, cantidad in faltantes.items():
        extra.extend([dulce] * min(cantidad, 2 - len(extra)))
    while len(extra) < 2:
        extra.append(random.choice(CARAMEL_TYPES))
    inv.update(extra)

    pasos.append(f"✅ Se hizo 1 chupetín (usando 2 limon, 2 huevo, 2 pera) y se recibieron: {extra}")
    return 1

def vender_chupetin(inv, pasos):
    faltantes = get_faltantes_para_proxima_combinacion(inv)
    elegidos = []
    for dulce, cantidad in faltantes.items():
        elegidos.extend([dulce] * min(cantidad, 6 - len(elegidos)))
    while len(elegidos) < 6:
        elegidos.append(random.choice(CARAMEL_TYPES))
    inv.update(elegidos)

    pasos.append(f"🔄 Se vendió 1 chupetín para obtener 6 caramelos: {elegidos}")

def get_faltantes_para_proxima_combinacion(inv):
    faltan = {
        'limon': max(0, 2 - inv['limon']),
        'huevo': max(0, 2 - inv['huevo']),
        'pera': max(0, 2 - inv['pera'])
    }
    return dict(sorted(faltan.items(), key=lambda x: -x[1]))

def interpretar_estadisticas(candies_por_persona):
    """Análisis estadístico con interpretación clara y mejorada"""
    valores = {'limon': [], 'huevo': [], 'pera': []}
    for dulces in candies_por_persona:
        contador = Counter(dulces)
        for tipo in CARAMEL_TYPES:
            valores[tipo].append(contador[tipo])

    resultados = []
    resultados.append("\n📊 INTERPRETACIÓN ESTADÍSTICA:")
    resultados.append("=" * 60)

    # Estadísticas descriptivas con interpretación
    resultados.append("\n📈 ANÁLISIS DE DISTRIBUCIÓN:")
    distribuciones_equilibradas = True
    tipo_mas_comun = ""
    tipo_menos_comun = ""
    max_promedio = 0
    min_promedio = float('inf')
    
    for tipo in CARAMEL_TYPES:
        data = valores[tipo]
        media = np.mean(data)
        std = np.std(data)
        total = sum(data)
        
        if media > max_promedio:
            max_promedio = media
            tipo_mas_comun = tipo
        if media < min_promedio:
            min_promedio = media
            tipo_menos_comun = tipo
        
        # Coeficiente de variación para medir dispersión
        cv = (std / media * 100) if media > 0 else 0
        
        resultados.append(f"  🍬 {tipo.upper()}:")
        resultados.append(f"    • Promedio por persona: {media:.2f} caramelos")
        resultados.append(f"    • Total obtenido: {total} caramelos")
        resultados.append(f"    • Variabilidad: {cv:.1f}% {'(Alta)' if cv > 50 else '(Baja)' if cv < 25 else '(Media)'}")

    # Interpretación de equilibrio
    diferencia_tipos = max_promedio - min_promedio
    if diferencia_tipos > 0.5:
        distribuciones_equilibradas = False
        resultados.append(f"\n⚖️ EQUILIBRIO DE DISTRIBUCIÓN:")
        resultados.append(f"  ❌ Distribución DESEQUILIBRADA")
        resultados.append(f"  📊 '{tipo_mas_comun}' es el más común ({max_promedio:.2f} promedio)")
        resultados.append(f"  📉 '{tipo_menos_comun}' es el menos común ({min_promedio:.2f} promedio)")
        resultados.append(f"  🔍 Diferencia: {diferencia_tipos:.2f} caramelos por persona")
    else:
        resultados.append(f"\n⚖️ EQUILIBRIO DE DISTRIBUCIÓN:")
        resultados.append(f"  ✅ Distribución EQUILIBRADA")
        resultados.append(f"  🎯 Los tres tipos tienen frecuencias similares")

    # ANOVA con interpretación práctica mejorada
    resultados.append(f"\n🔬 PRUEBA DE DIFERENCIAS (ANOVA):")
    f_val, p_val = stats.f_oneway(valores['limon'], valores['huevo'], valores['pera'])
    
    resultados.append(f"  📐 Estadístico F: {f_val:.4f}")
    resultados.append(f"  📊 Valor p: {p_val:.4f}")
    
    if p_val < 0.001:
        nivel_significancia = "MUY ALTA (p < 0.001)"
        interpretacion_tecnica = "Evidencia extremadamente fuerte de diferencias"
        interpretacion_practica = "Diferencias DEFINITIVAS entre tipos de caramelos"
        emoji_resultado = "🔴"
    elif p_val < 0.01:
        nivel_significancia = "ALTA (p < 0.01)"
        interpretacion_tecnica = "Evidencia muy fuerte de diferencias"
        interpretacion_practica = "Diferencias MUY SIGNIFICATIVAS entre tipos"
        emoji_resultado = "🟠"
    elif p_val < 0.05:
        nivel_significancia = "MODERADA (p < 0.05)"
        interpretacion_tecnica = "Evidencia suficiente de diferencias"
        interpretacion_practica = "Diferencias SIGNIFICATIVAS entre tipos"
        emoji_resultado = "🟡"
    elif p_val < 0.10:
        nivel_significancia = "DÉBIL (p < 0.10)"
        interpretacion_tecnica = "Evidencia débil de diferencias"
        interpretacion_practica = "Posibles diferencias menores"
        emoji_resultado = "🔵"
    else:
        nivel_significancia = "NO SIGNIFICATIVA (p ≥ 0.10)"
        interpretacion_tecnica = "No hay evidencia de diferencias"
        interpretacion_practica = "Los tipos se distribuyeron de forma similar"
        emoji_resultado = "🟢"
    
    resultados.append(f"  {emoji_resultado} Significancia: {nivel_significancia}")
    resultados.append(f"  🔍 Interpretación técnica: {interpretacion_tecnica}")
    resultados.append(f"  💡 Interpretación práctica: {interpretacion_practica}")
    
    if p_val < 0.05:
        resultados.append(f"  🎮 Impacto en el juego: Algunos jugadores tuvieron ventaja/desventaja")
        resultados.append(f"  ⚠️ Recomendación: Considerar mecanismos de balanceo")
    else:
        resultados.append(f"  🎮 Impacto en el juego: Condiciones equitativas para todos")
        resultados.append(f"  ✅ Recomendación: El sistema aleatorio funcionó correctamente")

    # Chi-cuadrado con interpretación mejorada
    resultados.append(f"\n🎲 PRUEBA DE UNIFORMIDAD (Chi-cuadrado):")
    total_candies = sum(sum(valores[tipo]) for tipo in CARAMEL_TYPES)
    esperado_por_tipo = total_candies / 3
    observado = [sum(valores[tipo]) for tipo in CARAMEL_TYPES]
    chi2, chi2_p = stats.chisquare(observado)
    
    resultados.append(f"  📐 Estadístico χ²: {chi2:.4f}")
    resultados.append(f"  📊 Valor p: {chi2_p:.4f}")
    resultados.append(f"  🎯 Esperado por tipo: {esperado_por_tipo:.1f} caramelos")
    resultados.append(f"  📊 Observado: {observado}")
    
    if chi2_p < 0.001:
        uniformidad = "EXTREMADAMENTE DESIGUAL"
        interpretacion_uni = "La distribución está muy lejos de ser uniforme"
        emoji_uni = "🔴"
        impacto_uni = "Juego potencialmente muy injusto"
    elif chi2_p < 0.01:
        uniformidad = "MUY DESIGUAL"
        interpretacion_uni = "La distribución se desvía significativamente de lo uniforme"
        emoji_uni = "🟠"
        impacto_uni = "Juego con desequilibrios importantes"
    elif chi2_p < 0.05:
        uniformidad = "MODERADAMENTE DESIGUAL"
        interpretacion_uni = "Hay cierto desequilibrio en la distribución"
        emoji_uni = "🟡"
        impacto_uni = "Juego con ligeros desequilibrios"
    else:
        uniformidad = "APROXIMADAMENTE UNIFORME"
        interpretacion_uni = "La distribución es razonablemente uniforme"
        emoji_uni = "🟢"
        impacto_uni = "Juego equitativo"
    
    resultados.append(f"  {emoji_uni} Uniformidad: {uniformidad}")
    resultados.append(f"  🔍 Interpretación: {interpretacion_uni}")
    resultados.append(f"  🎮 Evaluación: {impacto_uni}")

    # Análisis de normalidad con interpretación
    resultados.append(f"\n📊 PRUEBAS DE NORMALIDAD:")
    for tipo in CARAMEL_TYPES:
        if len(valores[tipo]) >= 3:  # Mínimo para Shapiro-Wilk
            shapiro_stat, shapiro_p = stats.shapiro(valores[tipo])
            
            if shapiro_p < 0.05:
                normalidad = "NO NORMAL"
                emoji_norm = "❌"
                interpretacion_norm = "Los datos no siguen una distribución normal"
            else:
                normalidad = "APROXIMADAMENTE NORMAL"
                emoji_norm = "✅"
                interpretacion_norm = "Los datos siguen aproximadamente una distribución normal"
            
            resultados.append(f"  🍬 {tipo.upper()}:")
            resultados.append(f"    {emoji_norm} Distribución: {normalidad} (p = {shapiro_p:.4f})")
            resultados.append(f"    💡 {interpretacion_norm}")

    # Análisis de equidad del juego con más detalle
    resultados.append(f"\n🎯 ANÁLISIS DE EQUIDAD DEL JUEGO:")
    total_necesario = len(candies_por_persona) * 6  # 6 caramelos por chupetín
    
    if chi2_p < 0.01 and p_val < 0.01:
        equidad = "🔴 JUEGO INJUSTO"
        explicacion = "Tanto la uniformidad como la igualdad entre tipos fallan"
        recomendacion = "URGENTE: Revisar el sistema de distribución aleatoria"
    elif chi2_p < 0.05 or p_val < 0.05:
        equidad = "🟡 JUEGO PARCIALMENTE INJUSTO"
        explicacion = "Hay desequilibrios detectables en la distribución"
        recomendacion = "RECOMENDADO: Considerar ajustes al sistema aleatorio"
    else:
        equidad = "🟢 JUEGO EQUITATIVO"
        explicacion = "La distribución aleatoria funcionó correctamente"
        recomendacion = "APROPIADO: El sistema actual es justo"
    
    resultados.append(f"  {equidad}")
    resultados.append(f"  📊 Explicación: {explicacion}")
    resultados.append(f"  💡 Recomendación: {recomendacion}")

    # Predicción de éxito con análisis estadístico
    total_disponible = total_candies
    resultados.append(f"\n🎯 PREDICCIÓN DE ÉXITO:")
    resultados.append(f"  📊 Caramelos totales disponibles: {total_disponible}")
    resultados.append(f"  📊 Caramelos necesarios (ideal): {total_necesario}")
    
    ratio_disponibilidad = total_disponible / total_necesario
    
    if ratio_disponibilidad >= 1.0:
        probabilidad_text = "ALTA"
        emoji = "🟢"
        confianza = "95%+"
    elif ratio_disponibilidad >= 0.8:
        probabilidad_text = "MEDIA-ALTA"
        emoji = "🟡"
        confianza = "70-85%"
    elif ratio_disponibilidad >= 0.6:
        probabilidad_text = "MEDIA"
        emoji = "🟠"
        confianza = "40-60%"
    else:
        probabilidad_text = "BAJA"
        emoji = "🔴"
        confianza = "<30%"
    
    resultados.append(f"  {emoji} Probabilidad de éxito: {probabilidad_text}")
    resultados.append(f"  📈 Nivel de confianza estimado: {confianza}")
    resultados.append(f"  📊 Ratio disponibilidad: {ratio_disponibilidad:.2f}")
     # Entropía con interpretación mejorada
    entropias = []
    for i, dulces in enumerate(candies_por_persona):
        contador = Counter(dulces)
        probs = [contador[tipo]/2 for tipo in CARAMEL_TYPES]  # 2 caramelos por persona
        entropia = -sum(p * np.log2(p) if p > 0 else 0 for p in probs)
        entropias.append(entropia)
    
    entropia_promedio = np.mean(entropias)
    entropia_maxima = np.log2(len(CARAMEL_TYPES))
    diversidad = entropia_promedio / entropia_maxima
    
    resultados.append(f"\n🌈 ANÁLISIS DE DIVERSIDAD (Entropía de Shannon):")
    resultados.append(f"  📊 Entropía promedio: {entropia_promedio:.3f} bits")
    resultados.append(f"  📊 Entropía máxima: {entropia_maxima:.3f} bits")
    resultados.append(f"  📊 Índice de diversidad: {diversidad:.1%}")
    
    if diversidad > 0.9:
        nivel_diversidad = "EXCELENTE"
        emoji_div = "🟢"
        interpretacion_div = "Distribución casi perfectamente diversa"
        impacto_div = "Experiencia muy variada para los jugadores"
    elif diversidad > 0.8:
        nivel_diversidad = "ALTA"
        emoji_div = "🟢"
        interpretacion_div = "Buena diversidad en las combinaciones"
        impacto_div = "Los jugadores recibieron mezclas variadas"
    elif diversidad > 0.6:
        nivel_diversidad = "MEDIA"
        emoji_div = "🟡"
        interpretacion_div = "Diversidad moderada"
        impacto_div = "Cierta variación en las combinaciones"
    elif diversidad > 0.4:
        nivel_diversidad = "BAJA"
        emoji_div = "🟠"
        interpretacion_div = "Poca diversidad en las combinaciones"
        impacto_div = "Combinaciones algo repetitivas"
    else:
        nivel_diversidad = "MUY BAJA"
        emoji_div = "🔴"
        interpretacion_div = "Muy poca diversidad"
        impacto_div = "Muchos jugadores recibieron combinaciones similares"
    
    resultados.append(f"  {emoji_div} Nivel de diversidad: {nivel_diversidad}")
    resultados.append(f"  🔍 Interpretación: {interpretacion_div}")
    resultados.append(f"  🎮 Impacto: {impacto_div}")

    return resultados

# ---------- LÓGICA PRINCIPAL DEL JUEGO ----------
def simular_juego():
    # Obtener número de participantes
    try:
        num_participantes = int(participantes_var.get())
        if num_participantes <= 0:
            messagebox.showerror("Error", "El número de participantes debe ser mayor a 0")
            return
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un número válido de participantes")
        return
    
    output_text.delete('1.0', tk.END)
    pasos = []

    people_candies = [random.choices(CARAMEL_TYPES, k=2) for _ in range(num_participantes)]
    all_candies = [c for pair in people_candies for c in pair]
    inventory = Counter(all_candies)

    chupetines = 0
    intercambios = 0

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pasos.append(f"🕐 Simulación iniciada: {timestamp}")
    pasos.append("=" * 70)

    pasos.append(f"\n🍬 DISTRIBUCIÓN INICIAL ({num_participantes} participantes):")
    for i, dulces in enumerate(people_candies, 1):
        pasos.append(f"  Persona {i:2}: {dulces}")

    total = sum(inventory.values())
    pasos.append("\n📊 INVENTARIO INICIAL:")
    for dulce in CARAMEL_TYPES:
        porcentaje = inventory[dulce]/total
        barra = "█" * int(porcentaje * 20)
        pasos.append(f"  {dulce.capitalize():<8}: {inventory[dulce]:2} ({porcentaje:.1%}) {barra}")

    pasos.append("\n🎯 PROCESO DE FABRICACIÓN:")
    paso_num = 1
    while can_make_chupetin(inventory):
        pasos.append(f"  Paso {paso_num}:")
        chupetines += make_chupetin(inventory, pasos)
        paso_num += 1

    pasos.append("\n🔄 PROCESO DE INTERCAMBIOS:")
    while chupetines < num_participantes:
        if chupetines == 0:
            pasos.append("\n❌ No se pueden hacer más chupetines ni intercambios posibles.")
            break
        pasos.append(f"  Intercambio {intercambios + 1}:")
        vender_chupetin(inventory, pasos)
        chupetines -= 1
        intercambios += 1
        while can_make_chupetin(inventory):
            pasos.append(f"    Fabricación adicional:")
            chupetines += make_chupetin(inventory, pasos)

    pasos.append("\n📦 INVENTARIO FINAL:")
    for dulce in CARAMEL_TYPES:
        pasos.append(f"  {dulce.capitalize():<8}: {inventory[dulce]:2}")
    
    pasos.append(f"\n🏆 RESULTADOS FINALES:")
    pasos.append(f"  🍭 Chupetines fabricados: {chupetines}")
    pasos.append(f"  🔄 Intercambios realizados: {intercambios}")
    pasos.append(f"  👥 Personas totales: {num_participantes}")

    if chupetines >= num_participantes:
        resultado = "✅ ¡OBJETIVO ALCANZADO! Cada persona tiene un chupetín."
        pasos.append(f"\n🎉 {resultado}")
    else:
        resultado = "❌ Objetivo no alcanzado. No hay suficientes chupetines."
        pasos.append(f"\n😞 {resultado}")

    # Agregar análisis estadístico con interpretación mejorada
    interpretacion = interpretar_estadisticas(people_candies)
    pasos.extend(interpretacion)

    # Mostrar resultados en la interfaz
    for linea in pasos:
        output_text.insert(tk.END, linea + "\n")

    # Mostrar mensaje final
    if chupetines >= num_participantes:
        messagebox.showinfo("🎉 ¡Éxito!", "✅ ¡Todos tienen al menos un chupetín!")
    else:
        messagebox.showwarning("😞 Objetivo no logrado", "❌ No se logró que todos tengan un chupetín.")

def simular_multiples():
    """Simular múltiples juegos para análisis estadístico"""
    # Obtener número de participantes
    try:
        num_participantes = int(participantes_var.get())
        if num_participantes <= 0:
            messagebox.showerror("Error", "El número de participantes debe ser mayor a 0")
            return
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un número válido de participantes")
        return
    
    num_sims = 100
    exitos = 0
    chupetines_totales = []
    intercambios_totales = []
    
    progress_window = tk.Toplevel(root)
    progress_window.title("Simulando...")
    progress_window.geometry("400x120")
    progress_window.resizable(False, False)
    
    ttk.Label(progress_window, text="Ejecutando 100 simulaciones para análisis robusto...").pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, length=350, mode='determinate')
    progress_bar.pack(pady=10)
    progress_bar['maximum'] = num_sims
    
    for i in range(num_sims):
        people_candies = [random.choices(CARAMEL_TYPES, k=2) for _ in range(num_participantes)]
        all_candies = [c for pair in people_candies for c in pair]
        inventory = Counter(all_candies)
        
        chupetines = 0
        intercambios = 0
        
        while can_make_chupetin(inventory):
            inventory['limon'] -= 2
            inventory['huevo'] -= 2
            inventory['pera'] -= 2
            chupetines += 1
        
        while chupetines < num_participantes and chupetines > 0:
            chupetines -= 1
            intercambios += 1
            for _ in range(6):
                inventory[random.choice(CARAMEL_TYPES)] += 1
            while can_make_chupetin(inventory):
                inventory['limon'] -= 2
                inventory['huevo'] -= 2
                inventory['pera'] -= 2
                chupetines += 1
        
        if chupetines >= num_participantes:
            exitos += 1
        chupetines_totales.append(chupetines)
        intercambios_totales.append(intercambios)
        
        progress_bar['value'] = i + 1
        progress_window.update()
    
    progress_window.destroy()
    
    # Análisis e interpretación de resultados múltiples
    tasa_exito = exitos/num_sims
    promedio_chupetines = np.mean(chupetines_totales)
    promedio_intercambios = np.mean(intercambios_totales)
    
    # Interpretación de la tasa de éxito
    if tasa_exito >= 0.8:
        interpretacion_exito = "🟢 EXCELENTE - El juego tiene alta probabilidad de éxito"
        recomendacion = "El juego funciona bien con este número de participantes"
    elif tasa_exito >= 0.6:
        interpretacion_exito = "🟡 BUENA - El juego tiene probabilidad moderada de éxito"
        recomendacion = "Considerar ajustar las reglas para mayor consistencia"
    elif tasa_exito >= 0.4:
        interpretacion_exito = "🟠 REGULAR - El juego es algo impredecible"
        recomendacion = "Recomendable reducir participantes o ajustar mecánicas"
    else:
        interpretacion_exito = "🔴 DIFÍCIL - El juego rara vez alcanza el objetivo"
        recomendacion = "Necesario revisar las reglas o reducir participantes"
    
    # Análisis de eficiencia
    if promedio_intercambios < 2:
        eficiencia = "🟢 ALTA - Pocos intercambios necesarios"
    elif promedio_intercambios < 5:
        eficiencia = "🟡 MEDIA - Intercambios moderados"
    else:
        eficiencia = "🔴 BAJA - Muchos intercambios requeridos"
    
    resultado_msg = f"""
🎯 ANÁLISIS DE 100 SIMULACIONES ({num_participantes} participantes):

📊 RESULTADOS GENERALES:
✅ Éxitos: {exitos}/100 ({tasa_exito:.1%})
❌ Fallos: {num_sims-exitos}/100 ({(num_sims-exitos)/num_sims:.1%})

🔍 INTERPRETACIÓN:
{interpretacion_exito}

💡 RECOMENDACIÓN:
{recomendacion}

📈 ANÁLISIS DETALLADO:

🍭 Chupetines producidos:
   • Promedio: {promedio_chupetines:.2f}
   • Rango: {np.min(chupetines_totales)} - {np.max(chupetines_totales)}
   • Variabilidad: {np.std(chupetines_totales):.2f}

🔄 Intercambios realizados:
   • Promedio: {promedio_intercambios:.2f}
   • Rango: {np.min(intercambios_totales)} - {np.max(intercambios_totales)}
   • Eficiencia: {eficiencia}

🎮 CONCLUSIÓN PARA EL DISEÑO DEL JUEGO:
{"Con " + str(num_participantes) + " participantes, el juego " + 
("funciona bien y es entretenido." if tasa_exito >= 0.6 else 
 "puede ser frustrante debido a la baja tasa de éxito.")}
"""
    
    messagebox.showinfo("📊 Análisis Estadístico Completo", resultado_msg)

def mostrar_ayuda():
    ayuda_texto = """
🎮 SIMULADOR DE CARAMELOS Y CHUPETINES

📝 OBJETIVO:
Lograr que cada participante obtenga al menos 1 chupetín.

🍬 REGLAS DEL JUEGO:
• Cada participante recibe 2 caramelos aleatorios (limón, huevo o pera)
• Para hacer 1 chupetín necesitas: 2 limón + 2 huevo + 2 pera
• Al hacer un chupetín, recibes 2 caramelos adicionales
• Puedes vender 1 chupetín para obtener 6 caramelos aleatorios

⚙️ CONFIGURACIÓN:
• Ajusta el número de participantes (1-100)
• Números más altos = mayor dificultad

🔍 TIPOS DE SIMULACIÓN:
• Individual: Simula 1 juego con análisis detallado
• Múltiple: Simula 100 juegos para estadísticas robustas

📊 INTERPRETACIÓN:
• El simulador analiza la equidad y probabilidades
• Proporciona recomendaciones para el diseño del juego
• Evalúa si el número de participantes es apropiado
"""
    messagebox.showinfo("🎮 Ayuda del Simulador", ayuda_texto)

# ---------- INTERFAZ GRÁFICA SIMPLIFICADA ----------
root = tk.Tk()
root.title("🍬 Simulador de Caramelos y Chupetines - Análisis Interpretativo")
root.geometry("1000x700")
root.configure(bg='#2c3e50')

# Estilo personalizado
style = ttk.Style()
style.theme_use('clam')
style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), foreground='#e74c3c')
style.configure('Subtitle.TLabel', font=('Helvetica', 11), foreground='#34495e')
style.configure('Custom.TButton', font=('Helvetica', 10, 'bold'))

# Frame principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Título
title_frame = ttk.Frame(main_frame)
title_frame.pack(fill=tk.X, pady=(0, 20))

title_label = ttk.Label(title_frame, text="🍭 SIMULADOR DE CARAMELOS Y CHUPETINES", 
                       style='Title.TLabel')
title_label.pack()

subtitle_label = ttk.Label(title_frame, text="Análisis Estadístico con Interpretación Inteligente", 
                          style='Subtitle.TLabel')
subtitle_label.pack()

# Frame de configuración
config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración", padding=10)
config_frame.pack(fill=tk.X, pady=(0, 10))

# Campo para número de participantes
ttk.Label(config_frame, text="👥 Número de participantes:", font=('Helvetica', 11)).pack(side=tk.LEFT)

participantes_var = tk.StringVar(value="10")
participantes_spinbox = ttk.Spinbox(config_frame, from_=1, to=100, width=10, 
                                   textvariable=participantes_var, font=('Helvetica', 11))
participantes_spinbox.pack(side=tk.LEFT, padx=(5, 20))

# Información adicional
info_label = ttk.Label(config_frame, text="ℹ️ Cada participante recibe 2 caramelos aleatorios", 
                      font=('Helvetica', 9), foreground='#7f8c8d')
info_label.pack(side=tk.LEFT)

# Frame de botones
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=(0, 10))

simulate_btn = ttk.Button(button_frame, text="🎮 Simular Juego Individual", 
                         command=simular_juego, style='Custom.TButton')
simulate_btn.pack(side=tk.LEFT, padx=(0, 10))

multiple_btn = ttk.Button(button_frame, text="📊 Análisis Múltiple (100 simulaciones)", 
                         command=simular_multiples, style='Custom.TButton')
multiple_btn.pack(side=tk.LEFT, padx=(0, 10))

clear_btn = ttk.Button(button_frame, text="🗑️ Limpiar", 
                      command=lambda: output_text.delete('1.0', tk.END), 
                      style='Custom.TButton')
clear_btn.pack(side=tk.LEFT)

# Botón de ayuda
help_btn = ttk.Button(button_frame, text="❓ Ayuda", 
                     command=lambda: mostrar_ayuda(), style='Custom.TButton')
help_btn.pack(side=tk.RIGHT)

# Área de resultados
results_frame = ttk.LabelFrame(main_frame, text="📊 Resultados e Interpretación", padding=10)
results_frame.pack(fill=tk.BOTH, expand=True)

# Text widget con scrollbar
text_container = ttk.Frame(results_frame)
text_container.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(text_container, wrap="word", font=("Consolas", 10), 
                     bg='#ecf0f1', fg='#2c3e50', relief='flat', bd=5)
scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=output_text.yview)
output_text.configure(yscrollcommand=scrollbar.set)

output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Barra de estado
status_frame = ttk.Frame(main_frame)
status_frame.pack(fill=tk.X, pady=(10, 0))

status_label = ttk.Label(status_frame, text="Listo para simular", font=('Helvetica', 10))
status_label.pack(side=tk.LEFT)

version_label = ttk.Label(status_frame, text="Versión 3.1 - Interpretación Estadística Mejorada", 
                         font=('Helvetica', 10))
version_label.pack(side=tk.RIGHT)

root.mainloop()