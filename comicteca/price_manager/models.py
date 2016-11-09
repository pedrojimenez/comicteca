from django.db import models


# ------------------------------------------------------------------ #
#
#                         Artist Model
#
# ------------------------------------------------------------------ #
class PriceField(models.Model):
    """Price model."""

    EURO_PTAS_EXCHANGE_RATE = 166.386
    EURO_DOLLARS_EXCHANGE_RATE = 1
    EURO_POUNDS_EXCHANGE_RATE = 1

    CURRENCY_TYPES = (
        ('EUROS', 'euros'),
        ('PESETAS', 'ptas'),
        ('DOLLARS', 'dollars'),
        ('POUNDS', 'pounds'),
    )
    _amount = models.FloatField(default=0)
    _unit = models.CharField(max_length=128, default='EUROS')

    def __init__(self, amount=0, unit='EUROS'):
        """."""
        self._amount = float(amount)
        self._unit = unit

    def __unicode__(self):
        """str/unicode function of PriceManager class."""
        return str(self.amount(self._unit)) + ' ' + str(self._unit)

    def amount(self, unit='EUROS'):
        """Return the amount of price in thr desired unit."""
        if unit == self._unit:
            return self._amount

        return self.__convert_to(unit)

    def __convert_to(self, unit):
        """Convert the amount(self) into selected unit."""
        # TODO: convert to all possible units by downloading the EX_rates
        if unit == 'EUROS':
            if self._unit == 'PESETAS':
                return round(self._amount / self.EURO_PTAS_EXCHANGE_RATE, 2)

            elif self._unit == 'DOLLARS':
                return round(self._amount / self.EURO_DOLLARS_EXCHANGE_RATE, 2)

            elif self._unit == 'POUNDS':
                return round(self._amount / self.EURO_POUNDS_EXCHANGE_RATE, 2)

        elif unit == 'PESETAS':
            if self._unit == 'EUROS':
                return round(self._amount * self.EURO_PTAS_EXCHANGE_RATE, 2)

        else:
            return round(
                float(self._amount), 2)
