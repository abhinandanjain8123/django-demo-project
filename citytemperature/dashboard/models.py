from django.db import models

class City(models.Model):
	city_name = models.CharField(max_length=15)

	def __str__(self):
		return self.city_name

class Temperature(models.Model):
	city = models.ForeignKey(City,on_delete=models.CASCADE)
	year = models.IntegerField()
	temperature = models.IntegerField()

	def __str__(self):
		return str(self.year)


	


