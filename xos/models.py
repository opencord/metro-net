from header import *



#from core.models.tenant import Tenant
from core.models import Tenant





















class EnterpriseLocation(Tenant):

  KIND = "metronetwork"

  class Meta:
      app_label = "metronet"
      name = "metronet"
      verbose_name = "Enterprise Localation"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  cord_site_ip = CharField( help_text = "ip of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_ip = CharField( help_text = "ip of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_port = IntegerField( help_text = "port of the local site", max_length = 256, null = False, db_index = False, blank = False )
  cord_site_username = CharField( help_text = "username of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_password = CharField( help_text = "password of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_type = CharField( default = "xos", choices = "(('onos', 'ONOS'), ('xos', 'XOS')", max_length = 64, blank = False, null = False, db_index = False )
  

  # Relations
  

  
  pass




class OnosModel(PlCoreBase):

  KIND = "metronetwork"

  class Meta:
      app_label = "metronet"
      name = "metronet"
      verbose_name = "Open Netowrk Operating System"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  onos_ip = CharField( help_text = "ip of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_port = IntegerField( help_text = "port of the transport manager", max_length = 256, null = False, db_index = False, blank = False )
  onos_username = CharField( help_text = "username of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_password = CharField( help_text = "password of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_type = CharField( default = "local", choices = "(('local', 'Local'), ('global', 'Global')", max_length = 64, blank = False, null = False, db_index = False )
  

  # Relations
  

  
  pass




class UserNetworkInterface(PlCoreBase):

  KIND = "metronetwork"

  class Meta:
      app_label = "metronet"
      name = "metronet"
      verbose_name = "User Network Interface"

  # Primitive Fields (Not Relations)
  tenant = CharField( help_text = "tenat name", max_length = 256, null = False, db_index = False, blank = False )
  cpe_id = CharField( blank = False, max_length = 1024, null = False, db_index = False )
  latlng = CharField( help_text = "location, i.e. [37.773972, -122.431297]", max_length = 256, null = False, db_index = False, blank = False )
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  
  def save(self, *args, **kwargs):
  
      if self.latlng:
          try:
              latlng_value = getattr(self, 'latlng').strip()
              if (latlng_value.startswith('[') and latlng_value.endswith(']') and latlng_value.index(',') > 0):
                  lat = latlng_value[1: latlng_value.index(',')].strip()
                  lng = latlng_value[latlng_value.index(',') + 1: len(latlng_value) - 1].strip()
  
                  # If lat and lng are not floats, the code below should result in an error.
                  lat_validation = float(lat)
                  lng_validation = float(lng)
              else:
                  raise ValueError("The lat/lng value is not formatted correctly.")
          except:
              raise ValueError("The lat/lng value is not formatted correctly.")
  
      super(UserNetworkInterface, self).save(*args, **kwargs)
  pass




class BandwidthProfile(PlCoreBase):

  KIND = "metronetwork"

  class Meta:
      app_label = "metronet"
      name = "metronet"
      verbose_name = "Bandwidth Profile"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  cbs = IntegerField( help_text = "committed burst size", null = False, blank = False, db_index = False )
  ebs = IntegerField( help_text = "expected burst size", null = False, blank = False, db_index = False )
  cir = IntegerField( help_text = "committed information rate", null = False, blank = False, db_index = False )
  eir = IntegerField( help_text = "expected information rate", null = False, blank = False, db_index = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  pass




class ELine(PlCoreBase):

  KIND = "metronetwork"

  class Meta:
      app_label = "metronet"
      name = "metronet"
      verbose_name = "Ethernet Virtual Private Line"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  connect_point_1_id = CharField( blank = False, max_length = 256, null = False, db_index = False )
  connect_point_2_id = CharField( blank = False, max_length = 64, null = False, db_index = False )
  vlanids = TextField( help_text = "comma separated list of vlanIds", null = False, blank = False, db_index = False )
  cord_site_username = CharField( blank = False, max_length = 64, null = False, db_index = False )
  bwp = CharField( help_text = "bandwidth profile name", max_length = 256, null = False, db_index = False, blank = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  pass


