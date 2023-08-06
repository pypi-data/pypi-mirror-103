from . import BlobCache,exceptions

class Sigstring:
    """
    Create a consistent string representation of a function signature.
    Used in the cache decorator.
    """
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        args = "_".join([str(a) for a in self.args])
        kwargs = "_".join([f"{k}-{v}" for k,v in self.kwargs.items()])
        return "~".join((args,kwargs))

    def sig(self):
        return self.args,self.kwargs

def cache(blob_cache:BlobCache):
    """
    Wrap a function, caching its results using a BlobCache instance.
    """
    def wrapper(fn):
        key = lambda *args,**kwargs: fn.__name__ + str(Sigstring(*args,**kwargs))
        def inner(*args,**kwargs):
            try:
                result = blob_cache[key(*args,**kwargs)]
            except exceptions.NotCached:
                result = fn(*args,**kwargs)
                blob_cache[key(*args,**kwargs)] = result
            return result
        return inner
    return wrapper 
