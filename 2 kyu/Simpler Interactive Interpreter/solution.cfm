component {

    variables.vars = {};
    variables.functions = {};

    function tokenize( string program ) {
        var tokens = []
        if (program == "") return tokens;
        
        var regex = '\s*([-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*';
        var start = 1
        var result = program.reFind( regex, start, true )
        while( result.len[1] ) {
            tokens.append( trim( result.match[1] ) )
            start += result.len[1]
            result = program.reFind( regex, start, true )
        }
        return tokens
    };

    function input( string exprStr ){
        var tokens = tokenize( exprStr );
        tokens = buildTree( tokens )
        
        var result = expr( tokens )
        return result
    }
    
    // Take parenthesis into account by turning flat tokens into tree
    function buildTree( array tokens ) {
        var newTokens = []
        
        while( tokens.len() > 0 ) {
          var next = tokens.first()
          tokens.deleteAt( 1 )
          if( next == '(' ) {
            next = buildTree( tokens )
          } else if( next == ')' ) {
            return newTokens
          }
          newTokens.append( next )
        }
        
        return newTokens    
    }
    
    
    function expr( array tokens ) {
                
        // return empty string for no tokens
        if( !tokens.len() ) {
            return ''
         // A single token is either a nested expression, a variable, or a constant
         } else if( tokens.len() == 1 ) {
          
             // Nested expression
            if( isArray( tokens[1] ) ) {
                return expr( tokens[1] )
            }
              
            // varible
            if( tokens[1].reFind( '^[a-zA-Z].*' ) ) {
              return getVar( tokens[1] )
            // constant
            } else {
              return tokens[1]
            }
            
         // 2 or more tokens is an assignment or an operator
         } else if( tokens.len() > 2 ) {
             
             // If second token is = then we're doing an assignment.  Eval everything to the right of the =
             if( tokens[ 2 ] == '=' ) {
                var lefthandToken = tokens.first()
                tokens.deleteAt(1)
                return assign( lefthandToken, tokens.slice( 2 ) )
            } else {
              // Process operators in this order.  Since we recursivley call ourselves, the last shall be first and the first shall be last.
              var oprs = ['+','-','*','/','%']
              for( var thisop in oprs ) {
                while( var opr = tokens.find( thisop ) ) {
                  // Process each binary operator
                  return op( thisop, expr( tokens.slice( 1, opr-1 ) ), expr( tokens.slice( opr+1 ) ) )
                }
              }
            }
         // This is an error scenario with a mismatched number of tokens
         } else {
            // Throw?
            echo( 'two left over tokens' & chr(10) )
            echo( serialize( tokens ) & chr(10) )
         }
    
    }
    
    // Get variable.  Throw if not exists
    function getVar( string name ) {
        if( !variables.vars.keyExists( name ) ) {
          throw 'Variable ' & name & ' does not exist.'
        }
        return variables.vars[ name ]
    }    

    // Set a variable
    function assign( string name, array exp) {
      var value = expr( exp )
      variables.vars[ name ] = value
      return variables.vars[ name ]
    }
    
    // Process binary operators
    function op( string operator, numeric operand1, numeric operand2) {
      
      switch( operator ) {
        case '+':
          return operand1 + operand2
        case '-':
          return operand1 - operand2
        case '*':
          return operand1 * operand2
        case '/':
          return operand1 / operand2
        case '%':
          return operand1 % operand2
      }
    }

}
