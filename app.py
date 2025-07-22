import streamlit as st
from streamlit_carousel import carousel
import base64
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="Minerva Productos Capilares",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Importar la fuente de Google Fonts (Roboto) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# --- CSS personalizado para mejorar el estilo (asegúrate que style.css existe) ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"Advertencia: El archivo CSS '{file_name}' no se encontró. La aplicación se ejecutará sin estilos personalizados.")

local_css("style.css")

# --- CSS para asegurar la visibilidad del menú de hamburguesa y limpiar Streamlit por defecto ---
hide_st_style = """
<style>
#MainMenu { visibility: visible; }
header { visibility: visible; background-color: transparent; height: 2.875rem; box-shadow: none; }
footer { visibility: hidden; height: 0; }
.stApp { padding-top: 0rem; }

.main-header-content {
    padding-top: 1rem;
    padding-bottom: 0.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- Datos de ejemplo (productos) ---
productos = [
    {
        "id": "shampoo_nutricion",
        "nombre": "Shampoo Nutrición Intensa",
        "descripcion": "Formulado con aceites naturales para una hidratación profunda. Ideal para cabellos secos y dañados.",
        "precio": "AR$ 3.500",
        "imagen": "images/shampoo.jpg",
        "detalles": "Este shampoo reparador, enriquecido con argán y coco, fortalece el cabello desde la raíz hasta las puntas, aportando brillo y suavidad."
    },
    {
        "id": "acondicionador_brillo",
        "nombre": "Acondicionador Brillo Sedoso",
        "descripcion": "Desenreda y aporta un brillo espectacular. Con extracto de seda y vitaminas.",
        "precio": "AR$ 3.200",
        "imagen": "images/acondicionador.jpg",
        "detalles": "Consigue un cabello deslumbrante con este acondicionador que sella la cutícula y protege el color. Aroma duradero."
    },
    {
        "id": "mascara_reparadora",
        "nombre": "Máscara Reparadora Profunda",
        "descripcion": "Tratamiento intensivo para restaurar la vitalidad del cabello. Uso semanal recomendado.",
        "precio": "AR$ 4.800",
        "imagen": "images/mascara.jpg",
        "detalles": "Una máscara de rescate para cabellos extremadamente dañados. Su fórmula con queratina y biotina reconstruye la fibra capilar."
    },
    {
        "id": "serum_anti_frizz",
        "nombre": "Serum Anti-Frizz Control Total",
        "descripcion": "Elimina el encrespamiento y protege de la humedad. Textura ligera no grasa.",
        "precio": "AR$ 2.900",
        "imagen": "images/serum.jpg",
        "detalles": "Mantén tu peinado perfecto todo el día. Este serum crea una barrera protectora contra la humedad y el frizz."
    },
    {
        "id": "oleo_argan",
        "nombre": "Óleo de Argán Puro",
        "descripcion": "Aceite multiuso para brillo, hidratación y protección térmica. 100% puro.",
        "precio": "AR$ 5.500",
        "imagen": "images/oleo_argan.jpg",
        "detalles": "El oro líquido para tu cabello. Nutre, repara y aporta un brillo sublime sin apelmazar. Ideal para antes o después del peinado."
    },
    {
        "id": "protector_termico",
        "nombre": "Protector Térmico Esencial",
        "descripcion": "Protege el cabello del calor de planchas y secadores hasta 230°C.",
        "precio": "AR$ 2.700",
        "imagen": "images/protector_termico.jpg",
        "detalles": "Indispensable antes de usar herramientas de calor. Crea una capa protectora que previene el daño y mantiene la salud del cabello."
    }
]

# --- Función para obtener la imagen en base64 ---
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- Carrusel de imágenes (banners) para el Home principal ---
banner_principal_items = [
    dict(
        title="",
        text="",
        img=f"data:image/jpeg;base64,{get_base64_image('images/banner_principal1.jpg')}",
        link=""
    ),
    dict(
        title="",
        text="",
        img=f"data:image/jpeg;base64,{get_base64_image('images/banner_principal2.jpg')}",
        link=""
    ),
    dict(
        title="",
        text="",
        img=f"data:image/jpeg;base64,{get_base64_image('images/banner_principal3.jpg')}",
        link=""
    )
]

# --- Inicialización del estado de la página ---
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"

# --- Header Principal (Logo y Título visibles siempre en el área principal) ---
st.markdown("<div class='main-header-content'>", unsafe_allow_html=True)
logo_path = "images/logo_minerva.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.warning("Logo 'images/logo_minerva.png' no encontrado. Asegúrate de que esté en la carpeta 'images'.")

st.markdown("<h1 class='app-title'>Minerva Productos Capilares</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# --- Sidebar (Menú de navegación y redes sociales) ---
with st.sidebar:
    st.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
    
    logo_path_sidebar = "images/logo_minerva.png"
    if os.path.exists(logo_path_sidebar):
        st.image(logo_path_sidebar, width=150)
    else:
        st.markdown("<h3 style='text-align: center; color: white;'>Minerva</h3>", unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px solid #444; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: white; text-align: center; margin-bottom: 15px;'>Menú</h3>", unsafe_allow_html=True)
    
    pages = ["Inicio", "Productos", "Novedades", "Contacto", "Sobre Nosotros"]
    
    selected_page_sidebar = st.radio(
        "",
        pages,
        index=pages.index(st.session_state.page),
        key="sidebar_navigation_radio",
        help="Navegación principal de la aplicación"
    )
    st.session_state.page = selected_page_sidebar

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #CCCCCC; font-size: 0.9em; margin-top: 20px;'>Síguenos en redes:</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <a href="https://facebook.com/minervaproductos" target="_blank" style="margin: 0 5px;"><img src="data:image/png;base64,{get_base64_image('images/icon_facebook.png')}" width="30" height="30" alt="Facebook"></a>
            <a href="https://instagram.com/minervaproductos" target="_blank" style="margin: 0 5px;"><img src="data:image/png;base64,{get_base64_image('images/icon_instagram.png')}" width="30" height="30" alt="Instagram"></a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# --- Contenido de las páginas ---
if st.session_state.page == "Inicio":
    # --- Hero Section / Main Banner ---
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    col_hero_text, col_hero_carousel = st.columns([1, 2.5])

    with col_hero_text:
        st.markdown("<div class='hero-text-content'>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Minerva: La Esencia de un Cabello Radiante</h1>", unsafe_allow_html=True)
        st.markdown("<p class='hero-subtitle'>**Formulaciones exclusivas** con botánicos premium y tecnología avanzada para **resultados de salón en casa**.</p>", unsafe_allow_html=True)
        st.markdown("<p class='hero-description'>Restauramos el brillo, la fuerza y la salud de tu cabello de manera sostenible, con un compromiso ético y productos Cruelty-Free.</p>", unsafe_allow_html=True)
        
        if st.button("Descubre Tu Transformación Capilar", key="explore_products_hero"):
            st.session_state.page = "Productos"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_hero_carousel:
        valid_banner_items = [item for item in banner_principal_items if item["img"] != "data:image/jpeg;base64,"]
        if valid_banner_items:
            carousel(items=valid_banner_items, width=1.0)
        else:
            st.warning("No se pudieron cargar las imágenes del banner principal. Asegúrate de que 'banner_principal1.jpg', 'banner_principal2.jpg', etc., existan en la carpeta 'images'.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # --- Sección de Beneficios Clave ---
    st.markdown("<h2 class='section-title'>¿Por Qué Elegir Minerva? Tu Cabello Lo Merece.</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Descubre los pilares que hacen de Minerva la elección perfecta para un cuidado capilar excepcional.</p>", unsafe_allow_html=True)
    
    benefits_col1, benefits_col2, benefits_col3 = st.columns(3)

    with benefits_col1:
        st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{get_base64_image('images/icon_botanico.png')}' class='benefit-icon'>", unsafe_allow_html=True)
        st.markdown("<h4>Fórmulas Botánicas Premium</h4>", unsafe_allow_html=True)
        st.markdown("<p>Ingredientes naturales seleccionados que nutren y revitalizan tu cabello desde la raíz.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with benefits_col2:
        st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{get_base64_image('images/icon_tecnologia.png')}' class='benefit-icon'>", unsafe_allow_html=True)
        st.markdown("<h4>Tecnología Capilar Avanzada</h4>", unsafe_allow_html=True)
        st.markdown("<p>Innovación en cada producto para ofrecer resultados profesionales que superan las expectativas.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with benefits_col3:
        st.markdown("<div class='benefit-card'>", unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{get_base64_image('images/icon_sostenible.png')}' class='benefit-icon'>", unsafe_allow_html=True)
        st.markdown("<h4>Belleza Sostenible y Ética</h4>", unsafe_allow_html=True)
        st.markdown("<p>Comprometidos con el medio ambiente y libres de crueldad animal. Tu belleza en armonía con el planeta.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # --- Sección de Productos Destacados / Líneas ---
    st.markdown("<h2 class='section-title'>Nuestras Líneas de Productos</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Encuentra la solución ideal para cada necesidad de tu cabello con nuestras fórmulas exclusivas.</p>", unsafe_allow_html=True)
    st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)

    col_promo_img, col_promo_text = st.columns([1.5, 1])

    with col_promo_img:
        promo_image_path = "images/promo_linea_profesional.jpg"
        if os.path.exists(promo_image_path):
            st.image(promo_image_path, caption="Descubre la diferencia profesional de Minerva", use_container_width=True)
        else:
            st.warning(f"Imagen promocional '{promo_image_path}' no encontrada. Crea una para esta sección.")

    with col_promo_text:
        st.markdown("<div class='promo-text-block'>", unsafe_allow_html=True)
        st.markdown("<h3 class='promo-title'>Línea Profesional Minerva: Resultados de Salón en Casa</h3>", unsafe_allow_html=True)
        st.markdown("<p class='promo-description'>Desarrollada con **activos de última generación** y **tecnología avanzada** para restaurar la salud y belleza de tu cabello. Ideal para cabellos exigentes que buscan un cuidado superior.</p>", unsafe_allow_html=True)
        if st.button("Explorar Línea Profesional", key="discover_professional_line"):
            st.session_state.page = "Productos"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # --- Sección de Testimonios ---
    st.markdown("<h2 class='section-title'>Lo Que Dicen Nuestros Clientes</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>La satisfacción de quienes eligen Minerva, es nuestra mayor recompensa.</p>", unsafe_allow_html=True)
    
    testimonials = [
        {"name": "Sofía G.", "city": "Córdoba", "quote": "¡Absolutamente enamorada de mi cabello después de usar Minerva! Brillo y suavidad que nunca antes tuve. ¡Gracias!", "image": "images/testimonial1.jpg"},
        {"name": "Martina P.", "city": "Rosario", "quote": "Mi cabello estaba muy dañado y esta máscara reparadora hizo maravillas. ¡Realmente se siente como un tratamiento de salón en casa!", "image": "images/testimonial2.jpg"},
        {"name": "Camila A.", "city": "Buenos Aires", "quote": "El serum anti-frizz es mi salvación en los días de humedad. ¡Funciona increíble y no deja sensación grasa!", "image": "images/testimonial3.jpg"},
    ]

    test_col1, test_col2, test_col3 = st.columns(3)
    cols_testimonials = [test_col1, test_col2, test_col3]

    for i, test in enumerate(testimonials):
        with cols_testimonials[i]:
            st.markdown("<div class='testimonial-card'>", unsafe_allow_html=True)
            if os.path.exists(test['image']):
                st.image(test['image'], width=100, use_column_width=False) # Avatar redondo con CSS
            else:
                st.markdown(f"<div class='testimonial-avatar-fallback'></div>", unsafe_allow_html=True) # Fallback para avatar
            st.markdown(f"<p class='testimonial-quote'>“{test['quote']}”</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='testimonial-author'><strong>{test['name']}</strong>, {test['city']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # --- Sección de Captura de Datos (Lead Generation) ---
    st.markdown("<div class='lead-form-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title' style='color: white;'>¡No te Pierdas Nuestras Novedades y Ofertas Exclusivas!</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description' style='color: white;'>Sé la primera en enterarte de nuevos lanzamientos, promociones y tips de cuidado capilar. ¡Únete a la comunidad Minerva!</p>", unsafe_allow_html=True)
    
    with st.form("lead_capture_form"):
        col_form_email, col_form_name = st.columns(2)
        with col_form_email:
            email_lead = st.text_input("Tu Email", placeholder="ejemplo@email.com", key="lead_email")
        with col_form_name:
            name_lead = st.text_input("Tu Nombre (opcional)", placeholder="Tu Nombre", key="lead_name")
        
        privacy_agree = st.checkbox("Acepto recibir comunicaciones de Minerva Productos Capilares.", key="privacy_checkbox")
        
        submit_lead = st.form_submit_button("Suscribirme Ahora")

        if submit_lead:
            if email_lead and privacy_agree:
                st.success("¡Gracias por suscribirte! Revisa tu bandeja de entrada para confirmar.")
                # Aquí iría la lógica para guardar el email en una base de datos o servicio de email marketing
            elif not email_lead:
                st.error("Por favor, introduce tu email para suscribirte.")
            elif not privacy_agree:
                st.error("Debes aceptar la política de privacidad para suscribirte.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)


    # --- Sección de Productos Más Vendidos (mantengo esta) ---
    st.markdown("<h2 class='section-title'>Nuestros Más Vendidos</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Descubre los favoritos de nuestros clientes, probados y amados por sus resultados.</p>", unsafe_allow_html=True)
    st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)

    cols_best_sellers = st.columns(3)
    # Solo muestra un subconjunto de productos para los más vendidos
    best_sellers_products = productos[:3] # Muestra los primeros 3 como ejemplo

    for i, product in enumerate(best_sellers_products):
        with cols_best_sellers[i % 3]:
            st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
            if os.path.exists(product['imagen']):
                st.image(product["imagen"], caption=product['nombre'], use_container_width=True)
            else:
                st.warning(f"Imagen no encontrada: {product['imagen']}")
            st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p class='product-price'>{product['precio']}</p>", unsafe_allow_html=True)
            if st.button(f"Ver Detalles", key=f"view_details_home_{product['id']}"): # Key único
                st.session_state.selected_product_id = product['id']
                st.session_state.page = "Productos"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
    
    # CTA final para ver todos los productos
    st.markdown("""
        <div class="cta-banner-final">
            <h3 class="cta-title">¿Listo para transformar tu cabello?</h3>
            <p class="cta-description">Explora nuestra colección completa y encuentra todo lo que necesitas para un cuidado capilar excepcional.</p>
            <a href="#" onclick="parent.postMessage({streamlit: {command: 'SET_PAGE', args: ['Productos']}}, '*')">
                <button class="cta-button">
                    Ver Todos los Productos
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

elif st.session_state.page == "Productos":
    st.markdown("<h1 class='page-title'>Nuestros Productos</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Explora nuestra amplia gama de productos para el cuidado capilar. Cada fórmula ha sido creada para nutrir, fortalecer y realzar la belleza natural de tu cabello.</p>", unsafe_allow_html=True)

    if 'selected_product_id' in st.session_state and st.session_state.selected_product_id:
        selected_product = next((p for p in productos if p['id'] == st.session_state.selected_product_id), None)
        if selected_product:
            st.subheader(f"Detalles de {selected_product['nombre']}")
            col_detail_img, col_detail_info = st.columns([1, 2])
            with col_detail_img:
                if os.path.exists(selected_product['imagen']):
                    st.image(selected_product['imagen'], use_container_width=True)
                else:
                    st.warning("Imagen del producto no encontrada.")
            with col_detail_info:
                st.markdown(f"<h2>{selected_product['nombre']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p class='product-price'>{selected_product['precio']}</p>", unsafe_allow_html=True)
                st.write(selected_product['detalles'])
                st.write(f"Descripción breve: {selected_product['descripcion']}")
                if st.button(f"Añadir al Carrito de {selected_product['nombre']}", key=f"add_detail_{selected_product['id']}"):
                    st.success(f"'{selected_product['nombre']}' añadido al carrito (simulado).")
            st.markdown("<hr>", unsafe_allow_html=True)
            del st.session_state.selected_product_id # Limpia el ID para que no se muestre al recargar
        
    st.subheader("Buscar y Filtrar Productos")
    search_term = st.text_input("Buscar producto:", "").lower()

    cols_per_row = 3

    filtered_products = [
        product for product in productos
        if (search_term in product["nombre"].lower() or search_term in product["descripcion"].lower())
        and os.path.exists(product['imagen'])
    ]

    if not filtered_products:
        st.info("No se encontraron productos que coincidan con su búsqueda.")
    else:
        for i in range(0, len(filtered_products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(filtered_products):
                    product = filtered_products[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                        st.image(product["imagen"], use_container_width=True)
                        st.markdown(f"<h4>{product['nombre']}</h4>", unsafe_allow_html=True)
                        st.write(product["precio"])
                        with st.expander("Ver Detalles"):
                            st.write(product["detalles"])
                            if st.button(f"Añadir al Carrito", key=f"add_{product['id']}"):
                                st.success(f"'{product['nombre']}' añadido al carrito (simulado).")
                        st.markdown("</div>", unsafe_allow_html=True)


elif st.session_state.page == "Novedades":
    st.markdown("<h1 class='page-title'>Novedades y Blog</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Mantente al tanto de los últimos lanzamientos y tendencias en cuidado capilar. ¡Inspírate y cuida tu cabello como se merece!</p>", unsafe_allow_html=True)

    novedades = [
        {"titulo": "Nueva Línea Vegana 'Origen Botánico'", "fecha": "15 de Julio, 2025", "contenido": "Presentamos nuestra nueva línea de productos capilares 100% veganos, libres de crueldad animal y parabenos. Con ingredientes de origen botánico para una experiencia natural y consciente. 🌱 Descubre cómo transformará tu rutina.", "imagen": "images/novedad1.jpg"},
        {"titulo": "Minerva en la Expo Belleza 2025: Un Éxito Total", "fecha": "1 de Julio, 2025", "contenido": "Estuvimos presentes en la Expo Belleza 2025, presentando nuestras innovaciones y recibiendo a cientos de visitantes. ¡Gracias por tu apoyo y entusiasmo! ✨ Revive los momentos destacados.", "imagen": "images/novedad2.jpg"},
        {"titulo": "Guía Completa para un Cabello Saludable en Verano", "fecha": "20 de Junio, 2025", "contenido": "Descubre nuestros tips y productos esenciales para proteger tu cabello del sol, el cloro y la sal durante la temporada de verano. ¡Mantén tu melena radiante y fuerte! ☀️", "imagen": "images/novedad3.jpg"},
    ]

    for novedad in novedades:
        if os.path.exists(novedad["imagen"]):
            st.markdown(f"<div class='news-card'>", unsafe_allow_html=True)
            col_news_img, col_news_content = st.columns([1, 2])
            with col_news_img:
                st.image(novedad["imagen"], use_container_width=True)
            with col_news_content:
                st.markdown(f"<h3>{novedad['titulo']}</h3>", unsafe_allow_html=True)
                st.caption(f"Publicado el: {novedad['fecha']}")
                st.write(novedad["contenido"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)
        else:
            st.warning(f"No se pudo cargar la imagen para la novedad '{novedad['titulo']}'. Asegúrate de que '{novedad['imagen']}' exista en la carpeta 'images'.")


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
                    st.success("¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.")
                else:
                    st.error("Por favor, completa todos los campos para enviar tu mensaje.")
        st.markdown("</div>", unsafe_allow_html=True)

    with contact_col2:
        st.markdown("<div class='contact-info-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Nuestra Información de Contacto</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Minerva Productos Capilares</strong></p>", unsafe_allow_html=True)
        st.markdown("<p>Calle Ficticia 123, San Miguel de Tucumán, Argentina</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Teléfono:</strong> +54 9 381 123-4567</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Email:</strong> <a href='mailto:info@minervaproductoscapilares.com.ar'>info@minervaproductoscapilares.com.ar</a></p>", unsafe_allow_html=True)

        st.markdown("<h3>Horarios de Atención</h3>", unsafe_allow_html=True)
        st.markdown("<p>Lunes a Viernes: 9:00 AM - 6:00 PM</p>", unsafe_allow_html=True)
        st.markdown("<p>Sábados: 9:00 AM - 1:00 PM</p>", unsafe_allow_html=True)
        st.markdown("<p>Domingos y Feriados: Cerrado</p>", unsafe_allow_html=True)
        
        st.markdown("<h3>Síguenos en Redes</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align: left; margin-top: 10px;">
                <a href="https://facebook.com/minervaproductos" target="_blank" style="margin-right: 10px;"><img src="data:image/png;base64,{get_base64_image('images/icon_facebook.png')}" width="30" height="30" alt="Facebook"></a>
                <a href="https://instagram.com/minervaproductos" target="_blank"><img src="data:image/png;base64,{get_base64_image('images/icon_instagram.png')}" width="30" height="30" alt="Instagram"></a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)


elif st.session_state.page == "Sobre Nosotros":
    st.markdown("<h1 class='page-title'>Sobre Minerva Productos Capilares</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Somos una empresa argentina dedicada a la excelencia en el cuidado del cabello, con pasión por la belleza y el bienestar.</p>", unsafe_allow_html=True)

    st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Nuestra Filosofía</h3>", unsafe_allow_html=True)
    st.markdown("""
        <p>En Minerva, creemos que un cabello hermoso es un reflejo de bienestar y confianza. Por eso, nos esforzamos en desarrollar
        productos innovadores que combinan la ciencia y la naturaleza para ofrecer soluciones efectivas para todo tipo de cabello,
        desde los más exigentes hasta los que buscan un cuidado diario.</p>

        <p>Nuestra misión es empoderar a nuestros clientes a través de la confianza que les brinda un cabello sano, fuerte y radiante.
        Trabajamos con pasión y compromiso, utilizando ingredientes de la más alta calidad y procesos de producción
        sostenibles y éticos, cuidando tanto a tu cabello como al planeta.</p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacer-small'></div>", unsafe_allow_html=True)

    st.markdown("<div class='about-section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Nuestros Valores Fundamentales</h3>", unsafe_allow_html=True)
    st.markdown("""
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px;"><strong style="color: #008C82;">✨ Calidad Inquebrantable:</strong> Compromiso con la excelencia en cada formulación.</li>
            <li style="margin-bottom: 10px;"><strong style="color: #008C82;">🔬 Innovación Constante:</strong> Búsqueda y desarrollo de soluciones avanzadas y tecnologías de vanguardia.</li>
            <li style="margin-bottom: 10px;"><strong style="color: #008C82;">🌿 Sostenibilidad y Ética:</strong> Respeto por el medio ambiente y prácticas responsables en toda nuestra cadena de valor.</li>
            <li style="margin-bottom: 10px;"><strong style="color: #008C82;">💖 Pasión por la Belleza:</strong> Amor por lo que hacemos y dedicación al bienestar de tu cabello.</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # --- Sección de Preguntas Frecuentes (FAQ) ---
    st.markdown("<h2 class='section-title'>Preguntas Frecuentes</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-description'>Encuentra respuestas a las preguntas más comunes sobre nuestros productos y servicios.</p>", unsafe_allow_html=True)

    faqs = [
        {"q": "¿Son los productos Minerva aptos para todo tipo de cabello?", "a": "Sí, nuestra línea ha sido cuidadosamente desarrollada para abarcar las necesidades de diversos tipos de cabello, desde seco y dañado hasta graso y con color. Consulta la descripción de cada producto para encontrar el ideal para ti."},
        {"q": "¿Minerva Productos Capilares realiza envíos a todo el país?", "a": "Actualmente realizamos envíos a todo el territorio argentino. Los costos y tiempos de entrega pueden variar según la provincia. Puedes consultar más detalles en nuestra sección de 'Envío y Devoluciones'."},
        {"q": "¿Son los productos de Minerva cruelty-free y sostenibles?", "a": "¡Absolutamente! En Minerva estamos comprometidos con la belleza ética. Nuestros productos son 100% cruelty-free (no testeados en animales) y nos esforzamos por utilizar ingredientes de origen sostenible y envases reciclables siempre que sea posible."},
        {"q": "¿Cómo puedo contactar al servicio al cliente de Minerva?", "a": "Puedes contactarnos a través del formulario en nuestra sección de 'Contacto', enviándonos un email a info@minervaproductoscapilares.com.ar, o llamando a nuestro número de teléfono durante horarios de oficina. ¡Estaremos encantados de ayudarte!"},
        {"q": "¿Minerva ofrece descuentos o programas de fidelidad?", "a": "Sí, ocasionalmente ofrecemos promociones exclusivas y descuentos para nuestros suscriptores. Te recomendamos unirte a nuestro newsletter (formulario al final de la página de Inicio) para recibir todas las novedades y ofertas especiales directamente en tu correo."},
    ]

    st.markdown("<div class='faq-section'>", unsafe_allow_html=True)
    for faq in faqs:
        with st.expander(f"**{faq['q']}**"):
            st.write(faq['a'])
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)


# --- Pie de página ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px; font-size: 0.9em; color: #666666; background-color: #F5F5F5; border-top: 1px solid #eeeeee;">
        <p>&copy; 2025 Minerva Productos Capilares. Todos los derechos reservados.</p>
        <p>Hecho con ❤️ en San Miguel de Tucumán, Argentina.</p>
    </div>
""", unsafe_allow_html=True)