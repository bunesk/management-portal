from django.db import models

class Licence(models.Model):
    """
    The model 'Licence' is the permission to use a software module of a software product.
    The licence also represents the used software module and has a 

    Attributes:
    key              (str)      : The licence key
    detail           (str)      : The detailed information about the licence
    start_date       (datetime) : The start date of the licence
    end_date         (datetime) : The end date of the licence
    software_version (str)      : The version of the software product used with this licence
    module           (int)      : Foreign key for the software module the licence is for
    location         (int)      : Foreign key for the customer's location which uses the licence
    """
    key              = models.CharField(max_length = 255)
    detail           = models.CharField(max_length = 2047)
    start_date       = models.DateTimeField(auto_now_add = True)
    end_date         = models.DateTimeField()
    software_version = models.CharField(max_length=16)
    module           = models.ForeignKey(
        to                  = 'SoftwareModule',
        on_delete           = models.CASCADE,
        related_name        = 'licences',
        related_query_name  = 'licence',
        null                = False,
    )
    location         = models.ForeignKey(
        to                  = 'customers.Location',
        on_delete           = models.CASCADE,
        related_name        = 'licences',
        related_query_name  = 'licence',
        null                = False,
    )

class SoftwareProduct(models.Model):
    """
    The model 'SoftwareProduct' is a software product which can be used by many customers.
    It has multiple software modules.

    Attributes:
    name     (str): The name of the software product
    category (str): The category the software product belongs to
    version  (str): The current version of the software product
    """
    name     = models.CharField(max_length = 64)
    category = models.CharField(max_length = 64)
    version  = models.CharField(max_length = 16)

class SoftwareModule(models.Model):
    """
    The model 'SoftwareModule' is a part of a software product.
    It has multiple licences.

    Attributes:
    name    (str): The name of the software module
    version (str): The current version of the software module
    product (int): Foreign key to the software product the module belongs to
    """
    name    = models.CharField(max_length = 127)
    version = models.CharField(max_length = 16)
    product = models.ForeignKey(
        to                  = 'SoftwareProduct',
        on_delete           = models.CASCADE,
        related_name        = 'modules',
        related_query_name  = 'module',
        null                = False,
    )