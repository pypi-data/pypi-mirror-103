#RP Config

Examples

| RP Config  |  http://localhost:8080  |  Examples  |  0f687fbd-5563-4f01-9a17-123d20ce7e8e |

#RP Start Bulid

Examples

| RP Start Bulid  |  Bulid Name |

#RP Start Test

Examples

| ${ReturnID}  |  RP Start Test  |  TEST  |                   |                     |

| ${ReturnID}  |  RP Start Test  |  TEST  | Test description  |                     |

| ${ReturnID}  |  RP Start Test  |  TEST  | Test description  |  {'key' : 'value'}  |


#RP Start Test Step

Examples

| ${ReturnID}           |  RP Start Test  |  TEST  |                |

| `RP Start Test Step`  |  ${ReturnID}    |  TEST  |                |

| `RP Start Test Step`  |  ${ReturnID}    |  TEST  |  D:/test.jpeg  |


#RP Finish Test

Examples

| ${ReturnID}         |  RP Start Test  |  TEST  |

| RP Start Test Step  |  ${ReturnID}    |  TEST  |

| `RP Finish Test`    |  ${ReturnID}    |        |


#RP Finish Bulid

Examples

| ${ReturnID}         |  RP Start Test  |  TEST  |

| RP Start Test Step  |  ${ReturnID}    |  TEST  |

| RP Finish Test      |  ${ReturnID}    |        |

| `RP Finish Bulid`   |                 |        |