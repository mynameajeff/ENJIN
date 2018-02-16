
?expr: label 
     | (vvars
     |  declare
     |  screen
     |  asset
     |  loop) ";"
     

?label: (l_begin
      |  l_end)

?vvars: (property
      |  method)

?declare: (const_dcl
        |  var_dcl)


l_begin: "LABEL" VARNAME "="
l_end:   "ENDLABEL" ";"


loop: "LOOP" "(" parameters ")"


asset: "ASSET" VARNAME "=" string


screen: "SCREEN" VARNAME "=" "(" parameters ")"


var_dcl:   "VAR"   dcl
const_dcl: "CONST" dcl

?dcl: VARNAME "=" (SIGNED_NUMBER | bool | string | P_VARNAME)


method: P_VARNAME "." VARNAME "(" parameters ")"

property: P_VARNAME "." VARNAME "=" (string | P_VARNAME | bool | SIGNED_NUMBER)


parameters: prm*

?prm:  "," prm
    |  SIGNED_NUMBER
    |  P_VARNAME
    |  method
    |  string
    |  bool


bool: TRUE
    | FALSE

VARNAME: /[A-Za-z0-9_-]+/
P_VARNAME: /\$[A-Za-z0-9_-]+/

string: STR_CONST
STR_CONST: /\"[A-Za-z0-9\/\.!?~ ]+\"/

TRUE: "*true"
FALSE: "*false"

%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
