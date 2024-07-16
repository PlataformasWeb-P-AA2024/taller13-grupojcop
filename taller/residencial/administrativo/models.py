from django.db import models

class Edificio(models.Model):
    opciones_tipo_barrio = (
        ('residencial', 'Edificio Residencial'),
        ('comercial', 'Edificio Comercial'),
    )
    
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30, choices=opciones_tipo_barrio)

    def __str__(self):
        return "%s %s %s %s" % (self.nombre, self.direccion, self.ciudad, self.tipo)
    
    def total_cuartos(self):
        return sum(departamento.numero_cuartos for departamento in self.departamentos.all())

    def costo_total_departamentos(self):
        return sum(departamento.costo_departamento for departamento in self.departamentos.all())

class Departamento(models.Model):
    nombre_completo_propietario = models.CharField(max_length=100)
    costo_departamento = models.FloatField()
    numero_cuartos = models.IntegerField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="departamentos")

    def __str__(self):
        return "%s %.2f %d" % (self.nombre_completo_propietario, self.costo_departamento, self.numero_cuartos)
