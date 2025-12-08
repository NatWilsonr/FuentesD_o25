"""
DEMOSTRACIÓN: ¿Dónde se ve el "error" de ThreadPool para CPU-bound?

El código NO tiene error de sintaxis - funciona correctamente.
El "error" es usar la herramienta INCORRECTA para CPU-bound.
La EVIDENCIA está en los TIEMPOS de ejecución.
"""

import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_heavy(n):
    """Trabajo CPU-intensivo: cálculos puros sin I/O"""
    resultado = sum(range(n))
    return resultado

if __name__ == "__main__":
    print("="*70)
    print("DEMOSTRACIÓN: ThreadPool vs ProcessPool para CPU-bound")
    print("="*70)
    print(f"Cores disponibles: {os.cpu_count()}")
    print()
    
    # Datos: 8 tareas idénticas de trabajo CPU-intensivo
    datos = [10_000_000] * 8
    print(f"Tareas: {len(datos)} tareas de {datos[0]:,} iteraciones cada una")
    print()
    
    # ============================================================
    # BASELINE: Ejecución SECUENCIAL (sin paralelismo)
    # ============================================================
    print("-"*70)
    print("1️⃣  BASELINE: Ejecución SECUENCIAL")
    print("-"*70)
    inicio = time.time()
    resultados_seq = [cpu_heavy(n) for n in datos]
    tiempo_seq = time.time() - inicio
    print(f"⏱️  Tiempo secuencial: {tiempo_seq:.2f}s")
    print(f"   (Cada tarea toma ~{tiempo_seq/8:.2f}s)")
    print()
    
    # ============================================================
    # ThreadPoolExecutor (NO paralelo por GIL)
    # ============================================================
    print("-"*70)
    print("2️⃣  ThreadPoolExecutor (8 hilos)")
    print("-"*70)
    print("   ⚠️  Esto NO debería usarse para CPU-bound")
    print()
    
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        resultados_thread = list(executor.map(cpu_heavy, datos))
    tiempo_thread = time.time() - inicio
    
    print(f"⏱️  Tiempo con ThreadPool: {tiempo_thread:.2f}s")
    print(f"   📊 Speedup vs secuencial: {tiempo_seq/tiempo_thread:.2f}x")
    print()
    print("   🔍 ANÁLISIS:")
    print(f"   - Tiempo secuencial: {tiempo_seq:.2f}s")
    print(f"   - Tiempo ThreadPool: {tiempo_thread:.2f}s")
    print(f"   - Diferencia: {abs(tiempo_seq - tiempo_thread):.2f}s")
    
    if tiempo_thread >= tiempo_seq * 0.9:  # Si es casi igual (90% o más)
        print()
        print("   ❌ PROBLEMA DETECTADO:")
        print("   - ThreadPool es CASI IGUAL al secuencial")
        print("   - NO hay speedup significativo")
        print("   - Esto indica que NO hay paralelismo real")
        print("   - El GIL está limitando la ejecución simultánea")
    print()
    
    # ============================================================
    # ProcessPoolExecutor (SÍ paralelo)
    # ============================================================
    print("-"*70)
    print("3️⃣  ProcessPoolExecutor (8 procesos)")
    print("-"*70)
    print("   ✅ Esto SÍ da paralelismo real")
    print()
    
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=8) as executor:
        resultados_process = list(executor.map(cpu_heavy, datos))
    tiempo_process = time.time() - inicio
    
    print(f"⏱️  Tiempo con ProcessPool: {tiempo_process:.2f}s")
    print(f"   📊 Speedup vs secuencial: {tiempo_seq/tiempo_process:.2f}x")
    print()
    print("   🔍 ANÁLISIS:")
    print(f"   - Tiempo secuencial: {tiempo_seq:.2f}s")
    print(f"   - Tiempo ProcessPool: {tiempo_process:.2f}s")
    print(f"   - Mejora: {tiempo_seq - tiempo_process:.2f}s ({tiempo_seq/tiempo_process:.2f}x más rápido)")
    
    if tiempo_process < tiempo_seq * 0.5:  # Si es menos de la mitad
        print()
        print("   ✅ PARALELISMO REAL CONFIRMADO:")
        print("   - ProcessPool es SIGNIFICATIVAMENTE más rápido")
        print("   - Speedup cercano al número de cores")
        print("   - Esto indica ejecución simultánea en múltiples cores")
    print()
    
    # ============================================================
    # COMPARACIÓN FINAL
    # ============================================================
    print("="*70)
    print("📊 RESUMEN COMPARATIVO")
    print("="*70)
    print(f"{'Método':<25} {'Tiempo':>10} {'Speedup':>10} {'Paralelismo':>15}")
    print("-"*70)
    print(f"{'Secuencial':<25} {tiempo_seq:>9.2f}s {'1.00x':>10} {'❌ NO':>15}")
    print(f"{'ThreadPool (8 hilos)':<25} {tiempo_thread:>9.2f}s {tiempo_seq/tiempo_thread:>9.2f}x {'❌ NO':>15}")
    print(f"{'ProcessPool (8 procesos)':<25} {tiempo_process:>9.2f}s {tiempo_seq/tiempo_process:>9.2f}x {'✅ SÍ':>15}")
    print("="*70)
    print()
    print("💡 CONCLUSIÓN:")
    print()
    print("   El 'error' de ThreadPool NO es un error de código.")
    print("   El código funciona correctamente, pero:")
    print()
    print("   ❌ ThreadPool: Tiempo ~8s (casi igual al secuencial)")
    print("      → NO hay paralelismo real (GIL limita)")
    print()
    print("   ✅ ProcessPool: Tiempo ~1.5s (mucho más rápido)")
    print("      → SÍ hay paralelismo real (múltiples cores)")
    print()
    print("   📍 La EVIDENCIA del problema está en los TIEMPOS,")
    print("      no en errores de sintaxis o excepciones.")



