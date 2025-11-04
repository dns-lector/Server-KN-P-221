# Виняткові ситуації, оброблення винятків
def throws() -> None :
    print("Throws error")
    raise TypeError


def throw_with_msg() -> None :
    raise ValueError("Message form error")


def not_throws() -> None :  # Python не має "порожнього блоку" на кшталт {}
    pass                    # для цих задач вживається оператор pass


def main() -> None :
    try :
        throws()
    except :
        print("Error detected")

    try :                               # Структура блока try
        throw_with_msg()                # Основні дії
    except TypeError :                  # Блок аналізу помилок за типом
        print("TypeError caught")       #
    except ValueError as err :          # Блок з типом та змінною
        print(err)                      # > Message form error  -- виводиться саме повідомлення без типів
    except :                            # Блок без типів - усі види помилок
        print("Undefined error")        #
    finally :                           # Фінальний блок: відпрацьовує завжди
        print("Finally action")         #

    try :
        throws()
    except :
        print("Error")
        return
    else :                              # Блок else виконується у разі успішного завершення
        print("Continue")               #  блоку try, але якщо у ньому немає return
    finally :                           # Finally виконується у т.ч. і після else
        print("Finally")                #  навіть якщо у try або except є return


if __name__ == '__main__' :
    main()
