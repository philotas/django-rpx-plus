from django.db import models
from picklefield.fields import PickledObjectField

class RpxData(models.Model):
    """holds bonus info about the user
    some of this this could alternately be implemented by using the rpx
    mapping api. but that requires more network traffic and still doesn't
    provide a place to stash all the user metadata.
    """
    #Below could be a foreignKey if we wish to associate many profiles with the
    #user. hm.
    user = models.ForeignKey("auth.User")

    #Why should these fields be hard-coded? Putting all extra data into
    #a serialized field.
    #profile_pic_url = models.URLField(blank=True, verify_exists=False)
    #info_page_url = models.URLField(blank=True, verify_exists=False)

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
        return u"RpxUserData for %s" % self.user.username
        
