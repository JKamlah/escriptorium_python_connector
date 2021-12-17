# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func("Hello ")
#         print("Something is happening after the function is called.")

#     return wrapper


# @my_decorator
# def say_whee(msg: str=""):
#     print(msg + "Whee!")


# say_whee()

class Dest(object):
    def __init__(self):
        self.m = "this obj"
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Just about to destroy {self.m}")
        
    @property
    def msg(self):
        return self.m

with Dest() as d:
    print(d.msg)

print("done")