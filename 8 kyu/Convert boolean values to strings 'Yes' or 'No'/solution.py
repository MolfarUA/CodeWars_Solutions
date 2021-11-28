def bool_to_word(boolean):
    if boolean:
        return 'Yes'
    return 'No'
####################
def bool_to_word(bool):
    return "Yes" if bool else "No"
##################
def bool_to_word(boolean):
    return "Yes" if boolean else "No"
###################
#Complete the method that takes a boolean value and return a 
#"Yes" string for true, or a "No" string for false.

def bool_to_word(boolean):
    if boolean == True:
        return 'Yes'
    elif boolean == False:
        return 'No'
################
def bool_to_word(bool):
    return ['No', 'Yes'][bool]
#############
bool_to_word = {True: 'Yes', False: 'No'}.get
##############
bool_to_word = ['No','Yes'].__getitem__
##############
bool_to_word= lambda _:{1:'Yes'}.get(_,'No')
###############
def bool_to_word(boolean):
    if boolean == True:
       return str("Yes")
    elif boolean == False:
       return str("No")
    else:
       print("failed")
    # TODO
if __name__ == "__main__":
  main()   
#########################
bool_to_word=lambda b:"YNeos"[1-b::2]
##################
bool_to_word=lambda b:"YNeos"[not b::2]
################
bool_to_word = lambda b : ["No", "Yes"][b]
##############
def bool_to_word(boolean):
    if boolean == True:
        var1 = "Yes"
    elif boolean == False:
        var1 = "No"
    return var1
