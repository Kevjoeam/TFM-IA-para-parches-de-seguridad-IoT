import streamlit as st
import os, sys, json, time
import pandas as pd

# CONFIGURACIÓN DE RUTAS
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
project_root = os.path.abspath(os.path.join(src_path, '..'))
if src_path not in sys.path: sys.path.insert(0, src_path)

from database.persistence import log_remediation_event
from ast_engine.context_pruner import prune_vulnerable_context
from ai_connector.local_patcher import generate_local_patch
from validation.patch_validator import run_validation

# Estados para métricas
if 'ahorro' not in st.session_state: st.session_state.ahorro = 0.0
if 'mttr_seconds' not in st.session_state: st.session_state.mttr_seconds = 0.0

# CONFIGURACIÓN ESTÉTICA 
st.set_page_config(page_title="IoT Self-Healing Dashboard", layout="wide")

st.title("🛡️ Panel de Conciencia Situacional - IA Patching")
st.markdown("Este panel representa el **Plano de Control (Nivel 3)** de la arquitectura propuesta en el TFM.")
st.markdown("---")

# --- BARRA LATERAL: CONFIGURACIÓN DEL SISTEMA ---
st.sidebar.header("⚙️ Configuración del Sistema")


# --- CONFIGURACIÓN DE CARPETA DE UPLOADS DE USUARIO ---
upload_dir = os.path.join(project_root, "uploads")
os.makedirs(upload_dir, exist_ok=True)  

# 1. CARGADOR DE ARCHIVOS
uploaded_file = st.sidebar.file_uploader("Subir nuevo Firmware/Script (.py)", type=["py"])

# 2. BUSCADOR DINÁMICO DE ARCHIVOS EXISTENTES EN /uploads
files_in_uploads = [f"uploads/{f}" for f in os.listdir(upload_dir) if f.endswith('.py')]

# Lógica para determinar qué archivo analizar
if uploaded_file is not None:
    # Guardar físicamente el archivo en la carpeta aislada /uploads
    target_file = f"uploads/{uploaded_file.name}"
    save_path = os.path.join(upload_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.info(f" 📁Usando archivo subido: {uploaded_file.name}")
else:
    target_file = st.sidebar.selectbox(
        "O seleccionar archivo detectado en /uploads", 
        options=files_in_uploads,
        help="Selecciona el código fuente del dispositivo IoT que deseas auditar."
    )


st.sidebar.markdown("### Motores usados")
st.sidebar.success("SAST Engine: Bandit")
st.sidebar.success(" AI Engine: Llama-3 (Local)")
st.sidebar.success("Validation: Docker Sandbox")

# LÓGICA DE EJECUCIÓN
if st.sidebar.button("ESCANEAR"):
    t_start = time.time()
    with st.status("Ejecutando orquestador de seguridad...", expanded=True) as status:
               
        # 1. Detección
        status.update(label="[1/4] Analizando código fuente con Bandit...")  # 
        report_path = os.path.join(project_root, "data", "reports", "vulnerability_report.json")
        os.system(f"bandit -f json -o {report_path} {os.path.join(project_root, target_file)} > nul 2>&1")
        
        # 2. Poda y Ahorro Dinámico
        status.update(label="[2/4] Optimizando contexto mediante poda de AST...") 
        contexto, issue, ahorro = prune_vulnerable_context(report_path)
        
        # --- SOLUCIÓN AL TYPEERROR ---
        if issue is None:
            status.update(label="Archivo Seguro", state="complete", expanded=False)
            st.success(f"Bandit no detectó vulnerabilidades en `{target_file}`. No se requiere parcheo.")

            st.stop() 
            
        st.session_state.ahorro = ahorro
        
        # 3. IA e Inferencia
        status.update(label="[3/4] Solicitando parche de seguridad a Llama-3...")  
        patch = generate_local_patch(contexto, issue['issue_text'])
        
        # 4. Validación en Sandbox
        status.update(label="[4/4] Validando integridad en Sandbox Docker...")  
        success = run_validation(patch)
        
        t_total = time.time() - t_start
        st.session_state.mttr_seconds = round(t_total, 1)
                
        if success:
            status.update(
                label="¡Escaneado con Éxito!",
                state="complete",
                expanded=False
            )
        else:
            status.update(
                label="Escaneado con Advertencias",
                state="error",
                expanded=False
            )

        log_remediation_event(
            issue['issue_text'],
            issue['line_number'],
            ahorro,
            patch,
            success,
            st.session_state.mttr_seconds
        )
    # COLUMNAS DE RESULTADOS 
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vulnerabilidad Detectada")
        st.error(f"**Hallazgo:** {issue['issue_text']}")
        st.info(f"**Línea:** {issue['line_number']}")
        st.markdown("**Contexto enviado a la IA (Poda AST):**")
        st.code(contexto, language="python")

    with col2:
        st.subheader("Solución Propuesta (Parche)")
        if success:
            st.success("Estado: Validado por Sandbox y Reescaneo SAST")
        else:
            st.warning("Estado: Error de Validación")
        st.markdown("**Código del Parche Sugerido por Llama-3:**")
        st.code(patch, language="python")
    
   

# MÉTRICAS
st.markdown("---")
st.subheader("Métricas de Rendimiento del Sistema")
m1, m2, m3 = st.columns(3)
m1.metric("Tiempo de remediación automatizada", f"{st.session_state.mttr_seconds}s", help="Tiempo total del ciclo: detección → generación → validación")
m2.metric("Reducción de Contexto", f"{st.session_state.ahorro}%", help="Optimización de contexto mediante poda AST")

# --- VISOR DE LA BASE DE DATOS (AUDITORÍA) CON CONTROL DE ERRORES ---
st.markdown("---")
st.subheader("📝 Historial de la Base de Datos (Auditoría)")
audit_file = os.path.join(project_root, "data", "reports", "audit_history.json")

if os.path.exists(audit_file) and os.path.getsize(audit_file) > 2:
    try:
        with open(audit_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("La base de datos está esperando el primer registro.")
            
    except (json.JSONDecodeError, ValueError):
        st.info("Base de datos lista para recibir nuevos registros.")
else:
    st.info("No hay registros en la base de datos de auditoría. ¡Inicia un ciclo para empezar!")