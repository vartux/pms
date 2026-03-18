import json

def load_config():
    with open("config.json","r") as file:
        config = json.load(file)
    
    return config

def save_config(config):
    with open("config.json","w") as file:
            json.dump(config,file,indent=4)
            
def read_operations():
     #LEE INFORMACION DE OPERACIONS
    with open("operations.json","r") as file:
        ops = json.load(file)
    return ops

def save_operation(concept,value,opt):
    ops = read_operations()

    operation = {}
    operation["operation"] = opt
    operation["value"] = value
    operation["description"] = concept
    ops.append(operation)

    with open("operations.json","w") as file:
            json.dump(ops,file,indent=4)
            
    #se efectua la modificacion del balance
    operate_balance(opt,value)
    
def operate_balance(operation,value):
    config = load_config()
    balance = config["balance"]
    band = True
    
    match operation:
        case "+":
           rs = float(balance) + float(value) 
        case "-":
           rs = float(balance) - float(value)
        case _: 
            print("Operación no reconocida.")
            band = False
            
    if(band):
        config["balance"] = rs
        save_config(config)
            
def login():
    config_data = load_config()
    
    print("\n--------------------------")
    print("Bienvenido a Tu Sistema de Gestion Personal")
    print("--------------------------\n")
    login_attemps = 0
    login = False
    while((login_attemps <= config_data['max_attemps']) and not login):
        user = input("Ingresa tu usuario: ")
        password = input("Ingresa tu contraseña: ")
        if(user == config_data['user'] and password == config_data['password']):
            print(f"Bienvenido { user }")
            login = True
        else:
            login_attemps+=1
            remain_attemps = config_data['max_attemps'] - login_attemps
            print("Usuario o contraseña incorrecta.")
            print(f"Te quedan {remain_attemps+1} intentos.")
    
    if(login):
        menu()
    else:
        print("\nAcceso bloqueado. Demasiados intentos fallidos.")
    

def menu():
    
    while(True):
        config_data = load_config()
        print("\n--------------------------")
        print("Sistema de Gestion Personal")
        print("--------------------------\n")
        print(f"Balance disponible: {round(config_data['balance'],2)}\n")
        print("1) Agregar Gasto")
        print("2) Agregar Fondos")
        print("3) Operaciones ")
        print("4) Salir")
        opt = input("\nSelecione una opción: ")
        
        match opt:
            case "1":
                value = input("¿Cuanto gastaste?\n")
                concept = input("¿En que los gastaste?\n")
                save_operation(concept,value,"-")
                print(f"\n Gasto por concepto {concept} ha sido guardado con exito\n")
            case "2":
                value = input("¿Cuanto recibiste?\n")
                concept = input("¿Descripción?\n")
                save_operation(concept,value,"+")
                print(f"\n Se agrego fondos por concepto de {concept} \n")
            case "3":
                print(f"\nOperaciones realizadas({ len(read_operations())}): \n")
                for operation in read_operations():
                    print(f"\nOperacion: {operation['operation']}\nConcepto: {operation['description']}\nMonto:{operation['value']}\n---------")
            case "4":
                print(f"Bye {config_data['user']}")
                break
            case _: #Este es el default
                print("Opcion no reconocida.")    
#menu()
login()
