import streamlit as st

class ManualForm:
    @staticmethod
    def agregar_manual_form(db):

        categorias_x = [
            "Esencial",
            "Acción Decisiva",
            "Sistemas Operativos en el Campo de Batalla",
            "Complementarios al Desarrollo de Doctrina"
        ]

        subcategorias = {
            "Esencial": ["Ejército"],
            "Acción Decisiva": ["Maniobra", "AIE", "Operaciones Especiales"],
            "Sistemas Operativos en el Campo de Batalla": [
                "Inteligencia", "Mando Tipo Misión", "Apoyo de Fuegos", "Ingeniería", "Sostenimiento"
            ],
            "Complementarios al Desarrollo de Doctrina": [
                "Doctrina", "Términos y Símbolos Militares", "Proceso de Operaciones", "Liderazgo", "Entrenamiento de Unidades"
            ]
        }

        categoria_x = st.selectbox("Codificación Eje X:", categorias_x)
        subcategoria_x = st.selectbox("Subcodificación Eje X:", subcategorias.get(categoria_x, []))

        categorias_y = [
            "Manuales Fundamentales del Ejército",
            "Manuales Fundamentales de Referencia del Ejército",
            "Manuales de Campaña del Ejército",
            "Manuales de Técnicas del Ejército",
            "Manuales de Educación Militar",
            "Manuales de Mantenimiento del Ejército",
            "Manuales de Administrativo Funcional"
        ]
        categoria_y = st.selectbox("Codificación Eje Y:", categorias_y)

        nombre = st.text_input("Nombre del Manual:")
        opciones_anio = ["No Publicado"] + list(range(2018, 2031))  # Agregar la opción al inicio
        anio = st.selectbox("Año de Publicación:", opciones_anio)

        estados = ["Publicado", "Actualización", "En Generación", "Virtualizado", "Por Generar"]
        estado = st.selectbox("Estado del Manual:", estados)

        subproceso_estado = None
        if estado == "En Generación":
            subprocesos_estado = ["Investigación", "Experimentación", "Edición y Difusión"]
            subproceso_estado = st.selectbox("Subproceso del Estado:", subprocesos_estado)

        if st.button("Agregar Manual"):
            if (categoria_x, subcategoria_x, categoria_y, nombre, anio, estado):
                db.add_manual(categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado)
                st.success(f"✅ Manual '{nombre}' agregado correctamente.")
            else:
                st.error("❌ Todos los campos son obligatorios. Por favor, complete la información.")

    @staticmethod
    def modificar_manual_form(db, manual_id):
        manual = db.fetch_manual_by_id(manual_id)

        # Verificar si se encontró el manual
        if not manual:
            st.error(f"❌ No se encontró un manual con el ID {manual_id}. Verifique el número ingresado.")
            return

        categorias_x = [
            "Esencial", "Acción Decisiva", "Sistemas Operativos en el Campo de Batalla",
            "Complementarios al Desarrollo de Doctrina"
        ]

        subcategorias = {
            "Esencial": ["Ejército"],
            "Acción Decisiva": ["Maniobra", "AIE", "Operaciones Especiales"],
            "Sistemas Operativos en el Campo de Batalla": [
                "Inteligencia", "Mando Tipo Misión", "Apoyo de Fuegos", "Ingeniería", "Sostenimiento"
            ],
            "Complementarios al Desarrollo de Doctrina": [
                "Doctrina", "Términos y Símbolos Militares", "Proceso de Operaciones", "Liderazgo", "Entrenamiento de Unidades"
            ]
        }

        # Obtener valores de forma segura
        categoria_x_value = manual.get("categoria_x", categorias_x[0])
        subcategoria_x_value = manual.get("subcategoria_x", subcategorias[categoria_x_value][0] if categoria_x_value in subcategorias else "Ejército")
        categoria_y_value = manual.get("categoria_y", "Manuales Fundamentales del Ejército")

        # Manejo seguro de índices para evitar errores
        categoria_x = st.selectbox("Codificación Eje X:", categorias_x, index=categorias_x.index(categoria_x_value) if categoria_x_value in categorias_x else 0)
        subprocesos_x = subcategorias.get(categoria_x, [])
        subcategoria_x = st.selectbox("Subcodificación Eje X:", subprocesos_x, index=subprocesos_x.index(subcategoria_x_value) if subcategoria_x_value in subprocesos_x else 0)

        categorias_y = [
            "Manuales Fundamentales del Ejército",
            "Manuales Fundamentales de Referencia del Ejército",
            "Manuales de Campaña del Ejército",
            "Manuales de Técnicas del Ejército",
            "Normas y Procedimientos",
            "Material Complementario"
        ]
        categoria_y = st.selectbox("Subcodificación Eje Y:", categorias_y, index=categorias_y.index(categoria_y_value) if categoria_y_value in categorias_y else 0)

        nombre = st.text_input("Nombre del Manual:", value=manual.get("nombre", ""))
        opciones_anio = ["No Publicado"] + list(range(2018, 2031))  # Agregar opción "No Publicado"
        anio_actual = manual.get("anio", "No Publicado")  # Obtener el año guardado, si no existe usa "No Publicado"

        # Si el año guardado es un número, lo convertimos a entero, si no, lo dejamos como "No Publicado"
        if isinstance(anio_actual, str) and not anio_actual.isdigit():
            anio_actual = "No Publicado"
        else:
            anio_actual = int(anio_actual)

        anio = st.selectbox("Año de Publicación:", opciones_anio, index=opciones_anio.index(anio_actual))

        estados = ["Publicado", "Actualización", "En Generación", "Virtualizado", "Por Generar"]
        estado_actual = manual.get("estado", "Publicado")
        if estado_actual not in estados:
            estado_actual = "Publicado"
        estado = st.selectbox("Estado del Manual:", estados, index=estados.index(estado_actual))

        subproceso_estado = st.text_input("Subproceso del Estado:", value=manual.get("subproceso_estado", ""))

        if st.button("Guardar Cambios"):
            db.update_manual(manual_id, categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado)
            st.success(f"✅ Manual con ID {manual_id} actualizado correctamente.")

    @staticmethod
    def borrar_manual_form(db):
        manual_id = st.number_input("Ingrese el ID del manual a borrar:", min_value=1, step=1)

        if st.button("❌ Borrar Manual"):
            if db.delete_manual(manual_id):
                st.success(f"✅ Manual con ID {manual_id} eliminado correctamente.")
            else:
                st.error(f"❌ No se encontró un manual con ID {manual_id}. Verifique el número ingresado.")