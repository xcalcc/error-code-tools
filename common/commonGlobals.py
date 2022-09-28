#
#  Copyright (C) 2021 Xcalibyte (Shenzhen) Limited.
#


import logging
from enum import Enum
from aenum import MultiValueEnum

ERR_EMPTY_MESSAGE = "%s is empty!  \n"
ERR_DUPLICATE_CODE = "%s is repeated!  \n"
ERR_FILE_DB_JSON_NOT_EXIST = "%s isn't exist! \n"

FILE_DB_JSON = "fileDB.json"
OUTPUT_FILE_JSON = "errorMessage.json"

# TODO: use real address
SHAREPOINT_SITE = "xxx"
SHAREPOINT_WEB_SITE = "xxx"
SHAREPOINT_FOLDER = "Shared Documents/ErrorTools"

APPROVAL_ICON = "approval.jpg"
DIS_APPROVAL_ICON = "disApproval.jpg"

class PROC_SUB_PHASE(MultiValueEnum):
    ENGINE_MERGE = 1, "Engine & Merge"
    VTXT_DIFF = 2, "Vtxt Diff"
    V2CSF = 3, "V2csf"
    FILE_INFO = 4, "File Info"
    UPLOAD_CSF = 5, "Upload csf"

class POST_PROC_SUB_PHASE(MultiValueEnum):
    INJECT_CSF2DB = 1, "Inject csd2db"
    HANDLE_HISTORY = 2, "Handle History"

class serverPhase(MultiValueEnum):
    PROC = 30, "Proc", PROC_SUB_PHASE
    POST_PROC = 40, "Post proc", POST_PROC_SUB_PHASE

class SETUP_SUB_PHASE(MultiValueEnum):
    PROJ_CONF = 1, "Project Config"
    CREATE_PROJ = 2, "Create Project"

class PRE_PROC_SUB_PHASE(MultiValueEnum):
    SCM = 1, "SCM Preparation"
    XCALBUILD = 2, "Xcalbuild"
    PACKAGE = 3, "Package"
    UPLOAD = 4, "Upload"
    CI = 5, "CI"
    CD = 6, "CD"
    TRIAL = 7, "TRIAL"

class clientPhase(MultiValueEnum):
    SETUP = 10, "Setup", SETUP_SUB_PHASE
    PRE_PROC = 20, "Pre proc", PRE_PROC_SUB_PHASE

class whoSelectItem(MultiValueEnum):
    GENERAL = 0, "General"
    INTERNAL = 1, "Internal"
    EXTERNAL = 2, "External"
    USER = 3, "User"

class whereSelectItem(MultiValueEnum):
    INSTALLATION = 0, "Installation"
    PROJECTSETUP = 1, "Project Setup"
    SCANPREPARATION = 2, "Scan Preparation"
    SCAN = 3, "Scan"
    REPORT = 4, "Report"
    CICD = 6, "CICD"
    GENERAL = 7, "General"

class whichSelectItem(MultiValueEnum):
    USER = 0, "User"
    EXTERNAL = 1, "External"
    XCAlINTERNAL = 3, "Xcal Internal"

class userVisibleSelectItem(MultiValueEnum):
    INVISIBLE = 0, "Invisible"
    VISIBLE = 1, "Visible"


class buttonLabel(Enum):
    ADD = "add"
    SAVE = "Save"
    LOAD_ORI_JSON = "Load Excel Json"
    LOAD_JSON = "Load Json"
    OUTPUT_JSON = "Output"
    DELETE = "Delete"

class commonLabel(Enum):
    EN = "English"
    CN = "Chinese"
    CREATE_BY = "Create by"

class inputType(Enum):
    LINE = 0
    TEXT = 1
    COMBOBOX = 2

class dataType(Enum):
    STRING = 0
    INT = 1

class langField(Enum):
    EN = "eng"
    CN = "cn"

class errExcel(Enum):
    LABEL = "EXCEL"
    FIELD = "EXCEL"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errCreate(Enum):
    LABEL = "Create by"
    FIELD = "create_by"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errApprovalBy(Enum):
    LABEL = "Approval By"
    FIELD = "approval_by"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errApproval(Enum):
    LABEL = "Approval"
    FIELD = "approval"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errMessage(Enum):
    LABEL = "Error Message"
    FIELD = "err_message"
    LIST_VALUE = None
    UI_TYPE = inputType.TEXT
    REQUEST = True
    DATA_TYPE = dataType.STRING
    MULTI_LANG = langField

class errDesc(Enum):
    LABEL = "Desciption"
    FIELD = "desc"
    LIST_VALUE = None
    UI_TYPE = inputType.TEXT
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = langField

class errProducer(Enum):
    LABEL = "Producer"
    FIELD = "producer"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errPhase(Enum):
    LABEL = "Phase"
    FIELD = "phase"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = True
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errUserVisible(Enum):
    LABEL = "User Visible"
    FIELD = "user_visible"
    LIST_VALUE = userVisibleSelectItem
    UI_TYPE = inputType.COMBOBOX
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errWhat(Enum):
    LABEL = "What"
    FIELD = "what"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errWhich(Enum):
    LABEL = "Which"
    FIELD = "which"
    LIST_VALUE = whichSelectItem
    UI_TYPE = inputType.COMBOBOX
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errWhere(Enum):
    LABEL = "Where"
    FIELD = "where"
    LIST_VALUE = whereSelectItem
    UI_TYPE = inputType.COMBOBOX
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errWho(Enum):
    LABEL = "Who"
    FIELD = "who"
    LIST_VALUE = whoSelectItem
    UI_TYPE = inputType.COMBOBOX
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errCode(Enum):
    LABEL = "Error Code"
    FIELD = "err_code"
    LIST_VALUE = None
    UI_TYPE = None
    REQUEST = True
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errName(Enum):
    LABEL = "Error Name"
    FIELD = "err_name"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = False
    DATA_TYPE = dataType.STRING
    MULTI_LANG = None

class errIndex(Enum):
    LABEL = "Error Index"
    FIELD = "err_index"
    LIST_VALUE = None
    UI_TYPE = inputType.LINE
    REQUEST = True
    DATA_TYPE = dataType.INT
    MULTI_LANG = None

class errorCodeInputData(MultiValueEnum):
    ERR_CODE = errCode
    ERR_WHO = errWho
    ERR_WHERE = errWhere
    ERR_WHICH = errWhich
    ERR_WHAT = errWhat
    ERR_USER_VISIBLE = errUserVisible
    ERR_PHASE = errPhase
    ERR_PRODUCER = errProducer
    ERR_DESC_MESSAGE = errDesc
    ERR_MESSAGE = errMessage
    ERR_APPROVAL = errApproval
    ERR_APPROVAL_BY = errApprovalBy
    ERR_CREATE = errCreate
    ERR_NAME = errName
    ERR_EXCEL = errExcel


class inputLabel(Enum):
    MASTER_ID = "Master ID"
    CODE = "Code"
    ENG_ABSTRACT = "Eng Abstract"
    CN_ABSTRACT = "CN Abstract"
    ENG_DESC = "Eng Desc"
    CN_DESC = "CN Desc"
    GOOD_EXAMPLES = "Good Examples"
    BAD_EXAMPLES = "Bad Examples"
    COMPLIANCE_CODE = "Compliance Code"
    RULE_PATH_CHAR = "Rule path characteristics"


class inputField(Enum):
    MASTER_ID = "master_id"
    CODE = "code"
    ENG_ABSTRACT = "eng_abstract"
    CN_ABSTRACT = "cn_abstract"
    ENG_DESC = "eng_desc"
    CN_DESC = "cn_desc"
    GOOD_EXAMPLES = "good_examples"
    BAD_EXAMPLES = "bad_examples"
    COMPLIANCE_CODE = "compliance_code"
    RULE_PATH_CHAR = "rule_path_char"

class color(Enum):
    RED = '#f0027f'
    ORANGE = '#fdc086'
    CYAN = '#17bfaf'
    GARY = '#666666'

