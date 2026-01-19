from django.db import models

'''
    Creamos el modelo de los usuarios registrados en el sistema, \
    nos valandremos de una verificacion de si estan o no activos, \
    no estarlo significaria que han inclumplido las normas en la \
    plataforma, tendran un contador de baneos para posteriomente \
    eliminarlos de la plataforma tras tener 3 baneos. Ah y \
    razones de baneo, posteriomente seran usadas para des-baneos\
    y distintas acciones por parte de los administradores.
'''
class usuarios(models.Model):
    propietario=models.CharField(max_length=128)
    activo=models.BooleanField(default=True)
    ban_razon=models.TextField(default="Sin novedad", null=True)
    ban_count=models.IntegerField(default=0)

    def __str__(self):
        return self.propietario
    pass
'''
    Y en este modelo tendremos las anotaciones de todos los usuarios,\
    solo nos valdremos del id del propietario, el texto de la nota \
    y la hora de cuando fue creada, luego se le añaderan mas metadatos.
'''
class posts(models.Model):
    texto=models.TextField()
    hora_creada=models.TimeField(auto_now=True,)
    pass

class respuestas(models.Model):
    id_post_relacionado=models.ForeignKey(posts,on_delete=models.CASCADE)
    texto=models.TextField()
    hora_creada=models.TimeField(auto_now=True,)
    pass