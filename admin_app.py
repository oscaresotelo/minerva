import streamlit as st
import os
import json
import uuid
from PIL import Image # Importar Image para el manejo de archivos

# --- Funciones de Gestión de Datos ---
def create_empty_data():
    """Crea una estructura de datos completa y vacía para el archivo JSON."""
    return {
        "products": [],
        "banners": [],
        "news": [],
        "testimonials": [],
        "nav_menu": ["Inicio", "Peluquería", "Barbería", "Accesorios", "Herramientas", "Equipamientos", "Novedades", "Contacto", "Sobre Nosotros"],
        "home_texts": {},
        "contact_info": {},
        "about_us": {},
        "faqs": [],
        "cta_texts": {}
    }

def load_data():
    """Carga los datos desde el archivo data.json o crea una estructura por defecto."""
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Asegura que todas las claves necesarias existan
                for key, default_value in create_empty_data().items():
                    if key not in data:
                        data[key] = default_value
                return data
            except json.JSONDecodeError:
                st.error("Error al decodificar el archivo data.json. Se usará una estructura vacía.")
                return create_empty_data()
    # Si el archivo no existe, crea la estructura completa
    return create_empty_data()

def save_data(data_to_save):
    """Guarda los datos en el archivo data.json."""
    try:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    except IOError as e:
        st.error(f"Error al guardar el archivo data.json: {e}")

# --- Configuración de la página del administrador ---
st.set_page_config(
    page_title="Panel de Administración Minerva",
    page_icon="⚙️",
    layout="wide",
)

# --- CSS personalizado ---
def local_css(file_name):
    """Importa un archivo CSS local."""
    try:
        if os.path.exists(file_name):
            with open(file_name, encoding="utf-8") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            st.warning(f"Advertencia: El archivo CSS '{file_name}' no se encontró.")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSS: {e}")

local_css("style.css")

# --- Lógica de la aplicación principal ---
data = load_data()

st.title("Panel de Administración de Minerva")
st.subheader("Bienvenido/a al Panel de Control. Gestiona el contenido de tu sitio web.")

# Barra lateral para navegación
st.sidebar.title("Menú de Gestión")
selection = st.sidebar.radio("Elige una sección:", [
    "Productos",
    "Banners",
    "Testimonios",
    "Textos de la Página de Inicio",
    "Gestión del Menú de Navegación",
    "Novedades",
    "Información de Contacto",
    "Textos de 'Sobre Nosotros'",
    "Preguntas Frecuentes (FAQs)",
    "Textos de Llamada a la Acción (CTA)"
])

# --- Gestión de Productos ---
if selection == "Productos":
    st.header("Gestión de Productos")
    st.markdown("Aquí puedes agregar, editar y eliminar los productos que se muestran en la tienda.")

    # Manejo de edición de producto
    product_to_edit = None
    if 'edit_product_id' in st.session_state and st.session_state.edit_product_id:
        product_to_edit = next((item for item in data["products"] if item["id"] == st.session_state.edit_product_id), None)
        if not product_to_edit:
            st.warning("Producto no encontrado para editar. Creando uno nuevo.")
            st.session_state.edit_product_id = None # Resetear para crear nuevo

    # Formulario para agregar/editar productos
    with st.form("product_form", clear_on_submit=True):
        st.subheader("Detalles del Producto")

        # Campos del formulario con títulos
        nombre = st.text_input("Nombre del Producto", value=product_to_edit.get("nombre", "") if product_to_edit else "")
        descripcion = st.text_area("Descripción Corta del Producto", value=product_to_edit.get("descripcion", "") if product_to_edit else "", height=100)
        precio = st.text_input("Precio (Ej: '$15.999')", value=product_to_edit.get("precio", "") if product_to_edit else "")

        # Campo para subir imagen
        st.subheader("Imagen del Producto")
        uploaded_image = st.file_uploader("Selecciona una imagen para el producto", type=["png", "jpg", "jpeg"], key="product_image_uploader")

        # Mostrar imagen actual si existe y permitir URL
        current_image_url = product_to_edit.get("imagen", "") if product_to_edit else ""
        if current_image_url:
            st.image(current_image_url, caption="Imagen Actual", use_column_width=True)

        imagen_url_input = st.text_input("O ingresa la URL de la Imagen (si no subes un archivo)", value=current_image_url)

        detalles = st.text_area("Detalles Completos del Producto", value=product_to_edit.get("detalles", "") if product_to_edit else "", height=200)

        submit_button = st.form_submit_button("Guardar Producto")

        if submit_button:
            if nombre and precio and descripcion:
                image_to_save = imagen_url_input # Inicialmente, toma la URL escrita

                if uploaded_image is not None:
                    # En una aplicación real, aquí guardarías la imagen en un servidor o almacenamiento
                    # y obtendrías su URL. Por ahora, simulamos que se guarda y se obtiene una URL.
                    # Ejemplo: image_to_save = save_uploaded_image_and_get_url(uploaded_image)
                    # Para este ejemplo, si se sube una imagen, la usaremos como URL temporal.
                    # Si tienes un sistema de archivos, deberías actualizar esta lógica.
                    try:
                        img = Image.open(uploaded_image)
                        img_path = f"images/{uploaded_image.name}" # Ruta donde se guardaría (simulado)
                        # Aquí deberías implementar la lógica para guardar la imagen de forma persistente
                        # y obtener su URL. Para este ejemplo, usaremos la ruta simulada.
                        # Si el archivo ya existe, podrías sobrescribirlo o renombrarlo.
                        # img.save(img_path) # Descomentar si tienes un sistema de guardado
                        image_to_save = img_path # Usamos la ruta simulada como referencia
                        st.warning(f"Imagen '{uploaded_image.name}' subida. En una implementación real, se guardaría y se generaría una URL.")
                    except Exception as e:
                        st.error(f"Error al procesar la imagen subida: {e}")
                        image_to_save = "" # Limpiar si hay error

                # Si se editaba un producto y no se subió nueva imagen, mantenemos la URL existente
                if product_to_edit and not uploaded_image and imagen_url_input:
                    image_to_save = imagen_url_input
                elif product_to_edit and not uploaded_image and not imagen_url_input and current_image_url:
                    image_to_save = current_image_url # Mantenemos la imagen anterior si no se sube ni se escribe nueva URL

                if 'product_to_edit' in locals() and product_to_edit: # Si estamos editando
                    product_to_edit.update({
                        "nombre": nombre,
                        "descripcion": descripcion,
                        "precio": precio,
                        "imagen": image_to_save,
                        "detalles": detalles
                    })
                    st.success("Producto actualizado con éxito!")
                else: # Si estamos agregando
                    new_product = {
                        "id": str(uuid.uuid4()),
                        "nombre": nombre,
                        "descripcion": descripcion,
                        "precio": precio,
                        "imagen": image_to_save,
                        "detalles": detalles
                    }
                    data["products"].append(new_product)
                    st.success("Producto agregado con éxito!")

                save_data(data)
                if 'product_to_edit' in locals():
                    del st.session_state.edit_product_id # Limpiar estado de edición
                st.rerun()
            else:
                st.error("Por favor, completa los campos obligatorios: Nombre, Descripción y Precio.")

    st.markdown("---")
    st.subheader("Lista de Productos Existentes")
    if not data["products"]:
        st.info("Aún no hay productos para mostrar.")
    else:
        # Usamos columnas para alinear los botones de acción
        for product in data["products"]:
            with st.expander(f"**{product.get('nombre', 'Producto sin nombre')}**"):
                col1, col2 = st.columns([1, 3]) # Divide el espacio para imagen y detalles
                with col1:
                    # Manejo seguro de imagen: usa placeholder si no hay URL o si la imagen no se carga
                    try:
                        if product.get('imagen'):
                            st.image(product.get('imagen'), width=150, use_column_width=False)
                        else:
                            st.image("https://via.placeholder.com/150x150.png?text=Sin+Imagen", width=150, use_column_width=False)
                    except Exception as e:
                        st.error(f"Error al cargar imagen: {e}")
                        st.image("https://via.placeholder.com/150x150.png?text=Error+Imagen", width=150, use_column_width=False)

                with col2:
                    st.write(f"**Descripción:** {product.get('descripcion', 'N/A')}")
                    st.write(f"**Precio:** {product.get('precio', 'N/A')}")
                    st.write(f"**URL Imagen:** {product.get('imagen', 'N/A')}")
                    st.write(f"**Detalles:** {product.get('detalles', 'N/A')}")

                # Botones de acción para cada producto
                col_buttons_1, col_buttons_2 = st.columns(2)
                with col_buttons_1:
                    if st.button("Eliminar", key=f"del_prod_{product['id']}"):
                        data["products"] = [p for p in data["products"] if p["id"] != product["id"]]
                        save_data(data)
                        st.success("Producto eliminado.")
                        st.rerun()
                with col_buttons_2:
                    if st.button("Editar", key=f"edit_prod_{product['id']}"):
                        st.session_state.edit_product_id = product["id"] # Almacenar el ID del producto a editar
                        st.rerun() # Recargar la app para mostrar el formulario de edición

# --- Gestión de Banners ---
elif selection == "Banners":
    st.header("Gestión de Banners")
    st.markdown("Aquí puedes gestionar las imágenes del carrusel en la página de inicio.")

    # Manejo de edición de banner (si se implementa en el futuro)
    banner_to_edit = None
    if 'edit_banner_id' in st.session_state and st.session_state.edit_banner_id:
        banner_to_edit = next((item for item in data["banners"] if item["id"] == st.session_state.edit_banner_id), None)
        if not banner_to_edit:
            st.warning("Banner no encontrado para editar.")
            st.session_state.edit_banner_id = None

    with st.form("banner_form", clear_on_submit=True):
        st.subheader("Agregar/Editar Banner")
        
        # Campo para subir imagen
        st.subheader("Imagen del Banner")
        uploaded_banner_image = st.file_uploader("Selecciona una imagen para el banner", type=["png", "jpg", "jpeg"], key="banner_image_uploader")
        
        # Mostrar imagen actual si existe y permitir URL
        current_banner_url = banner_to_edit.get("img", "") if banner_to_edit else ""
        if current_banner_url:
            try:
                st.image(current_banner_url, caption="Imagen Actual", use_column_width=True)
            except Exception as e:
                st.error(f"Error al cargar la imagen actual del banner: {e}")

        img_url = st.text_input("O ingresa la URL de la Imagen", value=current_banner_url)

        submit_button = st.form_submit_button("Guardar Banner")
        if submit_button:
            if uploaded_banner_image is not None:
                # En una aplicación real, aquí guardarías la imagen en un servidor o almacenamiento
                # y obtendrías su URL. Por ahora, simulamos que se guarda y se obtiene una URL.
                try:
                    img = Image.open(uploaded_banner_image)
                    img_path = f"images/{uploaded_banner_image.name}" # Ruta donde se guardaría (simulado)
                    # img.save(img_path) # Descomentar si tienes un sistema de guardado
                    img_url = img_path # Usamos la ruta simulada como referencia
                    st.warning(f"Imagen '{uploaded_banner_image.name}' subida. En una implementación real, se guardaría y se generaría una URL.")
                except Exception as e:
                    st.error(f"Error al procesar la imagen del banner subida: {e}")
                    img_url = "" # Limpiar si hay error
            
            if not img_url:
                st.error("Por favor, sube una imagen o introduce una URL de imagen para el banner.")
            else:
                if banner_to_edit: # Si estamos editando
                    banner_to_edit["img"] = img_url
                    st.success("Banner actualizado con éxito.")
                else: # Si estamos agregando
                    new_banner = {"img": img_url, "id": str(uuid.uuid4())}
                    data["banners"].append(new_banner)
                    st.success("Banner agregado.")
                save_data(data)
                if 'edit_banner_id' in st.session_state:
                    del st.session_state.edit_banner_id
                st.rerun()

    st.markdown("---")
    st.subheader("Banners Existentes")
    if not data["banners"]:
        st.info("Aún no hay banners para mostrar.")
    else:
        # Iterar sobre una copia para evitar problemas al modificar la lista mientras se itera
        for banner in list(data["banners"]):
            try:
                # Usar el ID directamente ya que está asegurado por la función create_empty_data
                with st.expander(f"**Banner {banner.get('id', 'sin ID')[:8]}**"):
                    st.image(banner.get('img'), caption=f"Banner {banner.get('id', 'sin ID')[:8]}", use_column_width=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Eliminar", key=f"del_ban_{banner['id']}"):
                            data["banners"] = [b for b in data["banners"] if b["id"] != banner["id"]]
                            save_data(data)
                            st.success("Banner eliminado.")
                            st.rerun()
                    with col2:
                         if st.button("Editar", key=f"edit_ban_{banner['id']}"):
                            st.session_state.edit_banner_id = banner["id"]
                            st.rerun()
            except KeyError:
                st.error("Error: Un banner no tiene un ID válido y no se puede gestionar.")
            except Exception as e:
                st.error(f"Ocurrió un error al mostrar el banner: {e}")

# --- Gestión de Testimonios ---
elif selection == "Testimonios":
    st.header("Gestión de Testimonios")
    st.markdown("Aquí puedes agregar y editar los testimonios de tus clientes.")

    with st.form("testimonial_form", clear_on_submit=True):
        st.subheader("Agregar Testimonio")
        name = st.text_input("Nombre del Cliente")
        city = st.text_input("Ciudad")
        quote = st.text_area("Cita del Testimonio", height=150)
        image_url = st.text_input("URL de la Imagen del Cliente (opcional)")

        submit_button = st.form_submit_button("Guardar Testimonio")
        if submit_button:
            if name and quote:
                new_testimonial = {
                    "name": name,
                    "city": city,
                    "quote": quote,
                    "image": image_url or "https://via.placeholder.com/100x100.png?text=User"
                }
                data["testimonials"].append(new_testimonial)
                save_data(data)
                st.success("Testimonio agregado con éxito.")
                st.rerun()
            else:
                st.error("Por favor, completa los campos obligatorios: Nombre y Cita.")

    st.markdown("---")
    st.subheader("Lista de Testimonios")
    if not data["testimonials"]:
        st.info("No hay testimonios para mostrar.")
    else:
        for i, test in enumerate(data["testimonials"]):
            with st.expander(f"**{test.get('name', 'Cliente sin nombre')} - {test.get('city', 'N/A')}**"):
                col1, col2 = st.columns([1, 4])
                with col1:
                    try:
                        # Manejo de error para la imagen del testimonio
                        if test.get('image'):
                            st.image(test.get('image'), width=75)
                        else:
                            st.image("https://via.placeholder.com/75x75.png?text=User", width=75)
                    except Exception as e:
                        st.error(f"Error al cargar imagen del testimonio: {e}")
                        st.image("https://via.placeholder.com/75x75.png?text=Error", width=75)
                with col2:
                    st.write(f"**Cita:** {test.get('quote')}")
                
                if st.button("Eliminar", key=f"del_test_{i}"):
                    data["testimonials"].pop(i)
                    save_data(data)
                    st.success("Testimonio eliminado.")
                    st.rerun()

# --- Gestión de Textos de la Página de Inicio ---
elif selection == "Textos de la Página de Inicio":
    st.header("Gestión de Textos de la Página de Inicio")
    st.markdown("Aquí puedes editar los textos principales de la página de inicio.")

    with st.form("edit_home_texts_form"):
        st.subheader("Textos Principales del Hero")
        data["home_texts"]['hero_title'] = st.text_input("Título Principal del Hero", value=data["home_texts"].get('hero_title', ''))
        data["home_texts"]['hero_subtitle'] = st.text_area("Subtítulo del Hero", value=data["home_texts"].get('hero_subtitle', ''), height=50)
        data["home_texts"]['hero_description'] = st.text_area("Descripción del Hero", value=data["home_texts"].get('hero_description', ''), height=100)

        st.markdown("---")
        st.subheader("Sección 'Por Qué Elegir Minerva'")
        data["home_texts"]['section1_title'] = st.text_input("Título de la Sección 'Por Qué Elegir Minerva'", value=data["home_texts"].get('section1_title', ''))
        data["home_texts"]['section1_description'] = st.text_area("Descripción de la Sección 'Por Qué Elegir Minerva'", value=data["home_texts"].get('section1_description', ''), height=50)

        st.markdown("---")
        st.subheader("Sección 'Nuestras Líneas de Productos'")
        data["home_texts"]['section2_title'] = st.text_input("Título de la Sección 'Líneas de Productos'", value=data["home_texts"].get('section2_title', ''))
        data["home_texts"]['section2_description'] = st.text_area("Descripción de la Sección 'Líneas de Productos'", value=data["home_texts"].get('section2_description', ''), height=50)

        st.markdown("---")
        st.subheader("Sección de Testimonios")
        data["home_texts"]['testimonials_title'] = st.text_input("Título de la Sección 'Testimonios'", value=data["home_texts"].get('testimonials_title', ''))
        data["home_texts"]['testimonials_description'] = st.text_area("Descripción de la Sección 'Testimonios'", value=data["home_texts"].get('testimonials_description', ''), height=50)

        st.markdown("---")
        st.subheader("Sección de Bestsellers")
        data["home_texts"]['bestsellers_title'] = st.text_input("Título de la Sección 'Más Vendidos'", value=data["home_texts"].get('bestsellers_title', ''))
        data["home_texts"]['bestsellers_description'] = st.text_area("Descripción de la Sección 'Más Vendidos'", value=data["home_texts"].get('bestsellers_description', ''), height=50)

        edit_texts_button = st.form_submit_button("Guardar Cambios")
        if edit_texts_button:
            save_data(data)
            st.success("Textos de inicio actualizados con éxito!")
            st.rerun()

# --- Gestión del Menú de Navegación ---
elif selection == "Gestión del Menú de Navegación":
    st.header("Gestión del Menú de Navegación")
    st.markdown("Puedes agregar, eliminar y reordenar los botones del menú superior.")

    with st.form("nav_menu_form", clear_on_submit=True):
        st.subheader("Agregar Nuevo Botón")
        new_item_name = st.text_input("Nombre del botón (Ej: 'Nuestra Historia')")
        submit_new_item = st.form_submit_button("Agregar al Menú")
        if submit_new_item and new_item_name:
            if new_item_name not in data["nav_menu"]:
                data["nav_menu"].append(new_item_name)
                save_data(data)
                st.success("Botón agregado con éxito.")
                st.rerun()
            else:
                st.error("Ese botón ya existe.")

    st.markdown("---")
    st.subheader("Menú Actual")
    if not data["nav_menu"]:
        st.info("El menú está vacío.")
    else:
        st.write("Usa los botones para reordenar o eliminar los elementos del menú.")
        # Iterar sobre una copia para evitar problemas al modificar la lista mientras se itera
        for i, item in enumerate(list(data["nav_menu"])):
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                st.markdown(f"**{i+1}. {item}**")
            with col2:
                if st.button("Eliminar", key=f"del_nav_{i}"):
                    data["nav_menu"].pop(i)
                    save_data(data)
                    st.success("Botón eliminado.")
                    st.rerun()
            with col3:
                # Asegurarse de que el índice sea válido antes de intentar mover hacia arriba
                if i > 0 and st.button("▲", key=f"up_nav_{i}"):
                    data["nav_menu"][i], data["nav_menu"][i-1] = data["nav_menu"][i-1], data["nav_menu"][i]
                    save_data(data)
                    st.rerun()
            with col4:
                # Asegurarse de que el índice sea válido antes de intentar mover hacia abajo
                if i < len(data["nav_menu"]) - 1 and st.button("▼", key=f"down_nav_{i}"):
                    data["nav_menu"][i], data["nav_menu"][i+1] = data["nav_menu"][i+1], data["nav_menu"][i]
                    save_data(data)
                    st.rerun()

# --- Gestión de Novedades ---
elif selection == "Novedades":
    st.header("Gestión de Novedades")
    st.markdown("Aquí puedes agregar y editar las noticias o entradas de blog que se muestran en la página de Novedades.")

    with st.form("news_form", clear_on_submit=True):
        st.subheader("Agregar Novedad")
        title = st.text_input("Título de la Novedad")
        content = st.text_area("Contenido completo de la Novedad", height=200)
        image_url = st.text_input("URL de la Imagen (opcional)")

        submit_button = st.form_submit_button("Guardar Novedad")
        if submit_button and title and content:
            new_news = {
                "titulo": title,
                "contenido": content,
                "imagen": image_url or "https://via.placeholder.com/400x300.png?text=Novedad",
                "fecha": "Fecha no disponible" # Puedes implementar la captura de fecha si lo necesitas
            }
            data["news"].append(new_news)
            save_data(data)
            st.success("Novedad agregada con éxito.")
            st.rerun()

    st.markdown("---")
    st.subheader("Lista de Novedades Existentes")
    if not data["news"]:
        st.info("No hay novedades para mostrar.")
    else:
        for i, news_item in enumerate(data["news"]):
            with st.expander(f"**{news_item.get('titulo', 'Novedad sin título')}**"):
                st.write(f"**Fecha:** {news_item.get('fecha', 'N/A')}")
                try:
                    if news_item.get('imagen'):
                        st.image(news_item.get('imagen'), width=200)
                    else:
                        st.image("https://via.placeholder.com/200x200.png?text=Sin+Imagen", width=200)
                except Exception as e:
                    st.error(f"Error al cargar imagen de novedad: {e}")
                    st.image("https://via.placeholder.com/200x200.png?text=Error+Imagen", width=200)

                st.write(f"**Contenido:** {news_item.get('contenido')}")
                if st.button("Eliminar", key=f"del_news_{i}"):
                    data["news"].pop(i)
                    save_data(data)
                    st.success("Novedad eliminada.")
                    st.rerun()

# --- Gestión de Información de Contacto ---
elif selection == "Información de Contacto":
    st.header("Gestión de Información de Contacto")
    st.markdown("Edita los datos de contacto que se muestran en tu página.")

    with st.form("contact_info_form"):
        st.subheader("Detalles de Contacto")
        data["contact_info"]['address'] = st.text_input("Dirección", value=data["contact_info"].get('address', ''))
        data["contact_info"]['phone'] = st.text_input("Teléfono", value=data["contact_info"].get('phone', ''))
        data["contact_info"]['email'] = st.text_input("Email", value=data["contact_info"].get('email', ''))
        data["contact_info"]['hours'] = st.text_area("Horarios de Atención", value=data["contact_info"].get('hours', ''), height=100)
        data["contact_info"]['facebook_url'] = st.text_input("URL de Facebook", value=data["contact_info"].get('facebook_url', ''))
        data["contact_info"]['instagram_url'] = st.text_input("URL de Instagram", value=data["contact_info"].get('instagram_url', ''))

        submit_button = st.form_submit_button("Guardar Contacto")
        if submit_button:
            save_data(data)
            st.success("Información de contacto actualizada.")
            st.rerun()

# --- Gestión de Textos de 'Sobre Nosotros' ---
elif selection == "Textos de 'Sobre Nosotros'":
    st.header("Gestión de Textos de 'Sobre Nosotros'")
    st.markdown("Edita los textos de la página 'Sobre Nosotros'.")

    with st.form("about_us_form"):
        st.subheader("Descripción General")
        data["about_us"]['about_description'] = st.text_area("Descripción de la empresa", value=data["about_us"].get('about_description', ''), height=150)

        st.subheader("Nuestra Filosofía y Misión")
        data["about_us"]['philosophy_title'] = st.text_input("Título de 'Nuestra Filosofía'", value=data["about_us"].get('philosophy_title', ''))
        data["about_us"]['philosophy_text'] = st.text_area("Texto de Filosofía", value=data["about_us"].get('philosophy_text', ''), height=100)
        data["about_us"]['mission_text'] = st.text_area("Texto de Misión", value=data["about_us"].get('mission_text', ''), height=100)

        st.subheader("Nuestros Valores")
        data["about_us"]['values_title'] = st.text_input("Título de 'Nuestros Valores'", value=data["about_us"].get('values_title', ''))
        data["about_us"]['value1_title'] = st.text_input("Título Valor 1", value=data["about_us"].get('value1_title', ''))
        data["about_us"]['value1_text'] = st.text_area("Texto Valor 1", value=data["about_us"].get('value1_text', ''), height=50)
        data["about_us"]['value2_title'] = st.text_input("Título Valor 2", value=data["about_us"].get('value2_title', ''))
        data["about_us"]['value2_text'] = st.text_area("Texto Valor 2", value=data["about_us"].get('value2_text', ''), height=50)
        data["about_us"]['value3_title'] = st.text_input("Título Valor 3", value=data["about_us"].get('value3_title', ''))
        data["about_us"]['value3_text'] = st.text_area("Texto Valor 3", value=data["about_us"].get('value3_text', ''), height=50)
        data["about_us"]['value4_title'] = st.text_input("Título Valor 4", value=data["about_us"].get('value4_title', ''))
        data["about_us"]['value4_text'] = st.text_area("Texto Valor 4", value=data["about_us"].get('value4_text', ''), height=50)

        submit_button = st.form_submit_button("Guardar Cambios")
        if submit_button:
            save_data(data)
            st.success("Textos de 'Sobre Nosotros' actualizados.")
            st.rerun()

# --- Gestión de Preguntas Frecuentes (FAQs) ---
elif selection == "Preguntas Frecuentes (FAQs)":
    st.header("Gestión de Preguntas Frecuentes")
    st.markdown("Agrega, edita y elimina las preguntas y respuestas.")

    with st.form("faq_form", clear_on_submit=True):
        st.subheader("Agregar/Editar FAQ")
        faq_q = st.text_input("Pregunta")
        faq_a = st.text_area("Respuesta", height=100)

        submit_button = st.form_submit_button("Guardar FAQ")
        if submit_button and faq_q and faq_a:
            new_faq = {"q": faq_q, "a": faq_a}
            data["faqs"].append(new_faq)
            save_data(data)
            st.success("FAQ agregada.")
            st.rerun()

    st.markdown("---")
    st.subheader("Lista de FAQs")
    if not data["faqs"]:
        st.info("No hay FAQs para mostrar.")
    else:
        for i, faq in enumerate(data["faqs"]):
            with st.expander(f"**{faq.get('q', 'Pregunta sin título')}**"):
                st.write(faq.get('a'))
                if st.button("Eliminar", key=f"del_faq_{i}"):
                    data["faqs"].pop(i)
                    save_data(data)
                    st.success("FAQ eliminada.")
                    st.rerun()

# --- Gestión de Textos de Llamada a la Acción (CTA) ---
elif selection == "Textos de Llamada a la Acción (CTA)":
    st.header("Gestión de Textos de CTA")
    st.markdown("Edita los textos de llamadas a la acción en la página de inicio.")

    with st.form("cta_form"):
        st.subheader("Texto del Banner Superior")
        data["cta_texts"]['banner_text'] = st.text_area("Texto del banner (Ej: 'Envíos Gratis')", value=data["cta_texts"].get('banner_text', ''), height=50)

        st.subheader("Texto del Banner Final")
        data["cta_texts"]['cta_title'] = st.text_input("Título del CTA", value=data["cta_texts"].get('cta_title', ''))
        data["cta_texts"]['cta_description'] = st.text_area("Descripción del CTA", value=data["cta_texts"].get('cta_description', ''), height=100)
        data["cta_texts"]['cta_button_text'] = st.text_input("Texto del botón del CTA", value=data["cta_texts"].get('cta_button_text', ''))

        submit_button = st.form_submit_button("Guardar Cambios")
        if submit_button:
            save_data(data)
            st.success("Textos de CTA actualizados.")
            st.rerun()