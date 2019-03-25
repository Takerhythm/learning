from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool as BasePool


class Pool(BasePool):
    def apply_async(self,func, args=(), kwargs={}, callback=None, error_callback=None):
        return super().apply_async(func, args, kwargs, callback=callback)

    def close(self):
        pass