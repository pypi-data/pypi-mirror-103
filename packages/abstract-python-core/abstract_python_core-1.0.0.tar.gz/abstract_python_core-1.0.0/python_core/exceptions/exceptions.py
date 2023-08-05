class HttpResponseException(Exception):
    """
    An Exception caused by bad Http response code
    Http codes >= 400
    """

    def __init__(self, http_code, msg):
        """
        An Exception caused by bad Http response code
        Http codes >= 400

        Args:
            http_code (int): http response status code that caused the error,
                             will determine the type of exception message
            msg (str): the system exec info, traceback is kept and we add msg to it
        """
        self.http_code = http_code
        self.msg = msg

    def __str__(self):


        output = f"""
            [ HttpResponseException ]
            {self.http_code} -- {self.msg}\n
            Make sure that : \n
            - subdomain is valid\n
            - good connection to internet\n
            - avoid using VPN

        """

        return output


class APIException(Exception):
    """
    An Exception caused by an API response with
    an error, the recieved error message/description
    will be raised
    """

    def __init__(self, http_code, msg):
        """
        An Exception caused by an API response with
        an error, the recieved error message/description
        will be raised

        Args:
            http_code (int): the response http code
            msg (str): the system exec info, traceback is kept and we add msg to it
        """
        self.http_code = http_code
        self.msg = msg

    def __str__(self):

        if self.http_code == 401:
            output = f"""
                [ HttpResponseException ]
                {self.http_code} -- {self.msg}\n
                [[ Unauthorized ]] Make sure that : \n
                - API key is valid\n

            """
        elif self.http_code == 400:
            output = f"""
                [ HttpResponseException ]
                {self.http_code} -- {self.msg}\n
                [[ Bad Request ]] Make sure that : \n
                - Request params are valid (valid phone number / valid IP address ...)\n

            """
        else:
            output = f"""
                [ HttpResponseException ]
                {self.http_code} -- {self.msg}\n
                Make sure that : \n
                - subdomain is valid\n
                - connection to internet\n
                - avoid using VPN

            """

        return output

