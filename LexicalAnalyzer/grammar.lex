keywords: {if else while}
datatype: {bool int float}
letter = [a-zA-Z]
digit = [0-9]
digits = digit+
id: letter(letter|digit)*
num: digit+ |(digit+ \. digits (\L | (E digits)))
relop: (\=\=) | (\!\=) | (\>) | (\>\=) | (\<) | (\<\=)
assign: \=
punct: [\;\,\(\)\{\}]
addop:\+ | \-
mulop: \* | \/

