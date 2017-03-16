class AppendOnlyError(Exception):
    pass


class AppendOnlyModelMixin(object):
    def save(self, *args, **kwargs):
        if self.pk:
            raise AppendOnlyError(
                'The Job table is append only. '
                'To "edit" a row, create a new row with an incremented rev.')
        super(AppendOnlyModelMixin, self).save(*args, **kwargs)
