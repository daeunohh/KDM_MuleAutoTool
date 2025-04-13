from enum import StrEnum  

class Error_Type(StrEnum):
    NONE = "none"
    TITLE = "title"
    CONTENT = "content"
    LOGINFAIL = 'login fail'
