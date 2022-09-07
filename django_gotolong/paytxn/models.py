from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PayTxn(models.Model):
    pt_made_by = models.ForeignKey(User, related_name='transactions',
                                   on_delete=models.CASCADE)
    pt_made_on = models.DateTimeField(auto_now_add=True)
    pt_amount = models.IntegerField()
    pt_order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    pt_checksum = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = u'global_paytxn'

    def save(self, *args, **kwargs):
        if self.pt_order_id is None and self.pt_made_on and self.id:
            self.pt_order_id = self.pt_made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
