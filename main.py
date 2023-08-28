

allowed_alphabetical = {"a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g", "h", "j", "k", "l""m", "w", "x", "c", "v", "b", "n"}
allowed_characters = {" ", "+", "(", ")"}

def client():
    power_n = 0
    algebraic_sum = input("wich remarkable identity do you want ? \n Enter elements inside parentheses :")
    algebraic_sum = modifications(algebraic_sum)
    try : 
        power_n = int(input("Enter the power : "))
        if power_n < 0 : raise ValueError
        else : 
            conditions(algebraic_sum, power_n)
    except (ValueError, SyntaxError): 
        print("PLS : respect the patern : a+b+...+z")
        algebraic_sum, power_n = client()
    
    return algebraic_sum, power_n

def modifications(algebraic_sum):
    lst_AS = []
    # FIRST : erase spaces
    algebraic_sum  = algebraic_sum.replace(" ", '')
    # SECOND : just lowercase
    algebraic_sum = algebraic_sum.lower()
    # THIRD : split elements to put them in to make the calcul easier
    lst_AS = algebraic_sum.split("+")
    return lst_AS
   
def conditions(algebraic_sum, power_n):
    index = 0
    # first condition : parentheses
    if algebraic_sum[0] == "(" and algebraic_sum[-1] == ")":
        print("You haven't to use parentheses")
        raise SyntaxError
    # second condition : (+ a + b+)
    elif (algebraic_sum[0] or algebraic_sum[-1]) == "+" : 
        print("you can't finish/start a calcul with 'a +' ")
        raise SyntaxError
    
    for letter in algebraic_sum :
        repetition = 0

        # third condition : 2 ++ next to each other
        if letter == "+" and algebraic_sum[index + 1] == "+":
            print("double +")
            raise SyntaxError
        # fourth condition : JUST LETTERS
        elif not (letter in allowed_alphabetical) and not (letter in allowed_characters) :
            print("use allowed characters")
            raise SyntaxError
        # fifth condition : PARENTHESES IN MIDDLE
        elif (index != 0 and index != len(algebraic_sum) - 1) and (letter == "(" or letter == ")"):
            print("why there is fckying parentheses here")
            raise SyntaxError
        
        # sixth condition : all differents letters    
        for check in algebraic_sum :
            if check == letter and letter != " " and letter != "+":
                repetition += 1
            if repetition >= 2 :
                print("You need to put differents letters") 
                raise SyntaxError

        index += 1   
    # default mathematics results
    if power_n == 0 : return print("0")
    elif power_n == 1 : return print(algebraic_sum)

# Used to compare 2 string without coefficients
def comparaison(str1, str2):
    str1 = pop_coeff(str1)
    str2 = pop_coeff(str2)
    if str1 == str2: return True
    else : return False

# convert list to a string
def lst_to_str(lst):
    str_ = ""
    for i in lst : str_ += i
    return str_

# delete coefficients in front of a letter
def pop_coeff(string):
    lst = list(string)
    for i in lst :
        index_i = lst.index(i)
        try :
            # generate ValueError if it's not an integer
            int(i)
            lst.pop(index_i)
            new_str_ = lst_to_str(lst)
            lst = pop_coeff(new_str_)
            return lst_to_str(lst)
        except ValueError:
            continue
    return lst_to_str(lst)

# return coefficient with type : int
def coeff_int(string):
    integer = ''
    for i in string :
        try :
            # generate ValueError if it's not an integer
            int(i)
            integer += i
        except : break
    return int(integer)

# Multiplicaiton can cause same letters that are not added, we need to add them
def sum(lst_calcul):
    letters_index = -1
    for letters in lst_calcul:
        letters_index +=  1
        check_index = -1
        for check in lst_calcul :
            check_index += 1            
            if comparaison(letters, check) and letters_index != check_index:
                # add
                add_letters = str(coeff_int(letters) + coeff_int(check)) + pop_coeff(letters)
                
                # actualize the algebraic list
                lst_calcul.append(add_letters)
                lst_calcul.pop(letters_index)
                lst_calcul.pop(check_index - 1)

                # we need to use recursive method to actualize the list
                lst_calcul = add_letters(lst_calcul)
                
                return lst_calcul
    return lst_calcul

#When you multiplie two letters you have "2a" * "3b" = "2a3b" you need to put the result away : "6ab"
def cleaner(string):
    # to make changes easier we need to transform it in a list, regulary used here
    lst_string = list(string)
    int_multiplication = 1
    for letter in lst_string:
        try :
            int_multiplication *= int(letter)
            lst_string.pop(lst_string.index(letter))
        except : continue

    new_str = lst_to_str(lst_string)
    
    # return a beautiful string
    new_str = ''.join(sorted(new_str))
    new_str = str(int_multiplication) + new_str
    return new_str

# We multiply the updated sum by the initial algebraic sum ex : n : 3 AS : a+b -> (aa + 2ab +bb)(a+b)
def multiplication(lst_AS, init_AS):
    new_lst_AS = []
    for letter in lst_AS:
        for init_letter in init_AS:
            string = cleaner(letter + init_letter)
            new_lst_AS.append(string)
    
    new_lst_AS = sum(new_lst_AS)
    return new_lst_AS

def main():
    init_lst_AS, power = client()
    lst_AS = init_lst_AS
    for _ in range(power - 1):
        lst_AS = multiplication(lst_AS, init_lst_AS)

    return lst_AS

print(main())