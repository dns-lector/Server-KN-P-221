from controllers.controller_rest import RestController, RestMeta, RestStatus, RestCache
import base64, binascii, json, re, helper

class DiscountController(RestController) :

    def serve(self) :
        # формуємо REST відповідь
        self.response.meta=RestMeta(
            service="Discount API",
            links={
                "get": "GET /discount",
                "post": "POST /discount",
            }
        )
        super().serve() 


    def do_get(self) :
        self.response.meta.service += ": User's bonuses"

        # Перевірити чи є заголовок 'Authorization' у запиті
        auth_header = self.request.headers.get('Authorization', None)
        if not auth_header :
            self.send_401("Missing required header 'Authorization'")
            return
        
        # Перевірити чи заголовок 'Authorization' має схему 'Bearer'
        auth_scheme = 'Bearer '
        if not auth_header.startswith(auth_scheme) :
            self.send_401(f"Invalid Authorization scheme: {auth_scheme} only")
            return
        
        jwt = auth_header[len(auth_scheme):]
        # Перевіряємо токен за алгоритмом з RFC7519  https://datatracker.ietf.org/doc/html/rfc7519#section-7.2
        # 1.   Verify that the JWT contains at least one period ('.') character.
        if '.' not in jwt:
            self.send_401("Invalid token format (missing '.')")
            return
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
            jose_header = self.b64_to_obj(jwt_splitted[0])
        except ValueError as err :
            self.send_401(f"Invalid token header ({err})")
            return
        
        # 5.   Verify that the resulting JOSE Header includes only parameters
        # and values whose syntax and semantics are both understood and
        # supported or that are specified as being ignored when not
        # understood.
        if not "typ" in jose_header :
            self.send_401("Invalid token header data (missing 'typ' field)")
            return
        if not jose_header["typ"] in ("JWT",) :
            self.send_401("Invalid token header data (unsupported 'typ' field)")
            return
        
        if not "alg" in jose_header :
            self.send_401("Invalid token header data (missing 'alg' field)")
            return
        if not jose_header["alg"] in ("HS256", "HS384", "HS512",) :
            self.send_401("Invalid token header data (unsupported 'alg' field)")
            return
        
        # 6-7 Перевірка підпису
        if len(jwt_splitted) != 3 :
            self.send_401("Invalid token format (invalid parts count)")
            return
        signed_part = jwt_splitted[0] + '.' + jwt_splitted[1]
        test_signature = helper.get_signature(signed_part.encode(), alg=jose_header["alg"])
        if test_signature != jwt_splitted[2] :
            self.send_401("Invalid token (signature error)")
            return
        
        # 8.   If the JOSE Header contains a "cty" (content type) value of
        # "JWT", then the Message is a JWT that was the subject of nested
        # signing or encryption operations.  In this case, return to Step
        # 1, using the Message as the JWT.  --  TODO
        
        # 9-10 за аналогією з 3-4
        try :
            payload = self.b64_to_obj(jwt_splitted[1])
        except ValueError as err :
            self.send_401(f"Invalid token payload ({err})")
            return

        self.response.meta.cache = RestCache.hrs1
        self.response.meta.dataType = "object"
        self.response.data = payload


    def b64_to_obj(self, input:str) -> dict :
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
