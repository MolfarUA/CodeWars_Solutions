import re
import traceback
import random
import time

from collections import defaultdict
from datetime import datetime, timedelta

READABLE_DATE_FORMAT = "%B %d, %Y"
DIGIT_DATE_FORMAT = "%Y.%m.%d"
TODAY = datetime.strptime("November 22, 1982", READABLE_DATE_FORMAT)

import re
import traceback

from datetime import datetime


READABLE_DATE_FORMAT = "%B %d, %Y"
DIGIT_DATE_FORMAT = "%Y.%m.%d"
TODAY = datetime.strptime("November 22, 1982", READABLE_DATE_FORMAT)


class Classifier:
    nations = [
        'Arstotzka',
        'Antegria',
        'Impor',
        'Kolechia',
        'Obristan',
        'Republia',
        'United Federation'
    ]
    
    excluded_fields = {"EXP",}
    
    field_map = {
        'DOB': 'date of birth', 
        'NATION': 'nationality', 
        'HEIGHT': 'height', 
        'WEIGHT': 'weight', 
        'ID#': 'ID number', 
        'NAME': 'name'}
    
    def __init__(self):
        self.rules = {
            nation: {
                "allowed": False,
                "required_documents": [],
                "required_vaccines": []
            } 
            for nation in self.nations
        }
        
        self.criminals = set()
        
        self.errors = []
        self.detains = []
        
        self.is_work_pass_required = False
    
    def _get_domains(self, string):
        if string.startswith("Entrants"):
            return ["Entrants"]
        elif string.startswith("Foreigners"):
            return ["Foreigners"]
        else:
            return re.match(r"Citizens\sof\s(.+?)\s(require|no)\s", string).group(1).split(", ")

    def _parse_nations(self, string):
        action, nations = re.match(r"(Allow|Deny)\scitizens\sof\s(.+)", string).groups()
        return action, nations.split(", ")

    def _update_nations(self, action, nations):
        for nation in nations:
            self.rules[nation]["allowed"] = action == "Allow"

    def _parse_documents(self, string):
        domains = self._get_domains(string)
        document = re.search(r"require\s(.+)", string).group(1)      
        return domains, "_".join(document.split(" "))   

    def _update_documents(self, domain, document):
        if domain == ["Entrants"]:
            changed_nations = self.nations
        elif domain == ["Foreigners"]:
            changed_nations = self.nations[1:]
        else:
            changed_nations = domain

        for nation in changed_nations:
            if document not in self.rules[nation]["required_documents"]:
                self.rules[nation]["required_documents"].append(document)

    def _parse_vaccines(self, string):
        domains = self._get_domains(string)
        illnesses = re.search(r"require\s(.+)\svaccination", string).group(1).split(", ")
        removed = "no longer" in string
        return illnesses, domains, removed
        
    def _update_vaccines(self, illnesses, domains, removed):
        if domains == ["Entrants"]:
            domains = self.nations
        elif domains == ["Foreigners"]:
            domains = self.nations[1:]
        
        if removed:
            for nation in domains:
                for illness in illnesses:
                    if illness in self.rules[nation]["required_vaccines"]:
                        self.rules[nation]["required_vaccines"].remove(illness)
                        if not self.rules[nation]["required_vaccines"]:
                            self.rules[nation]["required_documents"].remove('certificate_of_vaccination')
        else:
            for nation in domains:
                for illness in illnesses:
                    if illness not in self.rules[nation]["required_vaccines"]:
                        self.rules[nation]["required_vaccines"].append(illness)
                        if 'certificate_of_vaccination' not in self.rules[nation]["required_documents"]:
                            self.rules[nation]["required_documents"].append('certificate_of_vaccination')
    
    def _parse_criminals(self, string):
        return re.match(r"Wanted\sby\sthe\sState:\s(.+)", string).group(1).split(", ")

    def _update_criminals(self, criminals):
        self.criminals.update(criminals)

    def receive_bulletin(self, bulletin):
        self.criminals = set()
        for string in bulletin.split("\n"):
            if string.startswith("Allow") or string.startswith("Deny"):
                self._update_nations(
                    *self._parse_nations(string)
                )
            elif string.startswith("Wanted"):
                self._update_criminals(
                    self._parse_criminals(string)
                )
            elif string.startswith("Work"):
                self.is_work_pass_required = True
            elif "vaccination" in string:
                self._update_vaccines(
                    *self._parse_vaccines(string)
                )
            elif "require" in string:
                self._update_documents(
                    *self._parse_documents(string)
                )
    
    def _parse_document(self, doctext):
        data = {}
        for string in doctext.split("\n"):
            key, value = string.split(": ")
            data[key] = value
        return data
                
    def _parse_passport(self, passport):
        data = self._parse_document(passport)
        data["full_name"] = " ".join(reversed(data["NAME"].split(", ")))
        return data
    
    def _check_wanted(self, doc):
        value = doc["NAME"]
        if " ".join(reversed(value.split(", "))) in self.criminals or value in self.criminals:
            self.detains.insert(0, "Detainment: Entrant is a wanted criminal.")
            
    def _check_expiration(self, doc, name):
        if datetime.strptime(doc["EXP"], DIGIT_DATE_FORMAT) <= TODAY:
            self.errors.append("Entry denied: {} expired.".format(" ".join(name.split("_"))))
            
    def _check_coinside(self, info, doc):
        for field, value in doc.items():
            if field in info:
                if field not in self.excluded_fields and value != info[field]:
                    self.detains.append("Detainment: {} mismatch.".format(self.field_map[field]))
            else:
                info[field] = value
    
    def _validate_documents(self, traveler):
        traveler_info = {}
        for document in traveler:
            doc = self._parse_document(traveler[document])
            if 'diplomatic_authorization' == document:
                if "Arstotzka" not in doc["ACCESS"]:
                    self.errors.append("Entry denied: invalid diplomatic authorization.")
            if "EXP" in doc:
                self._check_expiration(doc, document)
            self._check_wanted(doc)
            self._check_coinside(traveler_info, doc)

        if "NATION" in traveler_info:
            nation = traveler_info["NATION"]
    
            for d in self.rules[nation]["required_documents"]:
                if d not in traveler:
                    if d == "access_permit" and \
                        ("diplomatic_authorization" in traveler or "grant_of_asylum" in traveler):
                        pass
                    else:
                        self.errors.append("Entry denied: missing required {}.".format(" ".join(d.split("_"))))
                        
            
            if not self.rules[nation]["allowed"]:
                self.errors.append("Entry denied: citizen of banned nation.")
                
            if self.is_work_pass_required and "access_permit" in traveler:
                if traveler_info["PURPOSE"] == "WORK" and "work_pass" not in traveler:
                    self.errors.append("Entry denied: missing required work pass.")
        else:
             self.errors.append("Entry denied: missing required passport.")
        return traveler_info
    
    def _check_vaccination(self, traveler):
        if "NATION" in traveler:
            required = self.rules[traveler["NATION"]]["required_vaccines"]
            if required:
                if "VACCINES" in traveler:
                    vaccines = traveler["VACCINES"]
                    for vaccine in required:
                        if vaccine not in vaccines:
                            self.errors.append("Entry denied: missing required vaccination.")
                else:
                     self.errors.append("Entry denied: missing required certificate of vaccination.")
    
    def inspect(self, traveler):
        self.errors = []
        self.detains = []
        info = self._validate_documents(traveler)
        self._check_vaccination(info)
        if self.detains:
            return self.detains
        if self.errors:
            return self.errors
        else:
            return "Glory to Arstotzka." if info["NATION"] == "Arstotzka" else "Cause no trouble."
    
nations = ['Arstotzka', 'Antegria','Impor','Kolechia','Obristan','Republia','United Federation']


def make_string_from_data(data):
    return "\n".join(["{}: {}".format(k, v) for k, v in data])

def is_valid(chance):
    return random.random() < chance

def generate_ID():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    first = random.sample(chars, 5)
    second = random.sample(chars, 5)
    return "{}-{}".format("".join(first), "".join(second))

def generate_gender():
    return "MF"[random.randint(0, 1)]

def generate_first_name(gender):
    names = {
        "M": ['Aaron','Abdullah','Adam','Adamik','Ahmad','Aidan','Alek','Aleksander','Aleksandr','Aleksi','Alfred','Andre','Andrej','Andrew','Anton','Aron','Artour','Attila','Azeem','Benito','Bernard','Borek','Boris','Bruno','Calum','Cesar','Christoph','Claude','Cosmo','Damian','Danil','David','Dimitry','Dominik','Eduardo','Emil','Erik','Evgeny','Felipe','Frederic','Fyodor','Gaston','Giovanni','Gregor','Gregory','Gunther','Gustav','Guy','Hayden','Hector','Henrik','Hubert','Hugo','Ibrahim','Igor','Isaak','Ivan','Jakob','James','Jan','Javier','Joachim','Johann','Jonathan','Jorge','Josef','Joseph','Julio','Karl','Khalid','Konstantine','Kristof','Kristofer','Lars','Lazlo','Leonid','Luis','Lukas','Maciej','Marcel','Marco','Martin','Mathias','Matthew','Michael','Mikhail','Mikkel','Mohammed','Nikolai','Nico','Nicolai','Niel','Nikolas','Olec','Omid','Otto','Pablo','Patrik','Pavel','Peter','Petr','Petros','Piotr','Pyotr','Rafal','Rasmus','Rikardo','Robert','Roman','Romeo','Samuel','Sasha','Sebastian','Sergei','Sergey','Simon','Stanislav','Stefan','Sven','Tomas','Tomasz','Vadim','Vanya','Vasily','Viktor','Vilhelm','Vincent','Vlad','Vladimir','Werner','William','Yuri','Yosef','Zachary'],
        "F": ['Ada','Adriana','Agnes','Alberta','Aleksandra','Alexa','Alexis','Amalie','Ana','Anastasia','Anita','Anna','Antonia','Anya','Augustine','Ava','Beatrix','Brenna','Cameron','Carmen','Cassandra','Cecelia','Cheyenne','Christina','Daniela','Danika','Edine','Ekaterina','Eleanor','Elena','Elizabeth','Emily','Emma','Erika','Eva','Felicia','Freja','Gabriela','Gabrielle','Galina','Georgia','Gloria','Greta','Hanna','Heidi','Helga','Ilya','Ingrid','Isabella','Ivana','Ivanka','Jennifer','Jessica','Joanna','Josefina','Josephine','Julia','Juliette','Kamala','Karin','Karina','Kascha','Katarina','Katherine','Katrina','Kristen','Kristina','Laura','Lena','Liliana','Lisa','Lorena','Lydia','Malva','Maria','Marina','Martha','Martina','Michaela','Michelle','Mikaela','Mila','Misha','Nada','Nadia','Naomi','Natalia','Natalya','Natasha','Nicole','Nikola','Nina','Olga','Paulina','Petra','Rachel','Rebeka','Renee','Roberta','Rozsa','Samantha','Sara','Sarah','Sharona','Simone','Sofia','Sonja','Sophia','Stefani','Svetlana','Tatiana','Tatyana','Teresa','Valentina','Vanessa','Victoria','Viktoria','Wilma','Yelena','Yulia','Yvonna','Zera','Zoe']
    }
    return random.choice(names[gender])

def generate_last_name():
    surnames = ['Aji','Anderson','Andrevska','Atreides','Babayev','Baryshnikova','Bennet','Bergman','Blanco','Borg','Borshiki','Bosch','Bullock','Burke','Carlstrom','Chernovski','Conrad','Costa','Costanzo','Crechiolo','Czekowicz','Dahl','David','DeGraff','Diaz','Dimanishki','Dimitrov','Dvorkin','Evans','Feyd','Fischer','Fisk','Fonseca','Frank','Frederikson','Graham','Grech','Gregorovich','Gruben','Guillot','Hammacher','Hammerstein','Hansson','Harkonnen','Haas','Hassad','Heintz','Henriksson','Hertzog','Ibrahimovic','Jacobs','Jager','Jensen','Johannson','Jokav','Jordan','Jovanovic','Jung','Kaczynska','Karlsson','Karnov','Kerr','Khan','Kierkgaard','Kirsch','Klass','Klaus','Kleiner','Knapik','Kostovetsky','Kovacs','Kowalska','Kravitz','Kreczmanski','Kremenliev','Krug','Lang','Larsen','Latva','Leonov','Levine','Lewandowski','Li','Lima','Lindberg','Lovska','Lukowski','Lundberg','Maars','Macek','Malkova','Mateo','Medici','Michaelson','Mikkelson','Moldavich','Muller','Murphy','Newman','Nilsson','Nityev','Novak','Odom','Olah','Ortiz','Owsianka','Pai','Pearl','Pejic','Peterson','Petrova','Popovic','Praskovic','Quinn','Rabban','Radic','Ramos','Rasmussen','Reed','Reichenbach','Reyes','Roberts','Romanoff','Romanov','Romanowski','Rosebrova','Rosenfeld','Sajarvi','Savelle','Schneider','Schroder','Schulz','Schumer','Seczek','Shaw','Smirnov','Sorenson','Sousa','Spektor','Stanislov','Steinberg','Steiner','Stolichnaya','Stoyakovich','Strauss','Thunstrom','Tjell','Tolaj','Tsarnaeva','Vazquez','Vaughn','Vincenza','Vyas','Wagner','Watson','Weiss','Weisz','Wojcik','Wolfe','Xavier','Yankov','Young','Zajak','Zeitsoff','Zhang','Zitna']
    return random.choice(surnames)

def generate_full_name():
    gender = generate_gender()
    return "{}, {}".format(generate_last_name(), generate_first_name(gender))

def generate_nation():
    nations = {
        "Antegria": ['St. Marmero','Glorian','Outer Grouse'],
        "Arstotzka": ['Orvech Vonor','East Grestin','Paradizna'],
        "Impor": ['Enkyo','Haihan','Tsunkeido'],
        "Kolechia": ['Yurko City','Vedor','West Grestin'],
        "Obristan": ['Skal','Lorndaz','Mergerous'],
        "Republia": ['True Glorian','Lesrenadi','Bostan'],
        'United Federation':['Great Rapid','Shingleton','Korista City']
    }
    nation = random.choice(list(nations.keys()))
    return nation, random.choice(nations[nation])

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end):
    return str_time_prop(start, end, '%Y.%m.%d', random.random())

def generate_date(valid):
    if valid:
        return random_date("1982.12.24", "1993.12.30")
    else:
        return random_date("1980.01.01", "1982.11.22")
    
def generate_dob():
    return random_date("1950.01.01", "1970.12.30")

def generate_height():
    return random.randint(145, 210)

def generate_weight():
    return random.randint(40, 130)

def generate_passport():
    nation, city = generate_nation()
    gender = generate_gender()
    return {
        "number": generate_ID(),
        "name": "{}, {}".format(generate_last_name(), generate_first_name(gender)),
        "dob": generate_dob(),
        "sex": gender,
        "issuing_city": city,
        "expiration": generate_date(True),
        "nationality": nation,
        "weight": generate_weight(),
        "height": generate_height()
    }

def generate_passport_string(passport):
    attr = [
        ['ID#','number'],
        ['NATION','nationality'],
        ['NAME','name'],
        ['DOB','dob'],
        ['SEX','sex'],
        ['ISS','issuing_city'],
        ['EXP','expiration']
    ]
    return make_string_from_data([[key, passport[alias]] for key, alias in attr])


def generate_vaccination_certificate(traveler, needed_vaccines, valid=True):
    vaccines = ['polio','HPV','cowpox','tetanus','typhus','yellow fever',
                'cholera','rubella','hepatitis B','measles','tuberculosis']
    available_vaccines = [v for v in vaccines if v not in needed_vaccines]
    if len(needed_vaccines) > 3:
        selected_vaccines = needed_vaccines
    else:
        selected_vaccines = random.sample(available_vaccines, 4 - len(needed_vaccines))
        if valid:
            selected_vaccines.extend(needed_vaccines)
    random.shuffle(selected_vaccines)
    
    data = [
        ["NAME", traveler["name"]],
        ["ID#", traveler["number"]],
        ["VACCINES", ", ".join(selected_vaccines)]
    ]
    
    if not valid and random.random() < 0.04:
        case = random.randint(1,2)
        if case == 1:
            data[0][1] = generate_full_name()
        elif case == 2:
            data[1][1] = generate_ID()

    return make_string_from_data(data)


def generate_id_card(traveler, valid=True):
    data = [
        ['NAME', traveler["name"]],
        ['DOB', traveler["dob"]],
        ['HEIGHT', str(traveler["height"]) + "cm"],
        ['WEIGHT', str(traveler["weight"]) + "kg"]
    ]
    
    if not valid:
        case = random.randint(1,4)
        if case == 1:
            data[0][1] = generate_full_name()
        elif case == 2:
            data[1][1] = generate_date(True)
        elif case == 3:
            data[2][1] = str(generate_height()) + "cm"
        elif case == 4:
            data[3][1] = str(generate_weight()) + "kg"
    return make_string_from_data(data)


def generate_entry_data(purpose=None):
    purposes = ['TRANSIT','VISIT','WORK','IMMIGRATE']
    times = ['2 DAYS','14 DAYS','1 MONTH','2 MONTHS','3 MONTHS','6 MONTHS','1 YEAR','FOREVER']
    durations = {"TRANSIT":[0,2],"VISIT":[1,5],"WORK":[2,7],"IMMIGRATE":[7, 8]}
    if purpose is None:
        purpose = random.choice(purposes)
    left, right = durations[purpose]
    return [purpose, random.choice(times[left:right])]


def generate_work_pass(traveler, valid=True):
    vacations = ['Accounting','Agriculture','Architecture','Aviation','Construction',
                       'Dentistry','Drafting','Engineering','Fine arts','Fishing',
                       'Food service','General labor','Healthcare','Manufacturing',
                       'Research','Sports','Statistics','Surveying']
    
    data = [
        ["NAME", traveler["name"]],
        ["FIELD", random.choice(vacations)],
        ["EXP", generate_date(valid)]
    ]
    
    if not valid:
        case = random.randint(1,2)
        if case == 1:
            data[0][1] = generate_full_name()
        elif case == 2:
            data[2][1] = generate_date(False)

    return make_string_from_data(data)


def generate_access_permit(traveler, entry_data, valid=True):
    nations = ['Antegria','Impor','Kolechia','Obristan','Republia','United Federation']
    data = [
        ['NAME',traveler["name"]],
        ['NATION',traveler["nationality"]],
        ['ID#',traveler["number"]],
        ['PURPOSE', entry_data[0]],
        ['DURATION', entry_data[1]],
        ['HEIGHT', str(traveler["height"]) + "cm"],
        ['WEIGHT', str(traveler["weight"]) + "kg"],
        ['EXP', generate_date(True)]
    ]
    if not valid:
        case = random.randint(0,2)
        if case == 0:
            data[1][1] = random.choice([nation for nation in nations if nation != traveler["nationality"]])
        elif case == 1:
            data[2][1] = generate_ID()
        elif case == 2:
            data[7][1] = generate_date(valid)

    return make_string_from_data(data)


def generate_diplomatic_auth(traveler, valid=True):
    nations = ['Antegria','Impor','Kolechia','Obristan','Republia','United Federation']
    nations.remove(traveler["nationality"])
    selected_nations = random.sample(nations, random.randint(1, 4))
    if valid:
        selected_nations.append('Arstotzka')
    random.shuffle(selected_nations)
    
    data = [
        ['NAME',traveler["name"]],
        ['NATION',traveler["nationality"]],
        ['ID#',traveler["number"]],
        ["ACCESS", ", ".join(selected_nations)]
    ]
    
    if not valid and random.random() < 0.1:
        case = random.randint(0,2)
        if case == 0:
            data[1][1] = random.choice([nation for nation in nations if nation != traveler["nationality"]])
        elif case == 1:
            data[2][1] = generate_ID()
        elif case == 2:
            data[0][1] = generate_full_name()

    return make_string_from_data(data)


def generate_asylum_grant(traveler, valid=True):
    data = [
        ['NAME',traveler["name"]],
        ['NATION',traveler["nationality"]],
        ['ID#',traveler["number"]],
        ['HEIGHT', str(traveler["height"]) + "cm"],
        ['WEIGHT', str(traveler["weight"]) + "kg"],
        ['EXP', generate_date(True)]
    ]
    if not valid:
        case  = random.randint(0,2)
        if case == 0:
            data[1][1] = random.choice([nation for nation in nations if nation != traveler["nationality"]])
        elif case == 1:
            data[2][1] = generate_ID()
        elif case == 2:
            data[5][1] = generate_date(valid)
    return make_string_from_data(data)


class Game:
    day_counter = 1
    prepared_orders = defaultdict(list)
    cancel_vaccines = {}
    foreign_nations = ['Antegria','Impor','Kolechia','Obristan','Republia','United Federation']
    banned_nations = foreign_nations[:]
    allowed_nations = []
    changed_nations = []
    vaccines_map = {nation: [] for nation in foreign_nations + ['Arstotzka']}
    all_vaccines = ['polio','HPV','cowpox','tetanus','typhus','yellow fever','cholera',
                    'rubella','hepatitis B','measles','tuberculosis']
    wanted = []
    
    def _get_ban_order(self):
        if random.random() < 0.7:
            return None
        available_nations = [
            nation for nation in self.allowed_nations 
            if nation not in self.changed_nations
        ]
        count = random.randint(0, len(available_nations))
        if count == 0:
            return None
        else:
            newly_banned = random.sample(available_nations, count)
            for nation in newly_banned:
                self.allowed_nations.remove(nation)
                self.banned_nations.append(nation)
                self.changed_nations.append(nation)
            return "Deny citizens of {}".format(", ".join(newly_banned))
        
    def _get_allow_order(self):
        available_nations = [
            nation for nation in self.banned_nations 
            if nation not in self.changed_nations
        ]
        count = random.randint(0, len(available_nations))
        if count == 0:
            return None
        else:
            newly_allowed = random.sample(available_nations, count)
            for nation in newly_allowed:
                self.banned_nations.remove(nation)
                self.allowed_nations.append(nation)
                self.changed_nations.append(nation)
            return "Allow citizens of {}".format(", ".join(newly_allowed))
        
    def get_vaccination_order(self):
        case = random.random()
        if case < 0.3:
            for_whom = ("Entrants",)
            nations = self.foreign_nations + ['Arstotzka']
        elif 0.3 <= case < 0.7:
            for_whom = ("Foreigners",)
            nations = self.foreign_nations
        else:
            count = random.randint(1, 4)
            for_whom = nations = tuple(random.sample(self.foreign_nations, count))
    
        available_vaccines = [
            v for v in self.all_vaccines 
            if all(v not in self.vaccines_map[nation] for nation in nations) 
        ]

        if not available_vaccines:
            return None
        
        selected = random.choice(available_vaccines)
        
        for nation in nations:
            self.vaccines_map[nation].append(selected)
        
        order = "{} require {} vaccination".format(", ".join(for_whom), selected)
        cancel_order = "{} no longer require {} vaccination".format(", ".join(for_whom), selected)
        if for_whom[0] != "Entrants" and for_whom[0] != "Foreigners":
            order = "Citizens of " + order
            cancel_order = "Citizens of " + cancel_order
        
        timespan = 3 + random.randint(0, 5)
        
        self.prepared_orders[self.day_counter + timespan].append(cancel_order)
        self.cancel_vaccines[self.day_counter + timespan] = (nations, selected)
        return order

    def get_bulletin_generator(self):
        bulletin_schedule = [
            ['Entrants require passport','Allow citizens of Arstotzka'],
            ['Allow citizens of {}'.format(", ".join(self.foreign_nations))],
            ['Foreigners require access permit'],
            ['Citizens of Arstotzka require ID card']
        ]
        work_pass = True
        while True:
            self.day_counter += 1
            self.changed_nations = []
            self.wanted = []
            if bulletin_schedule:
                scheduled = bulletin_schedule.pop(0)
                criminal = self.get_wanted()
                scheduled.append("Wanted by the State: {}".format(" ".join(reversed(criminal.split(", ")))))
                yield scheduled
            else:
                orders = []
                allow = self._get_allow_order()
                if allow is not None:
                    orders.append(allow)

                ban = self._get_ban_order()
                if ban is not None:
                    orders.append(ban)
                
                if random.random() < 0.5:
                    orders.append(self.get_vaccination_order())
                    
                if self.prepared_orders[self.day_counter]:
                    cancel_order = self.prepared_orders[self.day_counter]
                    whom, vaccine = self.cancel_vaccines[self.day_counter]
                    for nation in whom:
                        self.vaccines_map[nation].remove(vaccine)
                    orders.extend(cancel_order)
                    
                if work_pass and self.day_counter >= 7 and random.random() < 0.2:
                    orders.append("Workers require work pass")
                    work_pass = False
                    
                criminal = self.get_wanted()
                orders.append("Wanted by the State: {}".format(" ".join(reversed(criminal.split(", ")))))
                
                yield orders
            
    
    def get_wanted(self):
        gender = generate_gender()
        first_name, last_name = generate_first_name(gender), generate_last_name()
        full_name = "{}, {}".format(last_name, first_name)
        self.wanted.append(full_name)
        return full_name
    
    def is_wanted(self, traveler):
        return traveler["name"] in self.wanted
    
    def forget_doc(self, traveler, documents: [str],  **kwargs):
        doc = random.choice(list(traveler.keys()))
        del traveler[doc]
        return traveler
            
    def generate_traveler(self, nation: str, documents: [str], valid=True, **kwargs):
        passport = generate_passport()
        passport["nationality"] = nation
        if random.random() < 0.03 and self.wanted:
            passport["name"] = random.choice(self.wanted)
        entry_data = generate_entry_data()
        
        if random.random() < 0.1:
            passport["expiration"] = generate_date(False)
        
        traveler = {
            "passport": generate_passport_string(passport)
        }

        vaccines = kwargs.get('vaccines', None)

        if vaccines is not None and vaccines:
            traveler['certificate_of_vaccination'] = generate_vaccination_certificate(
                passport, 
                vaccines, 
                valid
            )
        for doc in documents:
            if doc == 'ID_card':
                traveler[doc] = generate_id_card(passport, valid=valid)
            elif doc == 'access_permit':
                case = random.random()
                if case < 0.6: 
                    traveler[doc] = generate_access_permit(passport, entry_data, valid=valid)
                    if entry_data[0] == "WORK" and kwargs.get("work", False):
                        if random.random() < 0.6:
                            traveler['work_pass'] = generate_work_pass(passport, valid=valid)
                elif case < 0.8:
                    traveler['grant_of_asylum'] = generate_asylum_grant(passport, valid=valid)
                else:
                    traveler['diplomatic_authorization'] = generate_diplomatic_auth(passport, valid=valid)
        return traveler
    

game = Game()
g = game.get_bulletin_generator()
c = Classifier()
i = Inspector()
error = False
test.describe("31 DAYS OF SERVICE")
d = datetime(1982,11,22)
for _ in range(31):
    d += timedelta(days=1)
    test.it(d.strftime("%B %d, %Y"))
    rules = next(g)
    c.criminals = set()
    bulletin = "\n".join(rules)
    c.receive_bulletin(bulletin)
    i.receive_bulletin(bulletin)

    for __ in range(random.randint(10, 14)):
        validness = is_valid(0.72)
        nation = generate_nation()[0]
        t = game.generate_traveler(
            nation, 
            c.rules[nation]["required_documents"], 
            validness,
            vaccines=c.rules[nation]["required_vaccines"],  
            work=c.is_work_pass_required,
        )
        if not validness and random.random() < 0.3:
            t = game.forget_doc(t, c.rules[nation]["required_documents"])
        t_ = dict(t)
        first = c.inspect(t)
        second = i.inspect(t_)
        if not second or second not in first:
            error = True
        if isinstance(first, str):
            test.assert_equals(second, first)
        else:
            if second in first:
                test.assert_equals(second, first[first.index(second)])
            else:
                test.assert_equals(second, first[0])
            

if error:
    print("You are under arrest for ineptitude in performing your duties. The penalty is forced labor. Glory to Arstotzka.")
else:
