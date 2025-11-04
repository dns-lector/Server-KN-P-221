# JSON
import json

j_str = '''{
"x": 123,
"y": 1.23,
"b1": true,
"b2": false,
"n": null,
"a": [1,2,3],
"o": {
    "f1": "Значення"
    }
}'''

def main() :
    j = json.loads(j_str)
    print(type(j), j)   # <class 'dict'>
    for k in j :
        print(k, type(j[k]), j[k])
        # x <class 'int'> 123
        # y <class 'float'> 1.23
        # b1 <class 'bool'> True
        # b2 <class 'bool'> False
        # n <class 'NoneType'> None
        # a <class 'list'> [1, 2, 3]
        # o <class 'dict'> {'f1': 'Значення'}
    j_str2 = json.dumps(j)
    print(j_str2)   # {"x": 123, "y": 1.23, "b1": true, "b2": false, "n": null, "a": [1, 2, 3], "o": {"f1": "\u0417\u043d\u0430\u0447\u0435\u043d\u043d\u044f"}}
    json.dump(j, ensure_ascii=False, indent=4, fp=open("j.json", "w", encoding="utf-8"))
    try :
        j2 = json.load(fp=open("j.json", "r", encoding="utf-8"))
    except json.decoder.JSONDecodeError as err:
        print("Decode error:", err)
    else:
        print(j2)


if __name__ == '__main__':
    main()


'''
JavaScript Object Notation
string: 
  "The String"
values:
  123
  0.123
  true
  false
  null  
array:
  [1,2,3]
object:
  {
    "fieldName": "field value",
    "fieldName2": "field value 2"
  }  
'''