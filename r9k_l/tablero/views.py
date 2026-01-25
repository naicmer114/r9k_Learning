from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Relaciones internas
from .forms import crear_post, responder_post, registro_form, login_form
from .models import posts, respuestas, usuarios

# Librerias externas
from difflib import SequenceMatcher


def global_id_detector():
    id_global = 0  # Declaro el id maximo de la bd del tablon
    # Traigo los datos de BD, guardo la cantidad de registros
    posts_cant = posts.objects.all().count()
    respuestas_cant = respuestas.objects.all().count()
    id_global = (
        posts_cant + respuestas_cant
    )  # Guardo el maximo de registros en BD de tablon
    if id_global == 0:
        id_global = 1
    return id_global  # Devuelvo el maximo de regs


"""
    La primera (first) vista sera para los administradores, \
    por lo que le pasaremos la tabla de los usuarios y las notas.
"""


def index(request):
    if request.method == "GET":
        # Pedimos datos a la vd
        _posts = posts.objects.all()  # Paso los datos de los posts de la BD
        _respuestas = (
            respuestas.objects.all()
        )  # Paso los datos de los respuestas a los posts de la BD

        # Declaramos el contexto que vamos a manejar en este caso. esto incluye datos de bd, forms y cookies del navegador
        CONTEXTO_SERVER = {
            "posts": _posts,  # Paso los posts
            "respuestas": _respuestas,  # Paso las respuestas
            "form_crear_post": crear_post(),  # Paso el formulario para crear posts (abajo su logica)
        }
        # Verifica si las cookies de estado de login y usuario estan presentes
        if "login_status" in request.COOKIES and "username" in request.COOKIES:
            new_data = {
                "username": request.COOKIES["username"],
                "login_status": request.COOKIES["login_status"],
            }
            CONTEXTO_SERVER.update(new_data)  # Se añade al contexto
            # Se devuelve el render
            return render(request, "index.html", CONTEXTO_SERVER)
        else:
            return render(request, "index.html", CONTEXTO_SERVER)

    if request.method == "POST":
        # Solicitamos los posts existentes para posterior uso
        posts_ = posts.objects.all()  # Paso los datos de los posts de la BD
        _usuarios = usuarios.objects.all()  # Se cargan los usuarios para luego
        # Se declara como se tratara el POST del HTML con el formulario de crear POSTS
        form = crear_post(request.POST, request.FILES)
        if form.is_valid():  # Dice el bool del form (si tiene todo lo pedido)
            grado_similaridad = 0

            # Verificamos si el texto tiene similaridades con otros posts
            # Guardamos el texto presente en el formulario
            texto = form.cleaned_data["texto"]

            """
                Declaramos una variable para saber si ya el proceso se hizo o no,
                esto ya que si no hay ningun post existente, el ciclo for no es
                realizado, ya que no tiene nada con que iterar (y por lo tanto
                comparar).
            """
            # listo = 0
            # Revisaremos todos los posts, por lo que usaremos los datos de la BD
            if not posts_.exists():
                post = form.save(commit=False)
                post.id_global = global_id_detector()

                if "login_status" in request.COOKIES and "username" in request.COOKIES:
                    post.autor = request.COOKIES["username"]

                post.save()
                return redirect("/")
            else:
                for post in posts_:
                    if texto == post.texto:  # Si ya existe el post, no se crea
                        print(
                            texto,
                            " Es igual a un post: ",
                            post.id,
                            ", texto:",
                            post.texto,
                        )
                        # listo = 1
                        break
                    """
                        Calculamos el grado de similaridad entre posts, le pasamos a
                        SequenceMatcher el texto nuevo del form y el del posts de BD
                        que estamos comparando. Usamos .ratio() al final para solo
                        quedarnos con el float del grado.
                    """
                    grado_similaridad = SequenceMatcher(None, texto, post.texto).ratio()
                    print(grado_similaridad)
                    """
                        Empleamos un grado por debajo de 0.5 para dejar un espacio
                        logico de posibilidad de posts que usen palabras similares
                        y no sea tan estricto el filtro. 
                    """

                    if grado_similaridad < 0.5:
                        print(" Es considerable o es distinto")
                        post = form.save(commit=False)  # aún NO se guarda en BD
                        print(form.cleaned_data.get("img"))
                        """
                            Si tiene imagen (osea, su url en bd NO se
                            considera la default) entonces se guarda. Caso 
                            contrario no se guarda, y por lo tanto, no se crea el
                            post
                        """
                        if form.cleaned_data.get("img") != "imagenes/default/def.png":
                            post.img = form.cleaned_data["img"]  # Set img
                            post.id_global = global_id_detector()  # Set global_id
                            """
                                Si hay una session iniciada, se toman los datos 
                                del username.
                                Posibilidad de falsificacion al no verificar en bd.
                            """
                            if (
                                "login_status" in request.COOKIES
                                and "username" in request.COOKIES
                            ):
                                # Se guarda como variable el username del cliente
                                usuario_cliente = request.COOKIES["username"]
                                """
                                    Se revisa en la bd para encontrar si hay
                                    un usuario similar, confirmando asi que este
                                    existe.

                                    Sin embargo, es facil de falsificar, luego se 
                                    optara por un encriptado para el cliente
                                """
                                for usuario in _usuarios:
                                    """
                                        Se convierte el usuario de la bd a un
                                        string, ya que la bd devuelve el objeto en
                                        si, y como string si se puede comparar
                                    """
                                    if str(usuario) == usuario_cliente:
                                        """
                                            Si el usuario en la bd coincide con el
                                            del cliente, se guarda en la bd
                                        """
                                        post.autor = usuario_cliente

                            post.save()  # Se guarda el post
                            # listo = 1
                        break
                    else:
                        break

            # Redirijo al inicio real
            return redirect(
                "/"
            )  # Debere cambiar esto luego cuando separe por paginas o no se


def post_base(request, id_post):
    if request.method == "GET":
        _post = posts.objects.get(
            id=id_post
        )  # Paso los datos del post deseado de la BD
        # Me traigo solo las respuestas del post en cuestion
        _respuestas = respuestas.objects.filter(id_post_relacionado=id_post)
        # Se prepara el contexto al servidor
        CONTEXTO_SERVER = {
            "post": _post,  # Paso los posts
            "respuestas": _respuestas,  # Paso las respuestas
            "form_responder_post": responder_post(),  # Paso el formulario para crear posts (abajo su logica)
        }
        # Verifica si las cookies de estado de login y usuario estan presentes
        if "login_status" in request.COOKIES and "username" in request.COOKIES:
            # De estar, se preparan los nuevos datos de cookies
            new_data = {
                "username": request.COOKIES["username"],
                "login_status": request.COOKIES["login_status"],
            }
            CONTEXTO_SERVER.update(new_data)  # Se añade al contexto
        # Se devuelve el render
        return render(
            request,
            "post_base.html",
            CONTEXTO_SERVER,
        )

    if request.method == "POST":
        _usuarios = usuarios.objects.all()  # Se cargan los usuarios para luego
        # Se declara el como se actuara al realzizar un 'protocolo' POST en HTML. En este caso para responder un post
        # print(global_id_detector())
        form = responder_post(request.POST, request.FILES)
        if form.is_valid():
            # Guardamos el texto presente en el formulario
            respuesta = form.save(commit=False)  # aún NO se guarda en BD:
            respuesta.img = form.cleaned_data["img"]  # especificamos la imagen
            respuesta.id_post_relacionado_id = id_post  # relacionamos al post
            respuesta.id_global = global_id_detector()  # Set global_id
            """
                Si hay una session iniciada, se toman los datos 
                del username.
                Posibilidad de falsificacion al no verificar en bd.
            """
            if "login_status" in request.COOKIES and "username" in request.COOKIES:
                # Se guarda como variable el username del cliente
                usuario_cliente = request.COOKIES["username"]
                """
                    Se revisa en la bd para encontrar si hay
                    un usuario similar, confirmando asi que este
                    existe.

                    Sin embargo, es facil de falsificar, luego se 
                    optara por un encriptado para el cliente
                """
                for usuario in _usuarios:
                    """
                        Se convierte el usuario de la bd a un
                        string, ya que la bd devuelve el objeto en
                        si, y como string si se puede comparar
                    """
                    if str(usuario) == usuario_cliente:
                        """
                            Si el usuario en la bd coincide con el
                            del cliente, se guarda en la bd
                        """
                        respuesta.autor = usuario_cliente

            respuesta.save()  # Se guarda  la espuesta
            # El segundo dato depende del id del post seleccionando, pudiendo asi relacionar las respuestas con el post asociado
            return redirect(
                "./" + str(id_post)
            )  # Al redirjir tomo la base del url y le agrego el id de nuvo (Misma logica con la que llego al post)
    else:
        pass


def registro(request):
    # Si se pide datos al servidor, se les devuelven
    if request.method == "GET":
        return render(
            request,
            "registro.html",
            {
                "form_registro": registro_form(),
            },
        )

    if request.method == "POST":
        # Pido todos los usuarios (todo menos optimizar)
        _usuarios = usuarios.objects.all()
        # Se declara el formulario enviado
        form = registro_form(request.POST)
        # Solo se procesa si cumple los campos y requisitos
        if form.is_valid():
            # Se guardan en variables temporales el usuario y contraseña
            username = form.cleaned_data["username"]

            # Verificamos si el usuario ya existe (puede haber dos usuarios distintos con misma contraseña, pero no al reves)
            no_es_similar = True
            """
                Si hay un usuario similar en la BD, cambiamos el estado de
                similaridad a falso, el negado de NO estar similar, 
                es, estarlo 
            """
            for usuario in _usuarios:
                if username == usuario.username:
                    no_es_similar = False
            # Si el usuario no es similar a alguno en la BD, procesamos mas
            if no_es_similar:
                passwd = form.cleaned_data["password_first"]
                # Se crea el registro en la BD
                usuarios.objects.create(
                    username=username,
                    passwd=passwd,
                )
                # POR AHORA SOLO SE REDIRECCIONA AL HOME SI HAY SIMILITUDES
                return redirect("/")
            else:
                # POR AHORA SOLO SE REDIRECCIONA AL HOME SI HAY SIMILITUDES
                return redirect("/")
        pass


def login(request):
    if request.method == "GET":
        return render(
            request,
            "login.html",
            {
                "form_login": login_form(),
            },
        )
        pass

    if request.method == "POST":
        # Pido todos los usuarios (todo menos optimizar)
        _usuarios = usuarios.objects.all()
        # Se declara el formulario enviado
        form = login_form(request.POST)
        # Solo se procesa si cumple los campos y requisitos
        if form.is_valid():
            # Se guardan en variables temporales el usuario y contraseña
            username = form.cleaned_data["username"]
            passwd = form.cleaned_data["password_first"]
            """
                Se revisan todos los nombres de usuario de la vd buscando
                similitudes con los presentes en el formulario.

                Si se consigue un usuario similar, se procede a comprar ahora
                si, la contraseña, y si esta coincide tambien, se da inicio
                al login.
            """
            for usuario in _usuarios:
                if username == usuario.username:
                    if passwd == usuario.passwd:
                        # Declaro el formato del contexto para preparar la respuesta
                        CONTEXTO_SERVER = {
                            "username": username,
                            "login_status": True,
                        }
                        # Declaro la respuesta
                        respuesta = redirect("/", CONTEXTO_SERVER)
                        """
                            Declaro como cookies el username y login_status
                            para guardarlos localmente (como cookie po)
                        """
                        respuesta.set_cookie("username", username)
                        respuesta.set_cookie("login_status", True)
                        # Devuelvo la respuesta ya procesada
                        return respuesta
            # POR AHORA SOLO SE REDIRECCIONA AL HOME SI NO HAY SIMILITUDES
            return redirect("/")


def logout(request):
    respuesta = HttpResponseRedirect("login")
    # Se eliminan las cookies que habian
    respuesta.delete_cookie("username")
    respuesta.delete_cookie("login_status")
    return respuesta
