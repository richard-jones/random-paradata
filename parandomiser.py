#ID	Title	Description	Language	Affiliation	Creator	Publisher	File Format	
#HE/FE	Record Origin	Record Created Date	JAX Classification	Subject Keywords	Type

import uuid
from random import random, randint
import os, csv
from datetime import datetime
import time

SIZE = 100

LANGUAGES = [("en", 0.1), ("en-GB", 0.7), ("en-US", 0.1), ("fr", 0.2)]
HE_AFFILIATIONS = [("The Open University", 193835),
                ("Leeds Metropolitan University", 41215),
                ("University of Manchester", 39732),
                ("Sheffield Hallam University", 33830),
                ("University of Leeds", 33585),
                ("Manchester Metropolitan University", 33490),
                ("Northumbria University", 32665),
                ("University of Nottingham", 32472),
                ("University of the West of England", 31645),
                ("University of Plymouth", 30930),
                ("Cardiff University", 30010),
                ("University of Birmingham", 29185),
                ("University of the Arts London", 28790),
                ("University of Warwick", 28435),
                ("University of Central Lancashire", 28130),
                ("Teesside University", 27505),
                ("London Metropolitan University", 26380),
                ("University of East London", 26315),
                ("University of Greenwich", 26120),
                ("Liverpool John Moores University", 25995),
                ("Kingston University", 25930),
                ("University of Glamorgan", 25770),
                ("University of Hertfordshire", 25195),
                ("Nottingham Trent University", 24905),
                ("Birmingham City University", 24850),
                ("University of Sheffield", 24715),
                ("University of Edinburgh", 24525),
                ("Edge Hill University", 24340),
                ("London South Bank University", 24280),
                ("University of Glasgow", 24240),
                ("University of Oxford", 23760),
                ("University of Westminster", 23160),
                ("University of Ulster", 23160),
                ("University of Cambridge", 22820),
                ("Queen's University of Belfast", 22810),
                ("University of Derby", 22725),
                ("University of Southampton", 22680),
                ("University of Hull", 22370),
                ("King's College London", 22275),
                ("University of Wolverhampton", 21770),
                ("City University", 21725),
                ("University of Bristol", 21720),
                ("University of Portsmouth", 21605),
                ("University of Huddersfield", 21590),
                ("De Montfort University", 21585),
                ("Middlesex University", 21350),
                ("University of Strathclyde", 21300),
                ("University College London", 21210),
                ("University of Brighton", 20975),
                ("Coventry University", 20230)]
FILE_FORMATS = [("video/mp4", 0.2), ("image/jpeg", 0.3), 
                ("impage/png", 0.3), ("application/x-shockwave-flash", 0.1), 
                ("application/pdf", 0.1)]
HE_FE = [("HE", 14035), ("FE", 2904)]
FE_AFFILIATIONS = [
        ("Amersham & Wycombe College", 1),
        ("Chelmsford College", 1),
        ("Farnborough College of Technology", 1),
        ("Great Yarmouth College", 1),
        ("Hackney Community College", 1),
        ("Isle of Wight College", 1),
        ("Kidderminster College", 1),
        ("Myerscough College", 1),
        ("New College, Telford", 1),
        ("Reigate College", 1)
    ]
ORIGIN = [("Repository", 0.3), ("Manual Entry", 0.1), ("Bulk Upload", 0.6)]

FE_JAX = [
    ("Agriculture Horticulture & Animal Care", 16),
    ("Area Studies / Cultural Studies / Languages / Literature", 94),
    ("Arts & Crafts", 74),
    ("Business / Management / Office Studies", 119),
    ("Catering / Food / Leisure Services / Tourism", 192),
    ("Communication / Media / Publishing", 55),
    ("Construction & Property (Built Environment)", 115),
    ("Education / Training / Teaching", 860),
    ("Engineering", 79),
    ("Environment Protection / Energy / Cleansing / Security", 2),
    ("Family Care / Personal Development / Personal Care & Appearance", 67),
    ("Health Care / Medicine / Health & Safety", 285),
    ("Humanities (History / Archaeology / Religious Studies / Philosophy)", 29),
    ("Information Technology & Information", 281),
    ("Logistics / Distribution / Transport / Driving", 0),
    ("Manufacturing / Production Work", 14),
    ("Oil / Mining / Plastics / Chemicals", 3),
    ("Performing Arts", 121),
    ("Politics / Economics / Law / Social Sciences", 108),
    ("Sales Marketing & Retailing", 94),
    ("Sciences & Mathematics", 264),
    ("Sports Games & Recreation", 32)
    ]

HE_JAX = [
    ("Architecture, Building and Planning", 66),
    ("Biological Sciences", 366),
    ("Business and Administrative studies", 695),
    ("Creative Arts and Design", 4304),
    ("Eastern, Asiatic, African, American and Australasian Languages, Literature and related subjects", 11),
    ("Education", 1310),
    ("Engineering", 1349),
    ("European Languages, Literature and related subjects", 366),
    ("Historical and Philosophical studies", 925),
    ("Law", 80),
    ("Linguistics, Classics and related subjects", 53),
    ("Mass Communications and Documentation", 139),
    ("Mathematical and Computer Sciences", 1019),
    ("Medicine and Dentistry", 307),
    ("Physical Sciences", 547),
    ("Social studies", 1004),
    ("Subjects allied to Medicine", 421),
    ("Technologies", 123),
    ("Veterinary Sciences, Agriculture and related subjects", 950)
    ]

KEYWORDS = {
    "Agriculture Horticulture & Animal Care": ['vet', 'farm', 'dog', 'cow', 'pig'],
    "Area Studies / Cultural Studies / Languages / Literature": ['english', 'french', 'german', 'welsh', 'finnish'],
    "Arts & Crafts": ['buttons', 'textiles', 'handmade', 'collage', 'beads'],
    "Business / Management / Office Studies": ['money', 'power', 'desks', 'corporate', 'structure'],
    "Catering / Food / Leisure Services / Tourism": ['eating', 'restaurant', 'waiting', 'customer', 'gym'],
    "Communication / Media / Publishing": ['newspaper', 'internet', 'magazine', 'layout', 'design'],
    "Construction & Property (Built Environment)": ['concrete', 'architecture', 'engineering', 'lettings', 'foundations'],
    "Education / Training / Teaching": ['course', 'study', 'learn', 'exam', 'class'],
    "Engineering": ['building', 'software', 'physics', 'design', 'technical'],
    "Environment Protection / Energy / Cleansing / Security": ['sustainable', 'nuclear', 'turbine', 'carbon', 'wave'],
    "Family Care / Personal Development / Personal Care & Appearance": ['children', 'washing', 'grooming', 'comb', 'clothes'],
    "Health Care / Medicine / Health & Safety": ['hospital', 'gp', 'antibiotics', 'antiviral', 'compliance'],
    "Humanities (History / Archaeology / Religious Studies / Philosophy)": ['books', 'digging', 'bible', 'neitchze', 'hume'],
    "Information Technology & Information": ['computer', 'software', 'architecture', 'python', 'java'],
    "Logistics / Distribution / Transport / Driving": ['truck', 'van', 'road', 'parcel', 'route'],
    "Manufacturing / Production Work": ['process', 'timeline', 'flow', 'machinery', 'factory'],
    "Oil / Mining / Plastics / Chemicals": ['drill', 'mould', 'dig', 'quarry', 'mine'],
    "Performing Arts": ['dance', 'mime', 'play', 'interpretive', 'theatre'],
    "Politics / Economics / Law / Social Sciences": ['mp', 'mep', 'judge', 'survey', 'model'],
    "Sales Marketing & Retailing": ['research', 'market', 'shop', 'store', 'highstreet'],
    "Sciences & Mathematics": ['physics', 'chemistry', 'biology', 'nuroscience', 'statistics'],
    "Sports Games & Recreation": ['judo', 'fencing', 'wrestling', 'athletics', 'darts'],
    "Architecture, Building and Planning": ['listed', 'neo', 'modern', 'baroque', 'gothic'],
    "Biological Sciences": ['worm', 'organism', 'cell', 'microbe', 'philum'],
    "Business and Administrative studies": ['spreadsheet', 'document', 'tax', 'hr', 'finance'],
    "Creative Arts and Design": ['collage', 'blueprint', 'drawing', 'template', 'theatre'],
    "Eastern, Asiatic, African, American and Australasian Languages, Literature and related subjects": ['mongolian', 'mandarin', 'cantonese', 'taiwanese', 'hindi'],
    "Education": ['primary', 'secondary', 'he', 'fe', 'postgraduate'],
    "Engineering": ['cogs', 'gears', 'bridges', 'buildings', 'software'],
    "European Languages, Literature and related subjects": ['english', 'french', 'german', 'dutch', 'norwegian'],
    "Historical and Philosophical studies": ['neitchze', 'descartes', 'malory', 'hume', 'chaucer'],
    "Law": ['criminal', 'property', 'corporate', 'contract', 'enforcement'],
    "Linguistics, Classics and related subjects": ['phonics', 'syntax', 'grammar', 'latin', 'greek'],
    "Mass Communications and Documentation": ['internet', 'twitter', 'facebook', 'magazine', 'newspaper'],
    "Mathematical and Computer Sciences": ['turing', 'computability', 'completeness', 'programming', 'software'],
    "Medicine and Dentistry": ['teeth', 'organs', 'heart', 'drill', 'liver'],
    "Physical Sciences": ['physics', 'mechanics', 'gravity', 'relativity', 'velocity'],
    "Social studies": ['survey', 'anthropology', 'geography', 'human', 'life'],
    "Subjects allied to Medicine": ['neurology', 'neuroscience', 'holistics', 'pharmacology', 'pharmacy'],
    "Technologies": ['java', 'python', 'windows', 'linux', 'osx'],
    "Veterinary Sciences, Agriculture and related subjects": ['cats', 'dogs', 'pigs', 'cows', 'fish']
}

LETTER_PAIRS = {
    "a" : ["b", "d", "g", "l", "m", "n", "r", "s", "t", "y"],
    "b" : ["a", "e", "i", "l", "o", "r", "y"],
    "c" : ["a", "e", "h", "k", "o"],
    "d" : ["a", "d", "e", "i", "o"],
    "e" : ["d", "g", "l", "m", "n", "p", "r", "s", "t", "y"],
    "f" : ["a", "e", "i", "o"],
    "g" : ["a", "e", "g", "h", "i", "l", "o", "r", "y"],
    "h" : ["a", "e", "i", "o", "u", "y"],
    "i" : ["b", "d", "f", "l", "m", "n", "p", "r", "s", "t"],
    "j" : ["a", "e", "o", "u"],
    "k" : ["a", "e", "i", "l", "n", "o", "s", "y"],
    "l" : ["a", "e", "i", "k", "l", "o", "p", "t", "u", "y"],
    "m" : ["a", "e", "i", "m", "o", "p", "u", "y"],
    "n" : ["a", "d", "e", "g", "i", "k", "n", "o", "s", "u", "y"],
    "o" : ["b", "c", "d", "f", "g", "l", "m", "n", "o", "p", "r", "s", "t", "w", "y"],
    "p" : ["a", "e", "h", "i", "l", "o", "p", "r", "s", "t", "u", "y"],
    "q" : ["u"],
    "r" : ["a", "e", "i", "k", "n", "o", "p", "r", "s", "t", "u", "y"],
    "s" : ["a", "c", "e", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "s", "t", "u", "w"],
    "t" : ["a", "e", "h", "i", "o", "r", "t", "u", "w", "y"],
    "u" : ["b", "d", "g", "l", "m", "n", "p", "r", "s", "t"],
    "v" : ["a", "e", "i", "o", "u", "y"],
    "w" : ["a", "d", "e", "h", "i", "l", "o"],
    "x" : ["a", "e", "y"],
    "y" : ["a", "e", "i", "o", "u"],
    "z" : ["e"]
}

WEB_RES_OR_FT = [('wr', 0.5), ('ft', 0.5)]

def generate_record(id):
    record = {}
    record['id'] = id
    record['title'] = uuid.uuid4()
    record['description'] = 'Lorem Ipsum Dolor'
    record['language'] = select_from(LANGUAGES)
    record['creator_id'] = uuid.uuid4()
    record['creator'] = random_name()
    # FIXME: have omitted publisher, this is very thin on the ground in Jorum
    # record['publisher'] = uuid.uuid4()
    record['format'] = select_from(FILE_FORMATS)
    record['he_fe'] = select_from(HE_FE)
    record['origin'] = select_from(ORIGIN)
    record['type'] = None # what are the options here
    record['created_date'] = random_date()
    
    # now the conditionals
    if record['he_fe'] == "HE":
        record['affiliation'] = select_from(HE_AFFILIATIONS)
        record['jacs'] = select_from(HE_JAX)
    else:
        record['affiliation'] = select_from(FE_AFFILIATIONS)
        record['jacs'] = select_from(FE_JAX)
    
    record['keywords'] = random_keywords(record['jacs'])
    
    record['web_resource'] = 'false'
    record['full_text'] = 'false'
    wr_ft = select_from(WEB_RES_OR_FT)
    if wr_ft == "wr":
        record['web_resource'] = 'true'
    else:
        record['full_text'] = 'true'
    
    return record

def random_keywords(jacs):
    kws = KEYWORDS[jacs]
    num = randint(1, 5)
    rkws = []
    for i in range(num):
        select = randint(0, 4)
        k = kws[select]
        if k not in rkws:
            rkws.append(k)
    return rkws

def random_date():
    return datetime.strftime(datetime.fromtimestamp(time.time() - randint(0, 400000000)), "%Y-%m-%dT%H:%M:%SZ")
    

def random_name():
    name = ""
    length = randint(5, 10)
    letter = LETTER_PAIRS.keys()[randint(0, len(LETTER_PAIRS.keys()) - 1)]
    while len(name) < length:
        name += letter
        letter = LETTER_PAIRS[letter][randint(0, len(LETTER_PAIRS[letter]) - 1)]
    
    initial = LETTER_PAIRS.keys()[randint(0, len(LETTER_PAIRS.keys()) - 1)]
    name = name + ", " + initial
    return name
    
def select_from(arr):
    narr = normalise_probability_matrix(arr)
    r = random()
    for (option, lower, upper) in narr:
        if r >= lower and r < upper:
            return option
    return None

def normalise_probability_matrix(arr):
    total = 0.0
    for (option, weight) in arr:
        total += float(weight)
    n_ratio = 1.0 / total
    select_arr = []
    last_prob = 0.0
    for (option, weight) in arr:
        prob = float(weight) * n_ratio
        upper = last_prob + prob
        select_arr.append((option, last_prob, upper))
        last_prob = upper
    return select_arr
    
#ID	Title	Description	Language	Affiliation	Creator	Publisher	File Format	
#HE/FE	Record Origin	Record Created Date	JAX Classification	Subject Keywords	Type
oers = []
for id in range(SIZE):
    oers.append(generate_record(id))
oer_csv = open("oers.csv", "w")
writer = csv.writer(oer_csv)
writer.writerow(["OER ID", "TITLE", "DESCRIPTION", "LANGUAGE", "AFFILIATION", "CREATOR", "CREATOR_ID", 
                    "FORMAT", "HE/FE", "ORIGIN", "CREATED DATE", "JACS", "KEYWORDS", "TYPE", "WEB RESOURCE",
                    "FULL TEXT"])
for oer in oers:
    writer.writerow([oer['id'], oer['title'], oer['description'], oer['language'],
                    oer['affiliation'], oer['creator'], oer['creator_id'], oer['format'],
                    oer['he_fe'], oer['origin'], oer['created_date'], oer['jacs'],
                    ",".join(oer['keywords']), oer['type'], oer['web_resource'], oer['full_text']])
oer_csv.close()