POWER_BUTTON_PIN          =3
POWER_BUTTON_HOLD_TIME    =3
DEVICE_POLLING_TIME       =1

TOTAL_SLOTS               =5
I2C_DEVICE                =[0x50,0x51,0x52,0x53,0x54]
I2C_PORT                  =TOTAL_SLOTS

#regular slot index is from 0 to TOTAL_SLOTS-1
NON_SLOT_INDEX            =TOTAL_SLOTS
RESPONSE_SUCCESS   ='1'
RESPONSE_ERROR     ='0'
SIGN_IN_RETRY     =5
SIGN_IN_SUCCESS   =0
SIGN_IN_FAIL      =1


EN_5VCC_PIN          =5
HUB_RST_PIN          =6
FAN_PWM_PIN          =19

I2C_MEM_STATUS       =0
I2C_MEM_LED_1        =3
I2C_MEM_LED_2        =4
I2C_MEM_UV           =5
I2C_MEM_ACK          =21
I2C_MEM_FORCE_READ   =22
I2C_MEM_SYTEM_RESET  =23
I2C_MEM_UID          =24
I2C_MEM_ID           =32+2


DEVICE_STATE_ORIGINAL            = 0x00

DEVICE_STATE_CASSETTE_VALID      = 0xAB
DEVICE_STATE_CASSETTE_POLLED     = 0xAC
DEVICE_STATE_CASSETTE_EMPTY      = 0xF0
DEVICE_STATE_CASSETTE_NO_READY   = 0xF1
DEVICE_STATE_CASSETTE_WRONG      = 0xFF

DEVICE_STATE_SUBSYS_EXCEPTION    = 0xE0
DEVICE_STATE_CAMERA_ERROR        = 0xE1
DEVICE_STATE_TAKING_PHOTO        = 0xE2
DEVICE_STATE_I2C_ERROR           = 0xE3
DEVICE_STATE_EXCEPTION           = 0xE4

CASSETTE_STATUS_FLAG     = 0x80
CASSETTE_STATUS = [
                    DEVICE_STATE_CASSETTE_VALID,
                    DEVICE_STATE_CASSETTE_POLLED,
                    DEVICE_STATE_CASSETTE_EMPTY,
                    DEVICE_STATE_CASSETTE_NO_READY,
                    DEVICE_STATE_CASSETTE_WRONG
                  ]


Positive_test_result         = 0
Negative_test_result         = 1
Cassette_not_found           = 2
Control_area_not_found       = 3
Invalid_image_identifier     = 4
Unexpected_exception         = 5


#  stacked slot index  #
SLOT_STATUS_EMPTY            = 0
SLOT_STATUS_DETECTING        = 1
SLOT_STATUS_WARNING          = 2
SLOT_STATUS_POSITIVE         = 3
SLOT_STATUS_NEGATIVE         = 4
SLOT_STATUS_INVALID          = 5


INVALID_DEVICE_INDEX      =0xFF
#IMG_PATH                  ='/home/pi/gxf/python/spotii/img/'
IMG_PATH                  ='img/'

MAX_CAMERA_RESOLUTION_WIDTH     =1600
MAX_CAMERA_RESOLUTION_HEIGHT    =1200
SAMPLE_PIXELS = [[1,1], [100,100], [200,200]]


PHOTO_TAKING_STOP    = 0xAA

GPA_UNIT = 60
GAP1 = 3*GPA_UNIT+45
#GAP1 = 1*GPA_UNIT
GAP2 = 1*GPA_UNIT
GAP3 = 1*GPA_UNIT
GAP4 = 1*GPA_UNIT
GAP5 = 1*GPA_UNIT

GAP_TAIL = 15
PHOTO_TAKING_GAPS =[GAP1,GAP2,GAP3,GAP4,GAP5]

TIMER_DURATION = GAP1+GAP2+GAP3+GAP4+GAP5+GAP_TAIL

#DETECTING_TIMEOUT = GAP1+GAP2+GAP3+GAP4+GAP5+GAP6+GAP_TAIL

#server response result [0, 1, 'La0012684', 'Negative']
RESULT_SLOT_NUMBER =0
RESULT_ERROR_CODE  =1
RESULT_CASSETTE_ID =2
RESULT_TEXT        =3
RESULT_RECORD_ID   =4


baseUrl = "https://www.look-spot.ca/lsservices/ws"
CODE = 'code'
DESC = 'description'
RSLT = 'result'
TKEN = 'passtoken'
RCID = 'testRecordId'
RCODE= 'retCode'
MSSG = 'message'
ADDRESS =["finch","Toronto","Canada"]


SIGNATURE = "client=laipac&signature=laipacws"
USER      = "userid=feng.gao@laipac.com&password=123456"
SERIAL_NO = "654321"