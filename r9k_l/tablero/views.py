from django.shortcuts import render, redirect

# Relaciones internas
from .forms import crear_post, responder_post
from .models import posts, respuestas

# Librerias externas
from difflib import SequenceMatcher

def global_id_detector():
    id_global=0 #Declaro el id maximo de la bd del tablon
    #Traigo los datos de BD, guardo la cantidad de registros
    posts_cant=posts.objects.all().count()
    respuestas_cant=respuestas.objects.all().count()
    id_global= posts_cant + respuestas_cant #Guardo el maximo de registros en BD de tablon
    if id_global == 0: id_global = 1
    return id_global # Devuelvo el maximo de regs
    

'''
    La primera (first) vista sera para los administradores, \
    por lo que le pasaremos la tabla de los usuarios y las notas.
'''
def index(request):

    if request.method == 'GET':
        _posts = posts.objects.all() #Paso los datos de los posts de la BD
        _respuestas = respuestas.objects.all() #Paso los datos de los respuestas a los posts de la BD
        return render(request, 'index.html',{
            'posts': _posts, #Paso los posts
            'respuestas': _respuestas, #Paso las respuestas
            'form_crear_post': crear_post(), #Paso el formulario para crear posts (abajo su logica)
            }
        )

    if request.method == 'POST':
        #Solicitamos los posts existentes para posterior uso
        posts_ = posts.objects.all() #Paso los datos de los posts de la BD

        #Se declara como se tratara el POST del HTML con el formulario de crear POSTS
        form = crear_post(request.POST, request.FILES)
        print(form.is_valid()) #Dice el bool del form (si tiene todo lo pedido)
        grado_similaridad = 0

        #Verificamos si el texto tiene similaridades con otros posts
        #Guardamos el texto presente en el formulario
        texto = form.cleaned_data['texto']
        
        '''
            Declaramos una variable para saber si ya el proceso se hizo o no,
            esto ya que si no hay ningun post existente, el ciclo for no es
            realizado, ya que no tiene nada con que iterar (y por lo tanto
            comparar).
        ''' 
        listo=0
        #Revisaremos todos los posts, por lo que usaremos los datos de la BD
        for post in posts_:
            if texto == post.texto: # Si ya existe el post, no se crea 
                print(texto, " Es igual a un post: ", post.id, ", texto:", post.texto)
                listo=1
                break
            '''
                Calculamos el grado de similaridad entre posts, le pasamos a
                SequenceMatcher el texto nuevo del form y el del posts de BD
                que estamos comparando. Usamos .ratio() al final para solo
                quedarnos con el float del grado.
            ''' 
            grado_similaridad = SequenceMatcher(None, texto, post.texto).ratio()
            print(grado_similaridad)
            '''
                Empleamos un grado por debajo de 0.5 para dejar un espacio
                logico de posibilidad de posts que usen palabras similares
                y no sea tan estricto el filtro. 
            '''
            
            if grado_similaridad < 0.5:
                print(" Es considerable o es distinto")
                posts.objects.create( # Se guarda en la BD, en la tabla acorde
                                texto=texto, id_global=global_id_detector(),
                            )
                listo=1
                break
            else:
                break
        if listo==0:
            posts.objects.create( # Se guarda en la BD, en la tabla acorde
                                texto=texto, id_global=global_id_detector(),
                            )

        #Redirijo al inicio real
        return redirect('/') #Debere cambiar esto luego cuando separe por paginas o no se
          
def post_base(request, id_post):
    
    if request.method == 'GET':
        post_ = posts.objects.get(id=id_post) #Paso los datos del post deseado de la BD
        #Me traigo solo las respuestas del post en cuestion
        respuestas_ = respuestas.objects.filter(id_post_relacionado=id_post)
        
        return render(request, 'post_base.html',{
                'id_post': id_post, #Envio el id del post para futuro uso. 26/12/2025 no tengo uso aun
                'post': post_, #Mando el texto original del post seleccionado
                'respuestas': respuestas_, #Envio las respuestas correspondientes al post
                'form_responder_post': responder_post(), #Envio el formulario para responder a los posts (abajo su logica)
        })

    if request.method == 'POST':
        # Se declara el como se actuara al realzizar un 'protocolo' POST en HTML. En este caso para responder un post
        #print(global_id_detector())
        form = responder_post(request.POST, request.FILES)
        print(form.is_valid())
        #Guardamos el texto presente en el formulario
        texto = form.cleaned_data['texto']
        respuestas.objects.create(
                                    texto=texto,
                                    id_post_relacionado_id=id_post,
                                    id_global = global_id_detector(),
                                 ) #El segundo dato depende del id del post seleccionando, pudiendo asi relacionar las respuestas con el post asociado
        return redirect('./'+str(id_post)) #Al redirjir tomo la base del url y le agrego el id de nuvo (Misma logica con la que llego al post)
    else:
        pass