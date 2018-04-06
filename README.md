# choices.py

choices.py is a wrapper around Django's choices to make them easier to use.

## Example

```py
from django.db import models

from choices import Choices


class Student(models.Model):

    class Year(Choices):

        FRESHMAN = 'FR'
        SOPHOMORE = 'SO'
        JUNIOR = 'JR'
        SENIOR = 'SR'

        @property
        def is_upperclass(self):
            return self in (self.JUNIOR, self.SENIOR)

    year_in_school = models.CharField(
        max_length=2, choices=Year.choices(), default=Year.FRESHMAN.value)

    def is_upperclass(self):
        return self.Year(self.year_in_school).is_upperclass
```

## Installing

Install it from [PyPI](https://pypi.org/project/choices.py/) with pip:

```
pip install choices.py
```

**Requirements:**
- Python 3.4+
