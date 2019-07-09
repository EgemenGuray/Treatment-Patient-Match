from typing import Dict, List, TextIO
# The "Not Available" indicator.
NA = 'NA'

# Name of the treatment attribute.
TREATMENT = 'Treatment'

# The index of the patient identifier in the dataset.
PATIENT_ID_INDEX = 0

# Dict key is name of an attribute. Corresponding dict value is value 
# of an attribute.
# E.g., {'Gender': 'female', 'Age': '58'}
NAME_TO_VALUE = Dict[str, str]

# Dict key is patient ID. Corresponding dict value is a dictionary in which
# key is attribute name and value is attribute value.
# E.g., {'tcga.5l.aat0': {'Gender': 'female', 'Age': '42'},
#        'tcga.ew.a6sa': {'Gender': 'male', 'Age': 59}}
ID_TO_ATTRIBUTES = Dict[str, NAME_TO_VALUE]

# Dict key is attribute value. Corresponding dict value is a list of 
# patient IDs.
# E.g., for the attribute name 'Gender' the dict could be:
#      {'female': ['tcga.5l.aat0', 'tcga.5l.aat1', 'tcga.a1.a0sp'],
#       'male': ['tcga.ew.a6sa']}
VALUE_TO_IDS = Dict[str, List[str]]

# Dict key is patient ID. Corresponding dict value is similarity measure.
# E.g., for the patient 'tcga.5l.aat0' the dict could be:
#      {'tcga.5l.aat1': 1.5, 'tcga.ew.a6sa' : 0.75}
ID_TO_SIMILARITY = Dict[str, float]


### Constants to help test code - use in docstring examples
THREE_PATIENTS = {
    'tcga.5l.aat0':
    {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '0', 'Treatment': 'plan_1'},
    'tcga.aq.a54o':
    {'Age': '51', 'Gender': 'male', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '0', 'Treatment': 'plan_2'},
    'tcga.aq.a7u7':
    {'Age': '55', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '4', 'Treatment': 'plan_4'}
}

PATIENTS_WITH_NA = {
    'tcga.5l.aat0':
    {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'NA', 'Lymph_Nodes': '0', 'Treatment': 'plan_1'},
    'tcga.aq.a54o':
    {'Age': '51', 'Gender': 'male', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '0', 'Treatment': 'plan_2'},
    'tcga.aq.a7u7':
    {'Age': '55', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': 'NA', 'Treatment': 'NA'}
}

NEW_PATIENT_INFO = {'Age': '50', 'Gender': 'female', 'Tumor_Size': 't2',
                    'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
                    'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 
                    'Treatment': 'NA'}

NEW_PATIENTS = {
    'tcga.uu.a93s':
    {'Age': '63', 'Gender': 'female', 'Tumor_Size': 't4d',
     'Nearby_Cancer_Lymphnodes': 'n3b', 'Cancer_Spread': 'm1',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': 'NA', 'Treatment': 'NA'},
    'tcga.v7.a7hq':
    {'Age': '75', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '5', 'Treatment': 'NA'},
    'tcga.xx.a899':
    {'Age': '46', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'mx',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 'Treatment': 'NA'},
}

NEW_PATIENTS_RECOMMENDATIONS = {
    'tcga.uu.a93s':
    {'Age': '63', 'Gender': 'female', 'Tumor_Size': 't4d',
     'Nearby_Cancer_Lymphnodes': 'n3b', 'Cancer_Spread': 'm1',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': 'NA', 'Treatment': 'plan_4'},
    'tcga.v7.a7hq':
    {'Age': '75', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'},
    'tcga.xx.a899':
    {'Age': '46', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'mx',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'},
}



def read_patients_dataset(patients_file: TextIO) -> ID_TO_ATTRIBUTES:
    i = 0
    age = 'Age'
    gender = 'Gender'
    ts = 'Tumor_Size'
    ncl = 'Nearby_Cancer_Lymphnodes'
    cs = 'Cancer_Spread'
    ht = 'Histological_Type'
    ln = 'Lymph_Nodes'
    trt = 'Treatment'
    retDict = {}
    for row in patients_file:
        col = row.split('\t')
        if not i == 0:
            patientName = col[0]
            data1 = col[1]
            data2 = col[2]
            data3 = col[3]
            data4 = col[4]
            data5 = col[5]
            data6 = col[6]
            data7 = col[7]
            data8 = col[8].replace('\n', '')
            patientDict = { age : data1, gender : data2, ts: data3, ncl: data4, cs: data5, ht: data6, ln: data7, trt: data8}
            retDict.update( { patientName : patientDict} )
        else:
            age = col[1]
            gender = col[2]
            ts = col[3]
            ncl = col[4]
            cs = col[5]
            ht = col[6]
            ln = col[7]
            trt = col[8].replace('\n', '')
        i = i + 1
    #print(retDict)
    #print('')
    #print(THREE_PATIENTS)
    return retDict
        



def build_value_to_ids(id_to_attributes: ID_TO_ATTRIBUTES, name: str) -> VALUE_TO_IDS:
    expected = {}
    for patId, patDict in id_to_attributes.items():   
        val = patDict.get(name)
        arr = [patId]
        if not expected.get(val) == None:
            arr = expected.get(val) + arr
        expected.update( {val : arr } )
        
    return expected



def patients_with_missing_values(id_to_attributes: ID_TO_ATTRIBUTES, name: str) -> List[str]:
    retVal = []
    for patId, patDict in id_to_attributes.items():    
        val = patDict.get(name)
        if val == NA:
            retVal.append(patId)
            
    return retVal





def similarity_score(name_to_value_1: NAME_TO_VALUE,
                     name_to_value_2: NAME_TO_VALUE) -> float:
    total = 0.0
    len1 = len(name_to_value_1.values())
    len2 = len(name_to_value_2.values())
    keyL = name_to_value_1.keys()
    if len1 > len2:
        keyL = name_to_value_2.keys()
    
        
    for key in  keyL:
        val1 = name_to_value_1[key]
        val2 = name_to_value_2[key]
    
        if val1 == NA or val2 == NA:
            total = total + 0.5
        elif val1.isnumeric() and val2.isnumeric():
            total = total + 1.0/(abs(float(val1) - float(val2)) + 1.0)
        elif val1 == val2:
            total = total + 1.0
        else:
            total = total + 0.0
            
    return round(total,2)
            


def patient_similarities(id_to_attributes: ID_TO_ATTRIBUTES, name_to_value: NAME_TO_VALUE) -> ID_TO_SIMILARITY:
    expected = {}
    for key in id_to_attributes.keys(): 
        simScore = similarity_score(id_to_attributes[key], name_to_value)
        expected.update( {key : simScore } )
    return expected


def patients_by_similarity(id_to_attributes: ID_TO_ATTRIBUTES, name_to_value: NAME_TO_VALUE) -> List[str]:
    dicT = patient_similarities(id_to_attributes, name_to_value)
    sorted_dicT = sorted(dicT.items() , key = lambda kv:kv[1])
    retval = []
    for keys in sorted_dicT:
        retval.append(keys[0])
    
    retval = retval[::-1]
    return retval

    

def treatment_recommendations(id_to_attributes: ID_TO_ATTRIBUTES,
                              name_to_value: NAME_TO_VALUE) -> List[str]:
    sim = patients_by_similarity(id_to_attributes, name_to_value)
    retval = []
    for item in sim:
        retval.append(id_to_attributes[item][TREATMENT])
    return retval


def make_treatment_plans(id_to_attributes: ID_TO_ATTRIBUTES,
                         new_id_to_attributes: ID_TO_ATTRIBUTES) -> None:
    for value in new_id_to_attributes.values(): 
        if value[TREATMENT] == NA:
            rec = treatment_recommendations(id_to_attributes, value)
            value[TREATMENT] = rec[0]
    

            

# Provided helper functions - can be used to test two objects for `sameness'.

def same_key_to_list_dicts(key_to_list1: Dict[str, List[str]],
                           key_to_list2: Dict[str, List[str]]) -> bool:
    """Return True if and only if key_to_list1 and key_to_list2 are equal
    dictionaries, regardless of the order in which elements occur in the 
    dictionaries' values.

    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    True
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'w']})
    False
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'd': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    False
    """

    if key_to_list1.keys() != key_to_list2.keys():
        return False

    for key in key_to_list1:
        if not same_lists(key_to_list1[key], key_to_list2[key]):
            return False

    return True


def same_lists(list1: list, list2: list) -> bool:
    """Return True if and only if list1 and list2 are equal lists, regardless 
    of the order in which elements occur.

    >>> same_lists(['x', 'y', 'z'], ['y', 'z', 'x'])
    True
    >>> same_lists(['x', 'y', 'k'], ['y', 'z', 'x'])
    False
    """

    return sorted(list1) == sorted(list2)


