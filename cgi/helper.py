import base64, hmac, hashlib, json, random, string, re, binascii, datetime
from models.request import CgiRequest

def jwt_payload_from_request(request:CgiRequest, required:bool=False) -> dict|None :
    '''
    Checks Authorization and returns JWT payload

    required: if True then raise ValueError for unauthorized requests
    '''    
    try :
        payload = get_payload_from_jwt( get_bearer(request) )
        validate_jwt_time( payload )
    except ValueError as err :
        if required :
            raise err
        else :
            return None
    else:
        return payload


def validate_jwt_time(payload:dict, max_time=1000) -> None :
    # Внутрішня перевірка - за часовими полями (iat, nbf, exp):
    # - якщо немає жодного з полів, то перевірка провалюється
    if not ("iat" in payload or "nbf" in payload or "exp" in payload) :
        raise ValueError("Token payload must include at least one time field: iat, nbf, exp")
    # - якщо є nbf і значення у майбутньому, то відмова по nbf
    now = datetime.datetime.now().timestamp()
    if "nbf" in payload and payload["nbf"] > now :
        raise ValueError("Token not valid yet: nbf violation")
    # - якщо є ехр і значення у минулому, то відмова по ехр
    if "exp" in payload and payload["exp"] < now :
        raise ValueError("Token expired: exp violation")
    # - якщо відсутнє поле ехр, то вимагаємо наявність або iat або nbf ...
    if not "exp" in payload :
        if not ("iat" in payload or "nbf" in payload):
            raise ValueError("Origin time field (nbf or iat) required if 'exp' missed")
        #   ... і їх величина повинна вкладатись у максимальний термін, встановлений параметрично
        #  вважаємо терміном проміжок часу від найбільшої дати серед iat i nbf до поточного часу
        if now - max(payload.get("iat", 0), payload.get("nbf", 0)) > max_time :
            raise ValueError(f"Max validity time ({max_time} sec) exceeded")


def get_bearer(request:CgiRequest) -> str :
    auth_header = request.headers.get('Authorization', None)
    if not auth_header :            
        raise ValueError("Missing required header 'Authorization'")
    
    # Перевірити чи заголовок 'Authorization' має схему 'Bearer'
    auth_scheme = 'Bearer '
    if not auth_header.startswith(auth_scheme) :
        raise ValueError(f"Invalid Authorization scheme: {auth_scheme}only")
    
    return auth_header[len(auth_scheme):]


def get_payload_from_jwt(jwt:str) -> dict :
    '''
    Validate JWT by RFC7519  https://datatracker.ietf.org/doc/html/rfc7519#section-7.2

    returns: JWT payload as dict

    error: raise ValueError if validation fails
    '''
    # 1.   Verify that the JWT contains at least one period ('.') character.
    if '.' not in jwt:
        raise ValueError("Invalid token format (missing '.')")
    # 2.   Let the Encoded JOSE Header be the portion of the JWT before the first period ('.') character.
    jwt_splitted = jwt.split('.')
    # 3.   Base64url decode the Encoded JOSE Header following the
    # restriction that no line breaks, whitespace, or other additional
    # characters have been used.
    # !! Python base64.urlsafe_b64decode() -- ігнорує неправильні символи, необхідна додаткова перевірка
    # 4.   Verify that the resulting octet sequence is a UTF-8-encoded
    # representation of a completely valid JSON object conforming to
    # RFC 7159 [RFC7159]; let the JOSE Header be this JSON object.
    try :
        jose_header = b64_to_obj(jwt_splitted[0])
    except ValueError as err :
        raise ValueError(f"Invalid token header ({err})")
        
    # 5.   Verify that the resulting JOSE Header includes only parameters
    # and values whose syntax and semantics are both understood and
    # supported or that are specified as being ignored when not
    # understood.
    if not "typ" in jose_header :
        raise ValueError("Invalid token header data (missing 'typ' field)")
    if not jose_header["typ"] in ("JWT",) :
        raise ValueError("Invalid token header data (unsupported 'typ' field)")
    
    if not "alg" in jose_header :
        raise ValueError("Invalid token header data (missing 'alg' field)")
    if not jose_header["alg"] in ("HS256", "HS384", "HS512",) :
        raise ValueError("Invalid token header data (unsupported 'alg' field)")
    
    # 6-7 Перевірка підпису
    if len(jwt_splitted) != 3 :
        raise ValueError("Invalid token format (invalid parts count)")
    signed_part = jwt_splitted[0] + '.' + jwt_splitted[1]
    test_signature = get_signature(signed_part.encode(), alg=jose_header["alg"])
    if test_signature != jwt_splitted[2] :
        raise ValueError("Invalid token (signature error)")
    
    # 8.   If the JOSE Header contains a "cty" (content type) value of
    # "JWT", then the Message is a JWT that was the subject of nested
    # signing or encryption operations.  In this case, return to Step
    # 1, using the Message as the JWT.  --  TODO
    
    # 9-10 за аналогією з 3-4
    try :
        payload = b64_to_obj(jwt_splitted[1])
    except ValueError as err :
        raise ValueError(f"Invalid token payload ({err})")
    
    if "nbf" in payload and not isinstance(payload["nbf"], (int, float)) :
        raise ValueError(f"Invalid token payload (nbf must be a number by RFC 7519 sec 4.1.5)")
    
    if "iat" in payload and not isinstance(payload["iat"], (int, float)) :
        raise ValueError(f"Invalid token payload (iat must be a number by RFC 7519 sec 4.1.6)")
    
    if "exp" in payload and not isinstance(payload["exp"], (int, float)) :
        raise ValueError(f"Invalid token payload (exp must be a number by RFC 7519 sec 4.1.4)")
    
    return payload


def b64_to_obj(input:str) -> dict :
    '''
    Base64url decode the Encoded input following the
    restriction that no line breaks, whitespace, or other additional
    characters have been used.
    
    Verify that the resulting octet sequence is a UTF-8-encoded
    representation of a completely valid JSON object conforming to
    RFC 7159 [RFC7159].
    '''
    non64char = re.compile(r"[^a-zA-Z0-9-_=]")
    if re.search(non64char, input) != None :
        raise ValueError("non-base64 character(s) found")
    try :
        decoded_bytes = base64.urlsafe_b64decode(input)
    except binascii.Error :
        raise ValueError("padding error")
    try :
        result = json.loads( decoded_bytes.decode("utf-8") )
    except UnicodeDecodeError :
        raise ValueError("UTF-8 decode error")
    except Exception :
        raise ValueError("JSON decode error")
    if not isinstance(result, dict) :
        raise ValueError("non-JSON object")
    return result


def compose_jwt(payload:dict, typ:str="JWT", alg:str="HS256", secret:bytes|None=None) :
    header = {
        "alg": alg,
        "typ": typ
    }
    j_header  = json.dumps(header)    
    j_payload = json.dumps(payload)
    b_header  = base64.urlsafe_b64encode( j_header.encode(encoding="utf-8") )
    b_payload = base64.urlsafe_b64encode( j_payload.encode(encoding="utf-8") )
    body = b_header.decode('ascii') + '.' + b_payload.decode('ascii')
    return body + '.' + get_signature(body.encode(), secret, alg)


def get_signature(data:bytes, secret:bytes|None=None, alg:str="HS256", form:str="base64url") :
    if secret is None :
        secret = "secret".encode()

    if alg == "HS256" :
        mode = hashlib.sha256 
    elif alg == "HS384" :
        mode = hashlib.sha384
    elif alg == "HS512" :
        mode = hashlib.sha512
    else :
        raise ValueError(f"get_signature error: alg '{alg}' not defined")   
    
    mac = hmac.new(secret, data, mode)
    if form == "base64url" :
        return base64.urlsafe_b64encode( mac.digest() ).decode('ascii')
    elif form == "base64std" :
        return base64.standard_b64encode( mac.digest() ).decode('ascii')
    elif form == "hex" :
        return mac.digest().hex()
    else :
        raise ValueError(f"get_signature error: form '{form}' not defined")   


def generate_salt(length:int=16) -> str :
    symbols = string.ascii_letters + string.digits
    return ''.join( random.choice(symbols) for _ in range(length) )


def main() :
    print(get_signature(b"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.QWxhZGRpbjpvcGVuIHNlc2FtZQ="))

if __name__ == "__main__" :
    main()
