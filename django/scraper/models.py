from django.db import models

# Create your models here.
class Noticia(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=250)
    bajada = models.TextField()
    cuerpo = models.TextField()
    fecha = models.DateField(blank=True, null=True)
    categoria = models.ManyToManyField("Categoria") #salud, medio ambiente, educacion, cultura
    institucion = models.ForeignKey('Institucion', default=None, on_delete=models.PROTECT) # seremi salud, universidad upla, mineduc
    estado = models.ForeignKey('Estado', default=None, on_delete=models.PROTECT) #disponible, publicada
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "noticia"
        verbose_name_plural = "noticias"
        ordering = ["-fecha"]
    
    def __str__(self):
        return self.titulo

class Categoria(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["-nombre"]
    
    def __str__(self):
        return self.nombre

class Institucion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)#gubernamental, prensa digital, noticia universitaria
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "institución"
        verbose_name_plural = "instituciones"
        ordering = ["-nombre"]
    
    def __str__(self):
        return self.nombre

class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "estado"
        verbose_name_plural = "estados"
        ordering = ["-nombre"]
    
    def __str__(self):
        return self.nombre