# Decorator is a function that adds behavior to a function without modifying the function itself
# https://www.youtube.com/watch?v=U-G-mSd4KAE


# Func 1: the decorator function that takes a function as an argument and returns a new function that adds behavior to the original function
def add_sprinkles(func):
    def wrapper(): # inner function that takes the same arguments as the original function
        func()
    return wrapper

@add_sprinkles
def get_ice_cream():
    print(f"Here is your ice cream 🍨")

# Como o decorator não faz nada, ele só printa a mensagem original:
get_ice_cream()

##################################

def add_sprinkles(func): # Recebe a função original como argumento
    def wrapper(): # Só é chamado quando a função decorada é chamada (get_ice_cream())
        print("*You add sprinkles 🎊*")
        func() #Chama a função original (get_ice_cream())
    return wrapper

def add_fudge(func):
    def wrapper():
        print("*You add fudge 🍫*")
        func()
    return wrapper

@add_sprinkles
@add_fudge
def get_ice_cream():
    print(f"Here is your ice cream 🍨")

get_ice_cream()

##################################

# Se eu preciso passar argumentos para a função original, eu preciso passar os mesmos argumentos para a função wrapper:
def add_sprinkles(func):
    def wrapper(*args, **kwargs): # a wrapper tem que receber os argumentos da função original
        print("*You add sprinkles 🎊*")
        func(*args, **kwargs)
    return wrapper

def add_fudge(func):
    def wrapper(*args, **kwargs): # args e kwargs permite que ele receba qualquer função com qualquer numero de argumentos
        print("*You add fudge 🍫*")
        func(*args, **kwargs)
    return wrapper

@add_sprinkles
@add_fudge
def get_ice_cream(flavor):
    print(f"Here is your {flavor} ice cream 🍨")

get_ice_cream("vanilla") # um argumento
