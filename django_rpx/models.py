from django.db import models
from picklefield.fields import PickledObjectField

class RpxData(models.Model):
    #The User field can be null if the user has logged in but did not 
    #register an account (thus creating aan associated User object).
    user = models.ForeignKey('auth.User', null = True)

    #Flag that specifies whether the Rpx login has been associated with a User
    #yet. It is used, in conjunction with User.is_active = False, to redirect
    #the user to a 'register' page.
    #TODO: Don't need this anymore.
    #is_associated = models.BooleanField(default = False)

    #Maybe we should go back to using TextField for identifier? We are
    #assuming that it'll always be a URL...
    identifier = models.URLField(unique = True, verify_exists = False,
                                 max_length = 255)
    provider = models.CharField(max_length = 255)
    
    #Since the profile can contain any number of fields and since this
    #information is rarely accessed anyway, we'll just pickle the DICTIONARY
    #and store it in db.
    profile = PickledObjectField()

    # class Admin:
    #     list_display = ('',)
    #     search_fields = ('',)

    def __unicode__(self):
        return u"RPX identifier is %s" % self.identifier
        
