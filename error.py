from enum import StrEnum  

class Error_Type(StrEnum):
    NONE = "none"
    TITLE = "title"
    CONTENT = "content"
    ID = "id"
    PW = "password"
    LOGINFAIL = 'login fail'
