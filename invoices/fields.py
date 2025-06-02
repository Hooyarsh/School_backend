from rest_framework import serializers
import jdatetime

class JalaliDateField(serializers.DateField):
    def to_internal_value(self, value):
        print('JalaliDateField received:', value)
        if isinstance(value, str):
            value = value.replace('/', '-')
            try:
                jy, jm, jd = map(int, value.split('-'))
                gdate = jdatetime.date(jy, jm, jd).togregorian()
                return gdate
            except Exception:
                pass
        return super().to_internal_value(value)