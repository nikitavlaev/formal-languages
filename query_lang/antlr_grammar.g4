grammar antlr_grammar;

script : (stmt ';')* EOF ;

stmt : 'connect' '"' STRING '"' 
     | STRING ':' pattern
     | 'select' qobject 'from' graph
     ;

graph : graph 'intersect' rgr
      | rgr
      ;

rgr : 'grammar'
    | '[' pattern ']'
    | '"' STRING '"'
    | '(' 'setStartAndFinal' vertices vertices graph ')'
    | '(' graph ')'
    ;

vertices : '{' int_set '}'
         | INT ':' INT
         | '_'
         ;

int_set : (INT ',')* INT ;

qobject : edges
        | 'count' edges
        ;

edges : 'edges'
      | 'filter' cond ':' edges
      ;

cond : '(' STRING ',' STRING ',' STRING ')' '->' '(' bool_expr ')' ;

bool_expr : bool_expr ALT bool_expr1
          | bool_expr1
          ;

bool_expr1 : bool_expr1 '&' bool_expr2
           | bool_expr2
           ;

bool_expr2 : '!' '(' bool_expr ')'
           | bool_expr3
           ;
      
bool_expr3 : STRING 'hasLbl' STRING
           | 'isStart' STRING
           | 'isFinal' STRING
           ;

pattern : pattern ALT pattern1
        | pattern1
        ;

pattern1 : pattern1 DOT pattern2
         | pattern2
         ;

pattern2 : pattern2 STAR
         | pattern2 PLUS
         | pattern2 OPTION
         | '(' pattern ')'
         | TERM '(' STRING ')'
         | NONTERM '(' STRING ')'
         | 'eps'
         ;

INT : '0' | [1-9] DIGIT* ;
STAR : '*' ;
PLUS : '+' ;
OPTION : '?' ;
DOT : '.' ;
ALT : '|' ;
TERM : 'term' ;
NONTERM : 'var' ;

fragment LOWER : [a-z] ;
fragment UPPER : [A-Z] ;
fragment DIGIT : [0-9] ;
STRING : (LOWER | UPPER | '/') (LOWER | UPPER | DIGIT | '_' | '/' | '.' )* ;
SPACE : [ \r\t\n]+ -> skip ; 
