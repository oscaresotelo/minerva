import streamlit as st
from streamlit_carousel import carousel
import json
import os

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

def get_image_path(product_dict):
    """
    Verifica si la ruta de la imagen del producto existe.
    Si no existe, devuelve una URL de placeholder y muestra una advertencia.
    """
    img_path = product_dict.get("imagen")
    if not img_path:
        st.warning(f"Advertencia: No se encontró la URL de imagen para el producto con ID '{product_dict.get('id', 'N/A')}'.")
        return "https://via.placeholder.com/400x400.png?text=Imagen+No+Encontrada"
    
    # Construye la ruta de archivo completa para la verificación
    full_path = os.path.join(os.getcwd(), img_path.replace('/', os.sep))

    if not os.path.exists(full_path):
        st.warning(f"Advertencia: No se pudo encontrar el archivo de imagen en '{full_path}'.")
        return "https://via.placeholder.com/400x400.png?text=Imagen+No+Encontrada"
    
    return img_path

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
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
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

# Llamar a la función para cargar el CSS
local_css("style.css")

# --- Carrusel de imágenes (banners) para el Home principal ---
if banner_principal_items_raw:
    banner_principal_items = [
        dict(
            title="",
            text=" ",
            img=item.get("img", "https://via.placeholder.com/1920x600.png?text=Minerva+Banner"),
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
if 'show_mobile_nav' not in st.session_state:
    st.session_state.show_mobile_nav = False

# --- Header Completo (Banner, Logo, Búsqueda, Menú de Usuario) ---
st.markdown(f"""
    <div class="main-banner">
        {cta_texts.get('banner_text', 'Envíos Gratis en compras mayores a $100.000 - Entregas en el día en Gran San Miguel de Tucumán')}
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='header-container'>", unsafe_allow_html=True)
col_logo, col_search, col_menu = st.columns([1, 3, 2])
with col_logo:
        st.image("images/logo.png", width=150) # <-- Cambia "tu_logo.png" por el nombre de tu archivo de logo

with col_search:
    with st.container():
        st.session_state.search_term = st.text_input("¿Qué estás buscando?", value=st.session_state.search_term, placeholder="Buscar productos...", label_visibility="collapsed")

with col_menu:
    st.markdown("<div class='user-menu-container'>", unsafe_allow_html=True)
   
    st.markdown("<span><a href='#'>Mi carrito</a></span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Barra de Navegación Principal y Menú Móvil ---

# Menú para desktop
st.markdown("<div class='desktop-nav'>", unsafe_allow_html=True)
cols_nav = st.columns(len(nav_menu))
for i, item in enumerate(nav_menu):
    with cols_nav[i]:
        if st.button(item, key=f"nav_{item}"):
            st.session_state.page = item
            st.session_state.search_term = ""  # Limpiamos el término de búsqueda
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

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
                        st.image(get_image_path(product), use_container_width=True)
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
                st.session_state.page = "Productos"
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
                            st.image(get_image_path(product), use_container_width=True)
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
            st.markdown("<p>Innovación en cada producto para ofrecer resultados profesionales que superan las expectativas.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with benefits_col3:
            st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
            st.markdown('<img src="https://via.placeholder.com/50x50.png?text=Sostenible" class="benefit-icon">', unsafe_allow_html=True)
            st.markdown("<h4>Belleza Sostenible y Ética</h4>", unsafe_allow_html=True)
            st.markdown("<p>Comprometidos con el medio ambiente y libres de crueldad animal. Tu belleza en armonía con el planeta.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='section-title'>{home_texts.get('section2_title', 'Nuestras Líneas de Productos')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('section2_description', 'Encuentra la solución ideal para cada necesidad de tu cabello con nuestras fórmulas exclusivas.')}</p>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        col_promo_img, col_promo_text = st.columns([1.5, 1])
        with col_promo_img:
            st.image("https://via.placeholder.com/800x600.png?text=Línea+Profesional", caption="Descubre la diferencia profesional de Finisima", use_container_width=True)
        with col_promo_text:
            st.markdown("<div class='promo-text-block'>", unsafe_allow_html=True)
            st.markdown(f"<h3 class='promo-title'>{home_texts.get('promo_title', 'Línea Profesional de nuestros productos: Resultados de Salón en Casa')}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p class='promo-description'>{home_texts.get('promo_description', 'Desarrollada con **activos de última generación** y **tecnología avanzada** para restaurar la salud y belleza de tu cabello. Ideal para cabellos exigentes que buscan un cuidado superior.')}</p>", unsafe_allow_html=True)
            if st.button("Explorar Línea Profesional", key="discover_professional_line"):
                st.session_state.page = "Productos"
                st.session_state.search_term = ""
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='section-title'>{home_texts.get('testimonials_title', 'Lo Que Dicen Nuestros Clientes')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('testimonials_description', 'La satisfacción de quienes eligen Finisima, es nuestra mayor recompensa.')}</p>", unsafe_allow_html=True)
        cols_testimonials = st.columns(3)
        for i, test in enumerate(testimonials):
            with cols_testimonials[i % 3]:
                st.markdown("<div class='testimonial-card'>", unsafe_allow_html=True)
                #st.image(test.get('image', "https://via.placeholder.com/100x100.png?text=User"), width=100, use_container_width=False)
                st.markdown(f"<p class='testimonial-quote'>“{test['quote']}”</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='testimonial-author'><strong>{test['name']}</strong>, {test['city']}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
        st.markdown("<div class='lead-form-section'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='section-title' style='color: white;'>{home_texts.get('lead_title', '¡No te Pierdas Nuestras Novedades y Ofertas Exclusivas!')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description' style='color: white;'>{home_texts.get('lead_description', 'Sé la primera en enterarte de nuevos lanzamientos, promociones y tips de cuidado capilar. ¡Únete a la comunidad Finisima!')}</p>", unsafe_allow_html=True)
        with st.form("lead_capture_form"):
            col_form_email, col_form_name = st.columns(2)
            with col_form_email:
                email_lead = st.text_input("Tu Email", placeholder="ejemplo@email.com", key="lead_email")
            with col_form_name:
                name_lead = st.text_input("Tu Nombre (opcional)", placeholder="Tu Nombre", key="lead_name")
            privacy_agree = st.checkbox("Acepto recibir comunicaciones de Finisima Productos Capilares.", key="privacy_checkbox")
            submit_lead = st.form_submit_button("Suscribirme Ahora")
            if submit_lead:
                if email_lead and privacy_agree:
                    st.success("¡Gracias por suscribirte!")
                elif not email_lead:
                    st.error("Por favor, introduce tu email para suscribirte.")
                elif not privacy_agree:
                    st.error("Debes aceptar la política de privacidad para suscribirte.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='section-title'>{home_texts.get('bestsellers_title', 'Nuestros Más Vendidos')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{home_texts.get('bestsellers_description', 'Descubre los favoritos de nuestros clientes, probados y amados por sus resultados.')}</p>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        cols_best_sellers = st.columns(3)
        best_sellers_products = productos[:3]
        for i, product in enumerate(best_sellers_products):
            with cols_best_sellers[i % 3]:
                st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                st.image(get_image_path(product), caption=product['nombre'], use_container_width=True)
                st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p class='product-price'>{product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)
                if st.button(f"Ver Detalles", key=f"view_details_home_{product['id']}"):
                    st.session_state.selected_product_id = product['id']
                    st.session_state.page = "Productos"
                    st.session_state.search_term = ""
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="cta-banner-final">
                <h3 class="cta-title">{cta_texts.get('cta_title', '¿Listo para transformar tu cabello?')}</h3>
                <p class="cta-description">{cta_texts.get('cta_description', 'Explora nuestra colección completa y encuentra todo lo que necesitas para un cuidado capilar excepcional.')}</p>
                <a href="#" onclick="parent.postMessage({{streamlit: {{command: 'SET_PAGE', args: ['Productos']}}}}, '*')">
                    <button class="cta-button">
                        {cta_texts.get('cta_button_text', 'Ver Todos los Productos')}
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    elif st.session_state.page == "Peluquería":
        st.markdown("<h1 class='page-title'>Peluquería</h1>", unsafe_allow_html=True)
        st.info("Contenido para la sección de Peluquería.")
    elif st.session_state.page == "Barbería":
        st.markdown("<h1 class='page-title'>Barbería</h1>", unsafe_allow_html=True)
        st.info("Contenido para la sección de Barbería.")
    elif st.session_state.page == "Accesorios":
        st.markdown("<h1 class='page-title'>Accesorios</h1>", unsafe_allow_html=True)
        st.info("Contenido para la sección de Accesorios.")
    elif st.session_state.page == "Herramientas":
        st.markdown("<h1 class='page-title'>Herramientas</h1>", unsafe_allow_html=True)
        st.info("Contenido para la sección de Herramientas.")
    elif st.session_state.page == "Equipamientos":
        st.markdown("<h1 class='page-title'>Equipamientos</h1>", unsafe_allow_html=True)
        st.info("Contenido para la sección de Equipamientos.")
    elif st.session_state.page == "Productos":
        st.markdown("<h1 class='page-title'>Nuestros Productos</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>Explora nuestra amplia gama de productos para el cuidado capilar. Cada fórmula ha sido creada para nutrir, fortalecer y realzar la belleza natural de tu cabello.</p>", unsafe_allow_html=True)
        if st.session_state.selected_product_id:
            selected_product = next((p for p in productos if p['id'] == st.session_state.selected_product_id), None)
            if selected_product:
                st.subheader(f"Detalles de {selected_product['nombre']}")
                col_detail_img, col_detail_info = st.columns([1, 2])
                with col_detail_img:
                    st.image(get_image_path(selected_product), use_container_width=True)
                with col_detail_info:
                    st.markdown(f"<h2>{selected_product['nombre']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p class='product-price'>{selected_product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)
                    st.write(selected_product.get('detalles', 'Detalles no disponibles.'))
                    st.write(f"Descripción breve: {selected_product.get('descripcion', 'Descripción no disponible.')}")
                    if st.button(f"Añadir al Carrito de {selected_product['nombre']}", key=f"add_detail_{selected_product['id']}"):
                        st.success(f"'{selected_product['nombre']}' añadido al carrito (simulado).")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.session_state.selected_product_id = None

        st.subheader("Todos los Productos")
        cols_per_row = 3
        for i in range(0, len(productos), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(productos):
                    product = productos[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                        st.image(get_image_path(product), use_container_width=True)
                        st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p class='product-price'>{product.get('precio', 'Precio no disponible')}</p>", unsafe_allow_html=True)
                        with st.expander("Ver Detalles"):
                            st.write(product.get("detalles", "Detalles no disponibles."))
                            if st.button(f"Añadir al Carrito", key=f"add_{product['id']}"):
                                st.success(f"'{product['nombre']}' añadido al carrito (simulado).")
                        st.markdown("</div>", unsafe_allow_html=True)
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
                    st.image(novedad.get("imagen"), use_container_width=True)
                with col_news_content:
                    st.markdown(f"<h3>{novedad.get('titulo')}</h3>", unsafe_allow_html=True)
                    st.caption(f"Publicado el: {novedad.get('fecha', 'N/A')}")
                    st.write(novedad.get("contenido", "Contenido no disponible."))
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
    elif st.session_state.page == "Contacto":
        st.markdown("<h1 class='page-title'>Contacto</h1>", unsafe_allow_html=True)
        st.markdown("<p class='section-description'>¿Tienes alguna pregunta o comentario? ¡Estamos aquí para ayudarte a encontrar la solución capilar perfecta!</p>", unsafe_allow_html=True)
        contact_col1, contact_col2 = st.columns(2)
        with contact_col1:
            st.markdown("<div class='contact-form-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Envíanos un Mensaje</h3>", unsafe_allow_html=True)
            with st.form("contact_form"):
                nombre = st.text_input("Tu Nombre", placeholder="Ingresa tu nombre completo")
                email = st.text_input("Tu Email", placeholder="tu.email@ejemplo.com")
                mensaje = st.text_area("Tu Mensaje", placeholder="Escribe tu consulta aquí...", height=150)
                submit_button = st.form_submit_button("Enviar Mensaje")
                if submit_button:
                    if nombre and email and mensaje:
                        st.success("¡Mensaje enviado con éxito!")
                    else:
                        st.error("Por favor, completa todos los campos.")
            st.markdown("</div>", unsafe_allow_html=True)
        with contact_col2:
            st.markdown("<div class='contact-info-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Nuestra Información de Contacto</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Finisima Productos Capilares</strong></p>", unsafe_allow_html=True)
            st.markdown(f"<p>{contact_info.get('address', 'Calle Ficticia 123, San Miguel de Tucumán, Argentina')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Teléfono:</strong> {contact_info.get('phone', '+54 9 381 123-4567')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Email:</strong> <a href='mailto:{contact_info.get('email', 'info@finisimaproductoscapilares.com.ar')}'>{contact_info.get('email', 'info@finisimaproductoscapilares.com.ar')}</a></p>", unsafe_allow_html=True)
            st.markdown("<h3>Horarios de Atención</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{contact_info.get('hours', 'Lunes a Viernes: 9:00 AM - 6:00 PM<br>Sábados: 9:00 AM - 1:00 PM<br>Domingos y Feriados: Cerrado')}</p>", unsafe_allow_html=True)
            st.markdown("<h3>Síguenos en Redes</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="text-align: left; margin-top: 10px;">
                    <a href="{contact_info.get('facebook_url', 'https://facebook.com/minervaproductos')}" target="_blank" style="margin-right: 10px;">Facebook</a>
                    <a href="{contact_info.get('instagram_url', 'https://instagram.com/minervaproductos')}" target="_blank">Instagram</a>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
    elif st.session_state.page == "Sobre Nosotros":
        st.markdown("<h1 class='page-title'>Sobre Finisima Productos Capilares</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='section-description'>{about_us_texts.get('about_description', 'Somos una empresa argentina dedicada a la excelencia en el cuidado del cabello, con pasión por la belleza y el bienestar.')}</p>", unsafe_allow_html=True)
        st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('philosophy_title', 'Nuestra Filosofía')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{about_us_texts.get('philosophy_text', 'En Finisima, creemos que un cabello hermoso es un reflejo de bienestar y confianza. Por eso, nos esforzamos en desarrollar productos innovadores que combinan la ciencia y la naturaleza para ofrecer soluciones efectivas para todo tipo de cabello, desde seco y dañado hasta graso y con color. Consulta la descripción de cada producto para encontrar el ideal para ti.')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{about_us_texts.get('mission_text', 'Nuestra misión es empoderar a nuestros clientes a través de la confianza que les brinda un cabello sano, fuerte y radiante. Trabajamos con pasión y compromiso, utilizando ingredientes de la más alta calidad y procesos de producción sostenibles y éticos, cuidando tanto a tu cabello como al planeta.')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{about_us_texts.get('values_title', 'Nuestros Valores Fundamentales')}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">✨ {about_us_texts.get('value1_title', 'Calidad Inquebrantable:')}</strong> {about_us_texts.get('value1_text', 'Compromiso con la excelencia en cada formulación.')}</li>
                <li style="margin-bottom: 10px;"><strong style="color: #008C82;">🔬 {about_us_texts.get('value2_title', 'Innovación Constante:')}</strong> {about_us_texts.get('value2_text', 'Búsqueda y desarrollo de soluciones avanzadas y tecnologías de vanguardia.')}</li>
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
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("Finisima Productos Capilares - 2024 © Todos los derechos reservados.")
st.markdown("</div>", unsafe_allow_html=True)