from django.db import models

EXCELLENT= "excellent"
VERY_GOOD= "very_good"
GOOD="good"
FAIR="fair"

x = (
    (EXCELLENT, "Excellent"),
    (VERY_GOOD, "Very Good"),
    (GOOD, "Good"),
    (FAIR, "Fair"),

)

class Sf12ModelMixin(models.Model):

    """Version ?"""

    x = models.CharField(
        verbose_name="In general, would you say your health is",
        choices=
    )
