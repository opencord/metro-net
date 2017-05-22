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
