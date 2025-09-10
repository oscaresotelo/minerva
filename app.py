import streamlit as st
from streamlit_carousel import carousel
import json
import os
from PIL import Image

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
                st.error("Error al decodificar el archivo data.json. Se utilizarán datos de ejemplo.")
                return create_empty_data()
    return create_empty_data()

def get_image_path(image_url_or_path):
    """
    Verifica si la ruta de la imagen existe.
    Si no existe, devuelve una URL de placeholder.
    Acepta URLs directas o rutas de archivo locales.
    """
    if not image_url_or_path:
        return "https://via.placeholder.com/400x400.png?text=Imagen+No+Encontrada"

    if image_url_or_path.startswith("http://") or image_url_or_path.startswith("https://"):
        return image_url_or_path
    
    full_path = os.path.join(os.getcwd(), image_url_or_path.replace('/', os.sep))

    if not os.path.exists(full_path):
        return "https://via.placeholder.com/400x400.png?text=Imagen+No+Encontrada"
    
    return image_url_or_path


# --- Cargar datos al inicio de la aplicación ---
data = load_data()
productos = data.get("products", [])
banner_principal_items_raw = data.get("banners", [])
novedades = data.get("news", [])
testimonials = data.get("testimonials", [])
nav_menu = data.get("nav_menu", ["Inicio", "Peluquería", "Barbería", "Accesorios", "Herramientas", "Equipamientos", "Novedades", "Contacto", "Sobre Nosotros"])
home_texts = data.get("home_texts", {})
contact_info = data.get("contact_info", {})
about_us_texts = data.get("about_us", {})
faqs = data.get("faqs", [])
cta_texts = data.get("cta_texts", {})

# --- Configuración de la página ---
st.set_page_config(
    page_title="Finisima Productos Capilares",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Importar la fuente de Google Fonts y CSS personalizado ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def local_css(file_name):
    """Importa un archivo CSS local."""
    try:
        if os.path.exists(file_name):
            with open(file_name, encoding="utf-8") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            st.warning(f"Advertencia: El archivo CSS '{file_name}' no se encontró. Utilizando estilos por defecto.")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSS: {e}")

local_css("style.css")

# --- Carrusel de imágenes (banners) para el Home principal ---
if banner_principal_items_raw:
    banner_principal_items = [
        dict(
            title="",
            text=" ",
            img=get_image_path(item.get("img", "https://via.placeholder.com/1920x600.png?text=Minerva+Banner")),
            link=""
        ) for item in banner_principal_items_raw
    ]
else:
    banner_principal_items = [
        dict(
            title="",
            text=" ",
            img="https://via.placeholder.com/1920x600.png?text=Minerva+Banner"),
    ]

# --- Inicialización del estado de la página ---
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"
if 'selected_product_id' not in st.session_state:
    st.session_state.selected_product_id = None
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

# --- Header Completo (Banner, Logo, Búsqueda, Menú de Usuario) ---
st.markdown(f"""
    <div class="main-banner">
        {cta_texts.get('banner_text', 'Envíos Gratis en compras mayores a $100.000 - Entregas en el día en Gran San Miguel de Tucumán')}
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='header-container'>", unsafe_allow_html=True)
col_logo, col_search, col_user_menu = st.columns([1, 2, 1])
with col_logo:
    st.image(get_image_path("images/logo.png"), width=150)

with col_search:
    st.session_state.search_term = st.text_input("¿Qué estás buscando?", value=st.session_state.search_term, placeholder="Buscar productos...", label_visibility="collapsed")

with col_user_menu:
    st.markdown("<div class='user-menu-container'>", unsafe_allow_html=True)
    st.markdown("<span><a href='#'>Mi carrito</a></span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Barra de Navegación Principal y Menú Móvil ---

# Menú para desktop
st.markdown("<div class='desktop-nav'>", unsafe_allow_html=True)
spacer1, cols_nav, spacer2 = st.columns([1, 4, 1])
with cols_nav:
    cols_items = st.columns(len(nav_menu))
    for i, item in enumerate(nav_menu):
        with cols_items[i]:
            if st.button(item, key=f"nav_{item}"):
                st.session_state.page = item
                st.session_state.search_term = ""
                st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Menú para móvil usando la barra lateral
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>Menú</h3>", unsafe_allow_html=True)
    for item in nav_menu:
        if st.button(item, key=f"nav_sidebar_{item}"):
            st.session_state.page = item
            st.session_state.search_term = ""
            st.rerun()

# --- Contenido de las páginas ---
if st.session_state.search_term:
    st.markdown(f"<h1 class='page-title'>Resultados de búsqueda para: '{st.session_state.search_term}'</h1>", unsafe_allow_html=True)

    filtered_products = [
        product for product in productos
        if (st.session_state.search_term.lower() in product.get("nombre", "").lower() or
            st.session_state.search_term.lower() in product.get("descripcion", "").lower())
    ]

    if not filtered_products:
        st.info(f"No se encontraron productos que coincidan con '{st.session_state.search_term}'.")
    else:
        cols_per_row = 3
        for i in range(0, len(filtered_products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(filtered_products):
                    product = filtered_products[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                        st.image(get_image_path(product.get("imagen")), use_container_width=True)
                        st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p class='product-price'>{product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)
                        with st.expander("Ver Detalles"):
                            st.write(product.get("detalles", "Detalles no disponibles."))
                            if st.button(f"Añadir al Carrito", key=f"add_{product['id']}"):
                                st.success(f"'{product['nombre']}' añadido al carrito (simulado).")
                        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
    if st.button("Limpiar Búsqueda y Volver al Inicio"):
        st.session_state.page = "Inicio"
        st.session_state.search_term = ""
        st.rerun()

else:
    if st.session_state.page == "Inicio":
        st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
        col_hero_text, col_hero_carousel = st.columns([1, 2.5])
        with col_hero_text:
            st.markdown("<div class='hero-text-content'>", unsafe_allow_html=True)
            st.markdown(f"<h1 class='hero-title'>{home_texts.get('hero_title', 'Finisima: La Esencia de un Cabello Radiante')}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p class='hero-subtitle'>{home_texts.get('hero_subtitle', '**Formulaciones exclusivas** con botánicos premium y tecnología avanzada para **resultados de salón en casa**.')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='hero-description'>{home_texts.get('hero_description', 'Restauramos el brillo, la fuerza y la salud de tu cabello de manera sostenible, con un compromiso ético y productos Cruelty-Free.')}</p>", unsafe_allow_html=True)
            if st.button("Descubre Tu Transformación Capilar", key="explore_products_hero"):
                st.session_state.page = "Peluquería"
                st.session_state.search_term = ""
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with col_hero_carousel:
            carousel(items=banner_principal_items, width=1.0)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        st.markdown(f"<h2 class='section-title'>{home_texts.get('all_products_title', 'Nuestros Productos Destacados')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('all_products_description', 'Explora nuestra colección completa y encuentra la solución perfecta para tu cabello.')}</p>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)

        if not productos:
            st.info("Actualmente no hay productos disponibles.")
        else:
            cols_per_row = 3
            for i in range(0, len(productos), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(productos):
                        product = productos[i + j]
                        with cols[j]:
                            st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                            st.image(get_image_path(product.get('imagen')), use_container_width=True)
                            st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
                            st.markdown(f"<p class='product-price'>{product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)

                            with st.expander("Ver Detalles"):
                                st.write(product.get("detalles", "Detalles no disponibles."))
                                if st.button(f"Añadir al Carrito", key=f"add_{product['id']}"):
                                    st.success(f"'{product['nombre']}' añadido al carrito (simulado).")
                            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        st.markdown(f"<h2 class='section-title'>{home_texts.get('section1_title', '¿Por Qué Elegir Finisima? Tu Cabello Lo Merece.')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('section1_description', 'Descubre los pilares que hacen de Finisima la elección perfecta para un cuidado capilar excepcional.')}</p>", unsafe_allow_html=True)
        benefits_col1, benefits_col2, benefits_col3 = st.columns(3)
        with benefits_col1:
            st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
            st.markdown('<img src="https://via.placeholder.com/50x50.png?text=Botánico" class="benefit-icon">', unsafe_allow_html=True)
            st.markdown("<h4>Fórmulas Botánicas Premium</h4>", unsafe_allow_html=True)
            st.markdown("<p>Ingredientes naturales seleccionados que nutren y revitalizan tu cabello desde la raíz.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with benefits_col2:
            st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
            st.markdown('<img src="https://via.placeholder.com/50x50.png?text=Tecnología" class="benefit-icon">', unsafe_allow_html=True)
            st.markdown("<h4>Tecnología Capilar Avanzada</h4>", unsafe_allow_html=True)
            st.markdown("<p>Innovación y ciencia al servicio de la belleza. Nuestras fórmulas combinan lo mejor de la naturaleza con tecnologías de vanguardia.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with benefits_col3:
            st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
            st.markdown('<img src="https://via.placeholder.com/50x50.png?text=CrueltyFree" class="benefit-icon">', unsafe_allow_html=True)
            st.markdown("<h4>Ética y Sostenibilidad</h4>", unsafe_allow_html=True)
            st.markdown("<p>Somos una marca Cruelty-Free, comprometida con el respeto animal y el cuidado del planeta.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        if testimonials:
            st.markdown(f"<h2 class='section-title'>Lo Que Dicen Nuestros Clientes</h2>", unsafe_allow_html=True)
            st.markdown("<div class='testimonial-container'>", unsafe_allow_html=True)
            test_cols = st.columns(3)
            for i, testimonial in enumerate(testimonials):
                with test_cols[i]:
                    st.markdown("<div class='testimonial-card'>", unsafe_allow_html=True)
                    st.markdown(f"<p><i>\"{testimonial.get('text', 'Testimonio no disponible.')}\"</i></p>", unsafe_allow_html=True)
                    st.markdown(f"<strong>- {testimonial.get('author', 'Cliente Anónimo')}</strong>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        # Sección de "Productos Más Vendidos"
        st.markdown(f"<h2 class='section-title'>{home_texts.get('best_sellers_title', 'Nuestros Más Vendidos')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('best_sellers_description', 'Descubre los favoritos de nuestros clientes, productos que garantizan resultados increíbles y han conquistado a miles de personas.')}</p>", unsafe_allow_html=True)

        if productos:
            best_sellers = sorted(productos, key=lambda x: x.get('ventas', 0), reverse=True)[:3]
            cols = st.columns(3)
            for i, product in enumerate(best_sellers):
                with cols[i]:
                    st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                    st.image(get_image_path(product.get('imagen')), use_container_width=True)
                    st.markdown(f"<h4>{product.get('nombre')}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p class='product-price'>{product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "Peluquería":
        st.markdown("<h1 class='page-title'>Peluquería Profesional</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Una línea completa de productos diseñados para los profesionales más exigentes.</p>", unsafe_allow_html=True)
        
    elif st.session_state.page == "Barbería":
        st.markdown("<h1 class='page-title'>Barbería Profesional</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Productos esenciales para el cuidado de la barba y el afeitado perfecto.</p>", unsafe_allow_html=True)
    
    elif st.session_state.page == "Accesorios":
        st.markdown("<h1 class='page-title'>Accesorios Esenciales</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Encuentra las herramientas perfectas para complementar tu rutina de belleza.</p>", unsafe_allow_html=True)
    
    elif st.session_state.page == "Herramientas":
        st.markdown("<h1 class='page-title'>Herramientas Profesionales</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Cepillos, secadores, planchas y todo lo que necesitas para un acabado de salón.</p>", unsafe_allow_html=True)
    
    elif st.session_state.page == "Equipamientos":
        st.markdown("<h1 class='page-title'>Equipamientos para Salones</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Sillas, lava-cabezas y todo el mobiliario necesario para tu negocio.</p>", unsafe_allow_html=True)
    
    elif st.session_state.page == "Novedades":
        st.markdown("<h1 class='page-title'>Novedades y Blog</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Mantente al tanto de los últimos lanzamientos y tendencias en cuidado capilar. ¡Inspírate y cuida tu cabello como se merece!</p>", unsafe_allow_html=True)
        if not novedades:
            st.info("No hay novedades disponibles en este momento.")
        else:
            for novedad in novedades:
                st.markdown(f"<div class='news-card'>", unsafe_allow_html=True)
                col_news_img, col_news_content = st.columns([1, 2])
                with col_news_img:
                    image_to_display = get_image_path(novedad.get("imagen"))
                    st.image(image_to_display, use_container_width=True)
                with col_news_content:
                    st.markdown(f"<h3>{novedad.get('titulo')}</h3>", unsafe_allow_html=True)
                    st.caption(f"Publicado el: {novedad.get('fecha', 'N/A')}")
                    st.write(novedad.get("contenido", "Contenido no disponible."))
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)

    elif st.session_state.page == "Contacto":
        st.markdown("<h1 class='page-title'>Contáctanos</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Estamos aquí para ayudarte. Rellena el formulario o encuentra nuestros datos de contacto.</p>", unsafe_allow_html=True)
        contact_col1, contact_col2 = st.columns(2)
        with contact_col1:
            st.markdown("<div class='contact-form-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Envíanos un Mensaje</h3>", unsafe_allow_html=True)
            with st.form("contact_form"):
                name = st.text_input("Nombre")
                email = st.text_input("Email")
                message = st.text_area("Mensaje")
                submitted = st.form_submit_button("Enviar Mensaje")
                if submitted:
                    st.success(f"¡Gracias, {name}! Tu mensaje ha sido enviado.")
            st.markdown("</div>", unsafe_allow_html=True)

        with contact_col2:
            st.markdown("<div class='contact-info-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Nuestros Datos de Contacto</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Dirección:</strong> {contact_info.get('address', 'Dirección no disponible.')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Teléfono:</strong> {contact_info.get('phone', 'Teléfono no disponible.')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Email:</strong> {contact_info.get('email', 'Email no disponible.')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Horario:</strong> {contact_info.get('hours', 'Horario no disponible.')}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
    elif st.session_state.page == "Sobre Nosotros":
        st.markdown("<h1 class='page-title'>Sobre Nosotros</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Conoce la historia detrás de Finisima y nuestros valores.</p>", unsafe_allow_html=True)
        st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('about_title', 'Nuestra Historia')}</h3>", unsafe_allow_html=True)
        st.write(about_us_texts.get("about_story", "Historia no disponible."))
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('values_title', 'Nuestros Valores')}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <ul>
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">✨ {about_us_texts.get('value1_title', 'Calidad Superior:')}</strong> {about_us_texts.get('value1_text', 'Comprometidos con la excelencia en cada producto que creamos.')}</li>
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">🌱 {about_us_texts.get('value2_title', 'Innovación Constante:')}</strong> {about_us_texts.get('value2_text', 'Siempre a la vanguardia, explorando nuevos ingredientes y tecnologías de vanguardia.')}</li>
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">🌿 {about_us_texts.get('value3_title', 'Sostenibilidad y Ética:')}</strong> {about_us_texts.get('value3_text', 'Respeto por el medio ambiente y prácticas responsables en toda nuestra cadena de valor.')}</li>
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">💖 {about_us_texts.get('value4_title', 'Pasión por la Belleza:')}</strong> {about_us_texts.get('value4_text', 'Amor por lo que hacemos y dedicación por tu bienestar.')}</li>
            </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('faqs_title', 'Preguntas Frecuentes')}</h3>", unsafe_allow_html=True)
        for faq in faqs:
            with st.expander(faq.get("question", "Pregunta frecuente...")):
                st.write(faq.get("answer", "Respuesta no disponible."))
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('team_title', 'Conoce a Nuestro Equipo')}</h3>", unsafe_allow_html=True)
        st.write(about_us_texts.get("team_text", "Información del equipo no disponible."))
        st.markdown("</div>", unsafe_allow_html=True)


# --- Pie de página ---
st.markdown("<div class='footer'>", unsafe_allow_html=True)
col_social, col_contact, col_legal = st.columns(3)
with col_social:
    st.markdown("<h4>Síguenos</h4>", unsafe_allow_html=True)
    st.markdown("""
        <a href='#' class='social-icon'><img src='https://via.placeholder.com/30x30.png?text=F' alt='Facebook'></a>
        <a href='#' class='social-icon'><img src='https://via.placeholder.com/30x30.png?text=I' alt='Instagram'></a>
        <a href='#' class='social-icon'><img src='https://via.placeholder.com/30x30.png?text=T' alt='Twitter'></a>
    """, unsafe_allow_html=True)
with col_contact:
    st.markdown("<h4>Contacto</h4>", unsafe_allow_html=True)
    st.markdown(f"<p>Email: {contact_info.get('email', 'N/A')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p>Tel: {contact_info.get('phone', 'N/A')}</p>", unsafe_allow_html=True)
with col_legal:
    st.markdown("<h4>Legal</h4>", unsafe_allow_html=True)
    st.markdown("<p>Términos y Condiciones</p>", unsafe_allow_html=True)
    st.markdown("<p>Política de Privacidad</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)