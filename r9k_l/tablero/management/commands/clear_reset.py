from django.core.management.base import BaseCommand
from django.db import connection

from datetime import date
from difflib import SequenceMatcher
from time import sleep

from tablero.models import posts


class Command(BaseCommand):
    help = "Limpia posts y respuestas y reinicia sus IDs"

    def handle(self, *args, **options):
        while True:
            """
                Traemos el ultimo id presente en la bd por parte de los posts,
                ya que de ellos nace todo lo demas.

                La ventaja de usar .first() es que nos traera el ultimo ultimo,
                no necesariamente el 1, porque imagina que ese post esta
                eliminado por x o y, entonces trae el 2, y si no el 3, y asi.
            """
            try:
                id_last_post = posts.objects.first().id
                # Buscamos la informacion del post mas antiguo
                _post = posts.objects.get(id=id_last_post)
                """
                    Guardamos la fecha del post mas antiguo y:

                    1) La primera accion se guardara como un string
                    
                    2) Traemos la fecha publicada del post mas antiguo

                    3) Se divide la fecha por espacios

                    4) Se toma solo el primer dato de la fecha, osea: año mes dia

                                    1            2              3        4
                                    ↓            ↓              ↓        ↓
                """
                fecha_mas_antigua = str(_post.fecha_publicado).split(" ")[0]

                # Guardamos la fecha del sistema en formato Año Mes Dia
                fecha_del_sistema = str(date.today())
                print(fecha_mas_antigua)
                print(fecha_del_sistema)
                """
                    Empleando la misma logica del "id_global" en posts y
                    respuestas, en este caso como solo tomamos el año, mes y dia, y
                    solo toleraremos por debajo a 1.
                    
                    Ya que mientras sea el mismo dia, el ratio()de este
                    SequenceMatcher sera 1, pero si es por debajo de el, ya es, o,
                    un dia, mes o año distinto.
                """
                grado_similaridad = SequenceMatcher(
                    None, fecha_mas_antigua, fecha_del_sistema
                ).ratio()

                if grado_similaridad < 1:
                    """
                        Empleando el modulo .cursor() de connection, abreviamos
                        esta funcion a solo "cursor", en este caso cursor es usado
                        para la ejecucion de query de base de datos a pelo
                        (osea, el query literal). 
                    """
                    with connection.cursor() as cursor:
                        # Declaramos el tipo de  base de datos que emplearemos
                        vendor = connection.vendor
                        # Mostramos un mensaje para que quede registro
                        self.stdout.write(f"Base de datos detectada: {vendor}")
                        # Y solo procedemos SI nuestra base de datos es sqlite
                        # evitando asi malas ejecuciones
                        if vendor == "sqlite":
                            """
                                Se limpia la tabla de respuestas, primero las 
                                respuestas, ya que estan ligadas a posts. Evitando
                                asi cualquier inconveniente (aunque estas esten 
                                declaradas como "on_delete=models.CASCADE" en el
                                models.py)
                            """
                            cursor.execute("DELETE FROM tablero_respuestas;")
                            # Se reinicia la indexacion (id) de la tabla respuestas
                            cursor.execute(
                                "DELETE FROM sqlite_sequence WHERE name='tablero_respuestas';"
                            )
                            # Se limpia la tabla de posts
                            cursor.execute("DELETE FROM tablero_posts;")
                            # Se reinicia la indexacion (id) de la tabla posts
                            cursor.execute(
                                "DELETE FROM sqlite_sequence WHERE name='tablero_posts';"
                            )
                        self.stdout.write(
                            self.style.WARNING(
                                "Posts y respuestas eliminados, IDs reiniciados"
                            )
                        )
            # En caso de algun error, lo mostramos
            except Exception as e:
                # Siendo el errror mas probable, lo destacamos
                print("Probablente no hay posts")
                self.stdout.write(
                    self.style.NOTICE("Error: \n\n") + self.style.WARNING(e)
                )
            # (usando time) Se pausa el bucle por 30 minutos (o 1800 segundos)
            sleep(1800)
