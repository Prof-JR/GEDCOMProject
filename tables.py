from prettytable import PrettyTable
import datetime
from Project3 import validLine

def determineAge(dob, date):

    '''
       Calculate the age of a person given two dates
       dob is the person's date of birth
       date is either the current date or the death date
    '''
    age = date.year - dob.year - ((dob.month, dob.day) > (date.month, date.day))

    #age = abs((date – dob)).days / 365.25

    return age

def user_story_1(inputDate): #Dates (birth, marriage, divorce, death) should not be after the current date

    current = datetime.datetime.today()

    difference = current.year - inputDate.year - ((inputDate.month, inputDate.day) > (current.month, current.day))

    if difference < 0:
        print ("Error: Date should not be after the current one")
        return False
    else:
        return True

def user_story_18(indi, husbid, wifeid): #Siblings should NOT marry
    husb_fam = indi[husbid].famc
    wife_fam = indi[wifeid].famc
    if husb_fam == wife_fam:
        print("Incest ouccurring")
        return False
    else: return True
    
def user_story_21_a (indi, husbid): #Correct gender role for husband
    husb_gender = indi[husbid].gender
    
    if husb_gender == "M":
        print("Correct gender for husband")
        return True
    else: 
        print("Incorrect gender for husband")
        return False
    
def user_story_21_b (indi, wifeid): #Correct gender role for wife
    wife_gender = indi[wifeid].gender
    
    if wife_gender == "F":
        print("Correct gender for wife")
        return True
    else:
        print("Incorrect gender for wife")
        return False      

def user_story_3(input_date1, input_date2): # a person's birthday must be before their death date

    birthday = input_date1

    death_day = input_date2

    difference = death_day.year - birthday.year - ((birthday.month, birthday.day) > (death_day.month, death_day.day))

    if birthday != "NA" and birthday < datetime.datetime.today():
        if death_day != "NA" and death_day <= datetime.datetime.today():
            if difference < 0:
                print("Error: Death date should not be before the birth date")
                return False
            else:
                return True
        else:
            print("Error: Death date not valid")
            return False
    else:
        print("Error: Birthday not valid")
        return False


def user_story_5(input_date3, input_date4): # A person cannot get married after their death date

    marriage_date = input_date3

    death_date = input_date4

    difference = death_date.year - marriage_date.year - ((marriage_date.month, marriage_date.day) > (death_date.month, death_date.day))

    if marriage_date != "NA" and marriage_date < datetime.datetime.today():
        if death_date != "NA" and death_date <= datetime.datetime.today():
            if difference < 0:
                print("Error: Marriage date should not occur after death date")
                return False
            else:
                return True
        else:
            print("Error: Death date not valid")
            return False
    else:
        print("Error: Marriage date not valid")
        return False

        

class Person():
    
    def __init__(self):
        self.idtag = "NA"
        self.name = "NA"
        self.gender = "NA"
        self.birth = "NA"
        self.age = "NA" 
        self.alive = True
        self.death = "NA"
        self.famc = list()
        self.fams = list()

class Family():

    def __init__(self):
        self.idtag = "NA"
        self.marr = "NA"
        self.div = "N/A"
        self.husbid = "NA"
        self.husbnam = "NA" 
        self.wifeid = "NA"
        self.wifename = "NA"
        self.chil = list()

def createTables(file):

    indi = dict() # indi[id] = instance of class Person
    fam = dict() # fam[id] = instance of class Family

    arr = file.readlines()

    i = 0
    person = None
    family = None

    while  i < len(arr):
        line = arr[i].strip()
        level, tag, args, tokens = validLine(line)

        i += 1

        if tag is not None:
                
            if tag == "INDI":
                person = Person()
                person.idtag = args
                indi[person.idtag] = person
                
            elif tag == "FAM":
                family = Family()
                family.idtag = args
                fam[family.idtag] = family
                
            elif tag == "NAME":
                person.name = args
                
            elif tag == "SEX":
                person.gender = args

            elif tag == "BIRT":
                
                #need to access next line for the DATE
                newLine = arr[i].strip()
                new_level, new_tag, new_args, new_tokens = validLine(newLine)
                
                if new_tag == "DATE":
                    #person.birth = new_args
                    new_date = datetime.datetime.strptime(new_args, "%d %b %Y").date()
                    if user_story_1(new_date):
                        person.birth = new_date
                        person.age = determineAge(new_date, datetime.datetime.today())

            elif tag == "DEAT":
                person.alive = False
                
                #need to access next line for the DATE
                newLine = arr[i].strip()
                new_level, new_tag, new_args, new_tokens = validLine(newLine)
                
                if new_tag == "DATE":
                    #person.death = new_args
                    new_date = datetime.datetime.strptime(new_args, "%d %b %Y").date()
                    if user_story_1(new_date):
                        person.death = new_date
                        person.age = determineAge(person.birth, new_date)


            elif tag == "FAMS":
                person.fams.append(args)
                
            elif tag == "FAMC":
                person.famc.append(args)

            elif tag == "MARR":

                #need to access next line for the DATE
                newLine = arr[i].strip()
                new_level, new_tag, new_args, new_tokens = validLine(newLine)
                
                if new_tag == "DATE":
                    new_date = datetime.datetime.strptime(new_args, "%d %b %Y").date()
                    if user_story_1(new_date):
                        family.marr = new_date

            elif tag == "DIV":

                #need to access next line for the DATE
                newLine = arr[i].strip()
                new_level, new_tag, new_args, new_tokens = validLine(newLine)
                
                if new_tag == "DATE":
                    new_date = datetime.datetime.strptime(new_args, "%d %b %Y").date()
                    if user_story_1(new_date):
                        family.div = new_date

            elif tag == "HUSB":
                family.husbid = args
                family.husbname = indi[args].name

            elif tag == "WIFE":
                family.wifeid = args
                family.wifename = indi[args].name
                

            elif tag == "CHIL":
                family.chil.append(args)
                
    for key in fam:
        user_story_18(indi, fam[key].husbid, fam[key].wifeid)
        
    createINDI(indi)
    createFAM(fam)
    
def createINDI(indi):
    
    table = PrettyTable()
    table.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age','Alive', 'Death', 'Child', 'Spouse']
    
    for key in sorted(indi.keys()):
        idt = indi[key].idtag
        nam = indi[key].name
        gen = indi[key].gender
        bir = indi[key].birth
        dea = indi[key].death
        age = indi[key].age
        ali = indi[key].alive
        fc = indi[key].famc
        fs = indi[key].fams
        table.add_row([idt, nam, gen, bir, age, ali, dea, fc, fs])
        
    print (table)

def createFAM(fam):
    table = PrettyTable()
    table.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
    
    for key in sorted(fam.keys()):
        idt = fam[key].idtag
        mar = fam[key].marr
        div = fam[key].div
        hus = fam[key].husbname
        hid = fam[key].husbid
        wif = fam[key].wifename
        wid = fam[key].wifeid
        chi = fam[key].chil
        table.add_row([idt, mar, div, hid, hus, wid, wif, chi])
        
    print (table)

def main():

    try:
        #file = open('/Users/Test/Documents/SSW555/NicoleFamily.ged')
        file = open ('/Users/carolinetelma/Desktop/NicoleFamily.ged', 'r')
    except:
        print("Cannot open file")
        
    print(createTables(file))
    
if __name__ == '__main__':
    main()
        

