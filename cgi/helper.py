import base64, hmac, hashlib, json, random, string


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
