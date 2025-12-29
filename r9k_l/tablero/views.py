from django.shortcuts import render, redirect

from .forms import crear_post, responder_post
from .models import posts, respuestas
'''
    La primera (first) vista sera para los administradores, \
    por lo que le pasaremos la tabla de los usuarios y las notas.
'''
def index(request):
    posts_ = posts.objects.all() #Paso los datos de los posts de la BD
    respuestas_ = respuestas.objects.all() #Paso los datos de los respuestas a los posts de la BD
    if request.method == 'GET':
        return render(request, 'index.html',{
            'posts': posts_, #Paso los posts
            'respuestas': respuestas_, #Paso las respuestas
            'form_crear_post': crear_post(), #Paso el formulario para crear posts (abajo su logica)
            }
        )
    else:
        #Se declara como se tratara el POST del HTML con el formulario de crear POSTS
        posts.objects.create(texto=request.POST['texto'])
        #Redirijo al inicio real
        return redirect('/') #Debere cambiar esto luego cuando separe por paginas o no se

def post_base(request, id_post):
    post_ = posts.objects.get(id=id_post) #Paso los datos del post deseado de la BD
    
    #Solo quiero quedarme con las respuestas correspondientes al post que se esta viendo
    respuestas_all = respuestas.objects.all() #Cargo todas las respuestas habidas en la BD
    repuestas_coincidentes = [] #Uso una lista para guardar las respuestas que me interesan
    for respuestas_lectura in respuestas_all:
        print(respuestas_lectura.texto)
        print(respuestas_lectura.id_post_relacionado.id)   
        if respuestas_lectura.id_post_relacionado.id == id_post: #Es foraneo, se trae con ruta completa
            repuestas_coincidentes.append(respuestas_lectura.texto+ ' '+ str(respuestas_lectura.hora_creada)) #Se empaqueta las respuestas correspondientes al post.        Por hora lo mandare junto
    print(repuestas_coincidentes)

    if request.method == 'GET':
        return render(request, 'post_base.html',{
                'id_post': id_post, #Envio el id del post para futuro uso. 26/12/2025 no tengo uso aun
                'post': post_, #Mando el texto original del post seleccionado
                'respuestas': repuestas_coincidentes, #Envio las respuestas correspondientes al post
                'form_responder_post': responder_post(), #Envio el formulario para responder a los posts (abajo su logica)
        })
    else:
        # Se declara el como se actuara al realzizar un 'protocolo' POST en HTML. En este caso para responder un post
        respuestas.objects.create(texto=request.POST['texto'], id_post_relacionado_id=id_post) #El segundo dato depende del id del post seleccionando, pudiendo asi relacionar las respuestas con el post asociado
        return redirect('./'+str(id_post)) #Al redirjir tomo la base del url y le agrego el id de nuvo (Misma logica con la que llego al post)