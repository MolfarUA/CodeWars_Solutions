/**
 * A tiny three pass compiler.
 *
 * Class Compiler
 */
class Compiler {

  /**
   * Compiles a given program.
   *
   * @param $program
   *   The program to compile.
   */
  public function compile($program) {
    return $this->pass3($this->pass2($this->pass1($program)));
  }

  /**
   * Split a program up into tokens.
   *
   * @param $program
   *   The program to tokenize.
   *
   * @return array
   *   The tokenized program.
   */
  public function tokenize($program) {
    /*
     * Turn a program string into an array of tokens.  Each token
     * is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
     * name or a number (as a string)
     */
    $tokens = preg_split('/\s+/', trim(preg_replace('/([-+*\/\(\)\[\]])/', ' $1 ', $program)));
    foreach ($tokens as &$token) {
      if (is_numeric($token)) {
        $token = (int) $token;
      }
    }
    return $tokens;
  }

  /**
   * The first pass for the compiler.
   *
   * @param string $program
   *   The program to compile.
   */
  public function pass1($program) {
    // Returns an un-optimized AST
    $tokens = $this->tokenize($program);
    $arg_list = $this->getArgListFromTokens($tokens);
    return $this->getASTFromTokens($tokens, $arg_list);
  }

  /**
   * The second pass for the compiler.
   *
   * @param array $ast
   *   The Abstract Syntax Tree to compile.
   */
  public function pass2($ast) {
    // Returns an AST with constant expressions reduced
    if (in_array($ast['op'], ['arg', 'imm'])) {
      return $ast;
    }

    $ast['a'] = $this->pass2($ast['a']);
    $ast['b'] = $this->pass2($ast['b']);
    if ($ast['a']['op'] === 'imm' && $ast['b']['op'] === 'imm') {
      return [
        'op' => 'imm',
        'n' => eval('return ' . $ast['a']['n'] . $ast['op'] . $ast['b']['n'] . ';'),
      ];
    }

    return $ast;
  }

  /**
   * The third pass for the compiler.
   *
   * @param array $ast
   *   The Abstract Syntax Tree to compile.
   */
  public function pass3($ast) {
    // Returns assembly instructions
    switch ($ast['op']) {
      case 'imm':
        return ["IM {$ast['n']}", "PU"];
      case 'arg':
        return ["AR {$ast['n']}", "PU"];
      case '+':
        return array_merge($this->pass3($ast['a']), $this->pass3($ast['b']), ["PO", "SW", "PO", "AD", "PU"]);
      case '-':
        return array_merge($this->pass3($ast['a']), $this->pass3($ast['b']), ["PO", "SW", "PO", "SU", "PU"]);
      case '*':
        return array_merge($this->pass3($ast['a']), $this->pass3($ast['b']), ["PO", "SW", "PO", "MU", "PU"]);
      case '/':
        return array_merge($this->pass3($ast['a']), $this->pass3($ast['b']), ["PO", "SW", "PO", "DI", "PU"]);
      default:
        return [];
    }
  }

  /**
   * Gets the arg list from an array of tokens.
   *
   * @param array $tokens
   *   The tokens to get the arg list from.
   */
  protected function getArgListFromTokens(array &$tokens) {
    $arg_list = [];
    foreach ($tokens as $key => $token) {
      if ($key === 0 && $token !== '[') {
        throw new InvalidArgumentException('Invalid argument list given!');
      }

      if (in_array($token, ['[', ']'])) {
        unset($tokens[$key]);
      }

      if ($key >= 1) {
        if ($token === ']') {
          return $arg_list;
        }
        $arg_list[$token] = $key - 1;
        unset($tokens[$key]);
      }
    }
    return $arg_list;
  }

  /**
   * Gets the AST from an array of tokens.
   *
   * @param array $tokens
   *   The tokens to get the AST from.
   * @param array $arg_list
   *   A list of expression arguments.
   */
  protected function getASTFromTokens(array $tokens, array $arg_list) {
    // The operations in hierarchical order.
    $op = [
      '+' => 1, '-' => 1,
      '*' => 2, '/' => 2
    ];
    $expressions = [];
    $operators = [];

    array_unshift($tokens, '(');
    $tokens[] = ')';

    while (count($tokens)) {
      $next = array_pop($tokens);
      if ($op[$next]) {
        while (TRUE) {
          if (
            !count($operators) ||
            $operators[count($operators) - 1] === ')' ||
            $op[$operators[count($operators) - 1]] <= $op[$next]
          ) {
            $operators[] = $next;
            break;
          }

          $expressions[] = [
            'op' => array_pop($operators),
            'a' => array_pop($expressions),
            'b' => array_pop($expressions),
          ];
        }
      }
      else if ($next === '(') {
        while (($next = array_pop($operators)) !== ')') {
          if ($next === 0) {
            break;
          }
          $expressions[] = [
            'op' => $next,
            'a' => array_pop($expressions),
            'b' => array_pop($expressions),
          ];
        }
      }
      else if ($next === ')') {
        $operators[] = $next;
      }
      else if (isset($arg_list[$next])) {
        $expressions[] = ['op' => 'arg', 'n' => $arg_list[$next]];
      }
      else {
        $expressions[] = ['op' => 'imm', 'n' => $next];
      }
    }
    return $expressions[0];
  }

}
              
###############################
class Ast {
  protected $args = [];
  protected $body = [];
  protected $stack = [];
  public $polish = [];
  public $ast = [];
  
  public function __construct(array $tokens) {
    $this->prepareArgsAndBody($tokens);
    $this->sortStation();
    while(!empty($this->polish)) {
      $this->addToAst();
    }
  }
  
  protected function sortStation() {
    while(!empty($this->body)) {
      $token = array_shift($this->body);
      if(is_int($token)) {
        $this->polish[] = $token;
      } elseif($this->isVar($token)) {
        $this->polish[] = $token;
      } elseif($this->isOperator($token)) {
        while(true) {
          if(empty($this->stack)) {
            break;
          }
          $last = array_pop($this->stack);
          if(!$this->isOperator($last)) {
            $this->stack[] = $last;
            break;
          }
          if($this->operatorPriority($last) >= $this->operatorPriority($token)) {
            $this->polish[] = $last;
          } else {
            $this->stack[] = $last;
            break;
          }
        }
        $this->stack[] = $token;
      } elseif($token == '(') {
        $this->stack[] = $token;
      } elseif($token == ')') {
        while(true) {
          $token = array_pop($this->stack);
          if($token == '(') {
            break;
          } else {
            $this->polish[] = $token;
          }
        }
      }
    }
    while(!empty($this->stack)) {
      $token = array_pop($this->stack);
      $this->polish[] = $token;
    }
  }
    
  protected function operatorPriority($token) : int {
    $priority = ['+'=>1,'-'=>1,'*'=>2,'/'=>2];
    return $priority[$token];
  }
  
  protected function addToAst() {
      $token = array_shift($this->polish);
      if(is_int($token)) {
        $this->ast[] = ['op'=>'imm','n'=>$token];
      } elseif($this->isVar($token)) {
        $this->ast[] = ['op'=>'arg','n'=>$this->getVarNumber($token)];
      } elseif($this->isOperator($token)) {
        $b = array_pop($this->ast);
        $a = array_pop($this->ast);
        $this->ast[] = ['op'=>$token,'a'=>$a, 'b'=>$b];
      }
  }
  
  protected function getVarNumber($token) : int {
    $reverse = array_flip($this->args);
    return $reverse[$token];
  }
  
  protected function prepareArgsAndBody(array $tokens) {
    $tmp = array_shift($tokens);
    if($tmp != '[') {
      throw new \Exception('Will be [ at start...');
    }
    while (true) {
      $curr = array_shift($tokens);
      if($curr == ']') {
        break;
      } else {
        $this->args[] = $curr;
      }
    }
    $this->body = $tokens;
  }
  protected function isVar(string $token) : bool {
    return in_array($token, $this->args);
  }
  protected function isOperator(string $token) : bool {
    return in_array($token, ['+','-','*','/']);
  }  
}

function constantReduce(array $node) : array {
  if(!in_array($node['op'], ['+','-','*','/'])) {
    return $node;
  }
  $node['a'] = constantReduce($node['a']);
  $node['b'] = constantReduce($node['b']);
  if(($node['a']['op'] != 'imm') or ($node['b']['op'] != 'imm')) {
    return $node;
  }
  $a = $node['a']['n'];
  $b = $node['b']['n'];
//  var_dump([$a,$b]);
  switch ($node['op']) {
    case '+':
      return ['op'=>'imm', 'n'=>$a+$b];
    case '-':
      return ['op'=>'imm', 'n'=>$a-$b];
    case '*':
      return ['op'=>'imm', 'n'=>$a*$b];
    case '/':
      return ['op'=>'imm', 'n'=>$a/$a];
  }
}

class Assembler {
  public $ast;
  public $flat = [];
  public $code = [];
  public function __construct($ast)
  {
    $this->ast = $ast;
    $this->flat = $this->flat($ast);
    $this->make();
//    echo json_encode($this->code);
  }
  protected function make()
  {
    foreach($this->flat as $node) {
      $this->code = array_merge($this->code, $this->node2code($node));
    }
  }
  
  protected function flat($node)
  {
    switch ($node['op']) {
      case 'arg':
      case 'imm':
        return [$node];
      case '+':
      case '-':
      case '*':
      case '/':
        $a = $this->flat($node['a']);
        $b = $this->flat($node['b']);
        $operator = ['op'=>$node['op']];
        return array_merge($a, $b, [$operator]);
    }
  }
  protected function node2code($node)
  {
    switch ($node['op']) {
      case 'arg':
        return [
          'AR '.$node['n'],
          'PU',
        ];
      case 'imm':
      case 'arg':
        return [
          'IM '.$node['n'],
          'PU',
        ];
      case '+':
        return [
          'PO',
          'SW',
          'PO',
          'AD',
          'PU'
        ];
      case '-':
        return [
          'PO',
          'SW',
          'PO',
          'SU',
          'PU'
        ];
      case '*':
        return [
          'PO',
          'SW',
          'PO',
          'MU',
          'PU'
        ];
      case '/':
        return [
          'PO',
          'SW',
          'PO',
          'DI',
          'PU'
        ];
    }
  }
}

class Compiler {

    public function compile($program) {
        return pass3(pass2(pass1($program)));
    }

    public function tokenize($program) {
        /*
         * Turn a program string into an array of tokens.  Each token
         * is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
         * name or a number (as a string)
         */
        $tokens = preg_split('/\s+/', trim(preg_replace('/([-+*\/\(\)\[\]])/', ' $1 ', $program)));
        foreach ($tokens as &$token) {
            if (is_numeric($token)) {
                $token = intval($token);
            }
        }
        return $tokens;
    }

    public function pass1($program) {
        // Returns an un-optimized AST
        $tokens = $this->tokenize($program);
        $ast = new Ast($tokens);
        return $ast->ast[0];
    }

    public function pass2($ast) {
        // Returns an AST with constant expressions reduced
        return constantReduce($ast);
//        echo json_encode($ast);
    }

    public function pass3($ast) {
        // Returns assembly instructions
      $asm = new Assembler($ast);
      return $asm->code;
    }

}
              
#########################
class Compiler
{
    protected $variables;

    public function pass1(string $program)
    {
        $program = $this->tokenize($program);
        $this->variables = [];
        for ($i = 1; $program[$i] !== ']'; $i++) {
            $this->variables[] = $program[$i];
        }
        return $this->buildTree(array_slice($program, $i + 1));
    }

    public function pass2(array $ast)
    {
        if ($ast['op'] == 'arg' || $ast['op'] == 'imm') {
            return $ast;
        }

        $ast['a'] = $this->pass2($ast['a']);
        $ast['b'] = $this->pass2($ast['b']);
        if ($ast['a']['op'] == 'imm' && $ast['b']['op'] == 'imm') {
            $a = $ast['a']['n'];
            $b = $ast['b']['n'];
            $op = $ast['op'];
            return [
                'op' => 'imm',
                'n'  => eval("return $a $op $b;"),
            ];
        }
        return $ast;
    }

    public function pass3($ast)
    {
        if ($ast['op'] == 'arg') {
            return ["AR {$ast['n']}"];
        } elseif ($ast['op'] == 'imm') {
            return ["IM {$ast['n']}"];
        } else {
            $left = $this->pass3($ast['a']);
            $right = $this->pass3($ast['b']);
            switch ($ast['op']) {
                case '+':
                    $opAsm = 'AD';
                    break;
                case '-':
                    $opAsm = 'SU';
                    break;
                case '*':
                    $opAsm = 'MU';
                    break;
                case '/':
                    $opAsm = 'DI';
                    break;
            }
            return array_merge($left, ['PU'], $right, ['SW', 'PO', $opAsm]);
        }
    }

    protected function tokenize($program)
    {
        $tokens = preg_split('/\s+/', trim(preg_replace('/([-+*\/\(\)\[\]])/', ' $1 ', $program)));
        foreach ($tokens as &$token) {
            if (is_numeric($token)) {
                $token = intval($token);
            }
        }
        return $tokens;
    }

    protected function buildTree(array $program)
    {
        $index = $this->lowestPriority($program);
        if ($index > 0) {
            $left = array_slice($program, 0, $index);
            $right = array_slice($program, $index + 1);
            return [
                'op' => $program[$index],
                'a'  => $this->buildTree($left),
                'b'  => $this->buildTree($right),
            ];
        }

        if ($program[0] == '(' && end($program) == ')') {
            array_pop($program);
            array_shift($program);
            return $this->buildTree($program);
        }

        if (is_int($program[0])) {
            return [
                'op' => 'imm',
                'n'  => $program[0],
            ];
        } else {
            return [
                'op' => 'arg',
                'n'  => array_search($program[0], $this->variables),
            ];
        }
    }

    protected function lowestPriority(array $program)
    {
        $closed = 0;
        $secondaryIndex = 0;
        for ($i = count($program) - 1; $i > 0; $i--) {
            $s = $program[$i];
            if ($s == ')') {
                $closed++;
            } elseif ($s == '(') {
                $closed--;
            } elseif ($closed == 0) {
                if ($s == '+' || $s == '-') {
                    return $i;
                }
                if (($s == '*' || $s == '/') && $secondaryIndex == 0) {
                    $secondaryIndex = $i;
                }
            }
        }
        return $secondaryIndex;
    }
}
              
###############################
class Compiler {

  public function compile($program) {
    return pass3(pass2(pass1($program)));
  }

  public function tokenize($program) {
    /*
     * Turn a program string into an array of tokens.  Each token
     * is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
     * name or a number (as a string)
     */
    $tokens = preg_split('/\s+/', trim(preg_replace('/([-+*\/\(\)\[\]])/', ' $1 ', $program)));
    foreach ($tokens as &$token) {
      if (is_numeric($token)) {
        $token = intval($token);
      }
    }
    return $tokens;
  }
  
  private function evaluate($tokens, $args) {
    $parsed = [];
    $index = 0;
    for (; $index < count($tokens); ++$index) {
      $token = $tokens[$index];
      if ($token === '(') {
          list($consumed, $value) = $this->evaluate(array_slice($tokens, $index + 1), $args);
          $index = $consumed + 1;
          $parsed[] = $value;
      }
      elseif ($token === ')') {
        break;
      } elseif (in_array($token, ['*', '/', '+', '-'])) {
        $parsed[] = $token;
      } elseif (is_numeric($token)) {
        $parsed[] = [
          'op' => 'imm',
          'n' => $token + 0,
        ];
      } elseif (isset($args[$token])) {
        $parsed[] = [
          'op' => 'arg',
          'n' => $args[$token],
        ];
      } else {
        throw new Exception("UNREACHABLE token=$token");
      }
    }
    $combine = function($ops) use(&$parsed) {
      while (true) {
        $keys = [];
        foreach ($ops as $op) {
          array_push($keys, ...array_keys($parsed, $op));
        }
        sort($keys);
        if (!$keys) {
          break;
        }
        $found = $keys[0];
        $rep = [
          'op' => $parsed[$found],
          'a' => $parsed[$found - 1],
          'b' => $parsed[$found + 1],
        ];
        unset($parsed[$found - 1]);
        unset($parsed[$found + 1]);
        $parsed[$found] = $rep;
        $parsed = [...$parsed];
      }
    };
    $combine(['*', '/']);
    $combine(['+', '-']);
    return [$index, $parsed[0]];
  }

  public function pass1($program) {
    $tokens = $this->tokenize($program);
    $index = 1;
    $args = [];
    for (; $tokens[$index] !== ']'; ++$index) {
      $token = $tokens[$index];
      $args[$token] = count($args);
    }
    ++$index;
    return $this->evaluate(array_slice($tokens, $index), $args)[1];
  }
  
  private function optimize($ast) {
    foreach ($ast as $k => $v) {
      if (is_array($v))
        $ast[$k] = $this->optimize($v);
    }
    if (in_array($ast['op'], ['*', '/', '+', '-'], true) &&
       $ast['a']['op'] === 'imm' && $ast['b']['op'] === 'imm') {
      switch ($ast['op']) {
          case '*':
            return ['op' => 'imm', 'n' => $ast['a']['n'] * $ast['b']['n']];
          case '/':
            return ['op' => 'imm', 'n' => intval($ast['a']['n'] / $ast['b']['n'])];
          case '+':
            return ['op' => 'imm', 'n' => $ast['a']['n'] + $ast['b']['n']];
          case '-':
            return ['op' => 'imm', 'n' => $ast['a']['n'] - $ast['b']['n']];
      }
    }
    return $ast;
  }

  public function pass2($ast) {
    return $this->optimize($ast);
  }
  
  private function visit($ast, bool $r1Out, &$asm) {
    if ($r1Out) {
      array_push($asm, "PU");
    } else {
      array_push($asm, "SW", "PU");
    }

    $instructions = [
      '*' => 'MU',
      '/' => 'DI',
      '+' => 'AD',
      '-' => 'SU',
      'arg' => 'AR',
      'imm' => 'IM',
    ];
    if (in_array($ast['op'], ['*', '/', '+', '-'])) {
      $this->visit($ast['a'], false, $asm);
      $this->visit($ast['b'], true, $asm);
      array_push($asm, $instructions[$ast['op']]);
    } elseif (in_array($ast['op'], ['arg', 'imm'])) {
      array_push($asm, $instructions[$ast['op']] . ' ' . $ast['n']);
    } else {
      throw new Exception("UNREACHABLE op=${$ast['op']}");
    }
    
    if ($r1Out) {
      array_push($asm, "SW", "PO");
    } else {
      array_push($asm, "SW", "PO", "SW");
    }
  }

  public function pass3($ast) {
    $asm = [];
    $this->visit($ast, false, $asm);
    return $asm;
  }

}
              
########################
<?php

class Compiler
{
  /**
   * @param string $program
   * @return string[]
   */
  public function compile(string $program): array {
    $ast1 = $this->pass1($program);

    $ast2 = $this->pass2($ast1);

    return $this->pass3($ast2);
  }

  /**
   * @param string $program
   * @return array
   * @psalm-return list<string|int>
   */
  private function tokenize(string $program): array {
    $tokenizer = new Tokenizer();
    return $tokenizer->tokenize($program);
  }

  /**
   * @param string $program
   * @return array
   */
  public function pass1(string $program): array
  {
    $tokens = $this->tokenize($program);
    $compiler = new AbstractSyntaxTreeBuilder($tokens);
    return $compiler->getAbstractSyntaxTree();
  }

  public function pass2(array $ast1): array
  {
    $optimizer = new AbstractSyntaxTreeOptimizer($ast1);
    return $optimizer->getOptimizedSyntaxTree();
  }

  /**
   * @param array $ast2
   * @return string[]
   * @psalm-return list<string>
   */
  public function pass3(array $ast2): array
  {
    $compiler = new AssemblyConverter($ast2);
    return $compiler->getAssemblyCommands();
  }
}

class Tokenizer
{
  /**
   * @param string $program
   * @return array
   * @psalm-return list<string|int>
   */
  public function tokenize(string $program): array
  {
    $program = $this->addSpacesAroundKeywords($program);

    $tokens = $this->cutProgramWithSpaces($program);

    $tokens = $this->removeEmptyTokens($tokens);

    return $this->castNumbersToInt($tokens);
  }

  private function addSpacesAroundKeywords(string $program): string
  {
    $keywords = [
      CompilerKeywords::FUNCTION_PARAMETERS_START,
      CompilerKeywords::FUNCTION_PARAMETERS_STOP,
      CompilerKeywords::OPERATOR_ADD,
      CompilerKeywords::OPERATOR_SUBTRACT,
      CompilerKeywords::OPERATOR_MULTIPLY,
      CompilerKeywords::OPERATOR_DIVIDE,
      CompilerKeywords::SUB_EXPRESSION_START,
      CompilerKeywords::SUB_EXPRESSION_STOP,
    ];
    $keywordsReplacements = $this->getKeywordsReplacements($keywords);

    return \str_replace(
      $keywords,
      $keywordsReplacements,
      $program
    );
  }

  /**
   * @param string[] $keywords
   * @psalm-param list<string> $keywords
   */
  private function getKeywordsReplacements(array $keywords): array
  {
    return \array_map(
      fn ($kw) => $this->keywordEnclosedWithSpaces($kw),
      $keywords
    );
  }

  private function keywordEnclosedWithSpaces(string $keyword): string
  {
    return " $keyword ";
  }

  /**
   * @param string $program
   * @return string[]
   * @psalm-return list<string>
   */
  private function cutProgramWithSpaces(string $program): array
  {
    return \explode(' ', $program);
  }

  /**
   * @param string[] $tokens
   * @return string[]
   * @psalm-return list<string>
   */
  private function removeEmptyTokens(array $tokens): array
  {
    return \array_values(
      \array_filter(
        $tokens,
        fn (string $t): bool => strlen($t) > 0
      )
    );
  }

  /**
   * @param string[] $tokens
   * @return array
   * @psalm-return list<string|int>
   */
  private function castNumbersToInt(array $tokens): array
  {
    return \array_map(
      fn (string $t): string|int => \is_numeric($t) ? (int) $t : $t,
      $tokens
    );
  }
}

class AbstractSyntaxTreeBuilder
{
  /**
   * @var array
   * @psalm-var array<string, int>
   */
  private array $argumentIndexesByName;
  private array $abstractSyntaxTree;
  /**
   * @var array
   * @psalm-var list<array>
   */
  private array $expressionsStack = [];
  /**
   * @var string[]
   * @psalm-var list<string>
   */
  private array $operationsStack = [];
  /**
   * @var array
   * @psalm-var list<array>
   */
  private array $savedStacks = [];

  /**
   * @param array                  $programTokens
   * @psalm-param list<string|int> $programTokens
   */
  public function __construct(private array $programTokens)
  {
    $this->abstractSyntaxTree = $this->buildAbstractSyntaxTree();
  }

  private function buildAbstractSyntaxTree(): array
  {
    $this->readArguments();

    return $this->buildSubExpressionTree();
  }

  private function readArguments(): void
  {
    $arguments = [];
    $this->readNextToken();
    $token = $this->readNextToken();
    while ($token !== CompilerKeywords::FUNCTION_PARAMETERS_STOP) {
      $arguments[] = (string) $token;
      $token = $this->readNextToken();
    }

    $this->argumentIndexesByName = \array_flip($arguments);
  }

  /**
   * @return array
   */
  private function buildSubExpressionTree(): array
  {
    $this->initExpressionAnalyzeStacks();

    $this->buildAndPushNextOperandTree();

    while (count($this->programTokens) > 0) {
      $token = $this->readNextToken();
      if ($token === CompilerKeywords::SUB_EXPRESSION_STOP) {
        break;
      }

      $op = $this->getOperation((string) $token);

      $this->buildAndPushStackedOperationsTreesWhile(fn() => $this->lastOperationHasHigherOrSamePriorityThan($op));

      $this->operationsStack[] = $op;

      $this->buildAndPushNextOperandTree();
    }

    $this->buildAndPushAllStackedOperationsTrees();

    if (count($this->expressionsStack) == 0) {
      throw new \LogicException('Bad program');
    }

    $res = \array_pop($this->expressionsStack);

    $this->endExpressionAnalyzeStacks();

    return $res;
  }

  private function initExpressionAnalyzeStacks(): void
  {
    $this->savedStacks[] = [$this->expressionsStack, $this->operationsStack];

    $this->expressionsStack = [];
    $this->operationsStack = [];
  }

  private function buildAndPushNextOperandTree(): void
  {
    $token = $this->readNextToken();

    if ($token === CompilerKeywords::SUB_EXPRESSION_START) {
      $this->expressionsStack[] = $this->buildSubExpressionTree();
    } else if (is_int($token)) {
      $this->expressionsStack[] = AbstractSyntaxTreeUtils::createConstantValue($token);
    } else {
      $this->expressionsStack[] = AbstractSyntaxTreeUtils::createArgumentIndex($this->argumentIndexesByName[$token]);
    }
  }

  private function readNextToken(): string|int
  {
    return \array_shift($this->programTokens);
  }

  /**
   * @param string $opToken
   * @return string
   * @psalm-return AbstractSyntaxTreeUtils::TYPE_OPERATION_ADD | AbstractSyntaxTreeUtils::TYPE_OPERATION_SUBTRACT | AbstractSyntaxTreeUtils::TYPE_OPERATION_MULTIPLY | AbstractSyntaxTreeUtils::TYPE_OPERATION_DIVIDE
   */
  private function getOperation(string $opToken): string
  {
    switch ($opToken) {
      case CompilerKeywords::OPERATOR_ADD:
        return AbstractSyntaxTreeUtils::TYPE_OPERATION_ADD;
      case CompilerKeywords::OPERATOR_SUBTRACT:
        return AbstractSyntaxTreeUtils::TYPE_OPERATION_SUBTRACT;
      case CompilerKeywords::OPERATOR_MULTIPLY:
        return AbstractSyntaxTreeUtils::TYPE_OPERATION_MULTIPLY;
      case CompilerKeywords::OPERATOR_DIVIDE:
        return AbstractSyntaxTreeUtils::TYPE_OPERATION_DIVIDE;
    }

    throw new \LogicException('Bad operation token \'' . $opToken . '\'');
  }

  private function buildAndPushStackedOperationsTreesWhile(callable $whileConditionCallback): void
  {
    while (
      count($this->operationsStack) > 0
      && $whileConditionCallback()
    ) {
      $this->buildAndPushLastStackedOperationTree();
    }
  }

  private function buildAndPushAllStackedOperationsTrees(): void
  {
    $this->buildAndPushStackedOperationsTreesWhile(fn() => true);
  }

  /**
   * @param string $op
   * @return bool
   */
  private function lastOperationHasHigherOrSamePriorityThan(string $op): bool
  {
    return AbstractSyntaxTreeUtils::getOperationPriority($this->operationsStack[count($this->operationsStack) - 1]) >= AbstractSyntaxTreeUtils::getOperationPriority($op);
  }

  private function buildAndPushLastStackedOperationTree(): void
  {
    $b = array_pop($this->expressionsStack);
    $a = array_pop($this->expressionsStack);
    $op = (string) array_pop($this->operationsStack);
    $this->expressionsStack[] = AbstractSyntaxTreeUtils::createOperation($op, $a, $b);
  }

  private function endExpressionAnalyzeStacks(): void
  {
    if (count($this->savedStacks) > 0) {
      list($this->expressionsStack, $this->operationsStack) = \array_pop($this->savedStacks);
    } else {
      $this->expressionsStack = [];
      $this->operationsStack = [];
    }
  }

  public function getAbstractSyntaxTree(): array
  {
    return $this->abstractSyntaxTree;
  }
}

class AbstractSyntaxTreeOptimizer
{
  public function __construct(private array $abstractSyntaxTree)
  {
  }

  public function getOptimizedSyntaxTree(): array
  {
    return $this->getOptimizedSyntaxTreeFor($this->abstractSyntaxTree);
  }

  private function getOptimizedSyntaxTreeFor(array $abstractSyntaxTree): array
  {
    if (AbstractSyntaxTreeUtils::isOperation($abstractSyntaxTree)) {
      return $this->getOptimizedOperationSyntaxTree($abstractSyntaxTree);
    }

    return $abstractSyntaxTree;
  }

  private function getOptimizedOperationSyntaxTree(array $operationSyntaxTree): array
  {
    $optimizedArgument1 = $this->getOptimizedSyntaxTreeFor(AbstractSyntaxTreeUtils::getOperationArgument1($operationSyntaxTree));

    $optimizedArgument2 = $this->getOptimizedSyntaxTreeFor(AbstractSyntaxTreeUtils::getOperationArgument2($operationSyntaxTree));

    if (AbstractSyntaxTreeUtils::isConstantValue($optimizedArgument1) && AbstractSyntaxTreeUtils::isConstantValue($optimizedArgument2)) {
      return AbstractSyntaxTreeUtils::createConstantValue(
        $this->computeOperation(
          AbstractSyntaxTreeUtils::getConstantValue($optimizedArgument1),
          AbstractSyntaxTreeUtils::getOperationType($operationSyntaxTree),
          AbstractSyntaxTreeUtils::getConstantValue($optimizedArgument2)
        )
      );
    }

    return AbstractSyntaxTreeUtils::createOperation(
      AbstractSyntaxTreeUtils::getOperationType($operationSyntaxTree),
      $optimizedArgument1,
      $optimizedArgument2
    );
  }

  private function computeOperation(int|float $constantValue1, string $operationType, int|float $constantValue2): int|float
  {
    return match ($operationType) {
      AbstractSyntaxTreeUtils::TYPE_OPERATION_ADD => $constantValue1 + $constantValue2,
      AbstractSyntaxTreeUtils::TYPE_OPERATION_SUBTRACT => $constantValue1 - $constantValue2,
      AbstractSyntaxTreeUtils::TYPE_OPERATION_MULTIPLY => $constantValue1 * $constantValue2,
      AbstractSyntaxTreeUtils::TYPE_OPERATION_DIVIDE => $constantValue1 / $constantValue2,
      default => 0
    };
  }
}

class AbstractSyntaxTreeUtils
{
  const KEY_TYPE                 = 'op';
  const TYPE_CONSTANT            = 'imm';
  const TYPE_ARGUMENT            = 'arg';
  const TYPE_OPERATION_ADD       = '+';
  const TYPE_OPERATION_SUBTRACT  = '-';
  const TYPE_OPERATION_MULTIPLY  = '*';
  const TYPE_OPERATION_DIVIDE    = '/';
  const KEY_CONSTANT_VALUE       = 'n';
  const KEY_ARGUMENT_INDEX       = 'n';
  const KEY_OPERATION_ARGUMENT_1 = 'a';
  const KEY_OPERATION_ARGUMENT_2 = 'b';

  public static function createConstantValue(int|float $constant): array
  {
    return [
      self::KEY_TYPE           => self::TYPE_CONSTANT,
      self::KEY_CONSTANT_VALUE => $constant
    ];
  }

  public static function isConstantValue(array $abstractSyntaxTree): bool
  {
    return $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_CONSTANT;
  }

  public static function getConstantValue(array $abstractSyntaxTree): int|float
  {
    return $abstractSyntaxTree[self::KEY_CONSTANT_VALUE];
  }

  public static function createArgumentIndex(int $argumentIndex): array
  {
    return [
      self::KEY_TYPE           => self::TYPE_ARGUMENT,
      self::KEY_ARGUMENT_INDEX => $argumentIndex
    ];
  }

  public static function isArgumentIndex(array $abstractSyntaxTree): bool
  {
    return $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_ARGUMENT;
  }

  public static function getArgumentIndex(array $abstractSyntaxTree): int
  {
    return $abstractSyntaxTree[self::KEY_ARGUMENT_INDEX];
  }

  /**
   * @param string                                                                                                                       $op
   * @psalm-param self::TYPE_OPERATION_ADD | self::TYPE_OPERATION_SUBTRACT | self::TYPE_OPERATION_MULTIPLY | self::TYPE_OPERATION_DIVIDE $op
   * @param array                                                                                                                        $a
   * @param array                                                                                                                        $b
   * @return array
   */
  public static function createOperation(string $op, array $a, array $b): array
  {
    return [
      self::KEY_TYPE                 => $op,
      self::KEY_OPERATION_ARGUMENT_1 => $a,
      self::KEY_OPERATION_ARGUMENT_2 => $b
    ];
  }

  public static function isOperation(array $abstractSyntaxTree): bool
  {
    return $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_OPERATION_ADD
         || $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_OPERATION_SUBTRACT
         || $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_OPERATION_MULTIPLY
         || $abstractSyntaxTree[self::KEY_TYPE] === self::TYPE_OPERATION_DIVIDE;
  }

  /**
   * @param array $abstractSyntaxTree
   * @return string
   * @psalm-return self::TYPE_OPERATION_ADD | self::TYPE_OPERATION_SUBTRACT | self::TYPE_OPERATION_MULTIPLY | self::TYPE_OPERATION_DIVIDE
   */
  public static function getOperationType(array $abstractSyntaxTree): string
  {
    return $abstractSyntaxTree[self::KEY_TYPE];
  }

  public static function getOperationPriority(string $operation): int
  {
    return match ($operation) {
      self::TYPE_OPERATION_ADD, self::TYPE_OPERATION_SUBTRACT => 1,
      self::TYPE_OPERATION_MULTIPLY, self::TYPE_OPERATION_DIVIDE => 2,
      default => 0,
    };
  }

  public static function getOperationArgument1(array $abstractSyntaxTree): array
  {
    return $abstractSyntaxTree[self::KEY_OPERATION_ARGUMENT_1];
  }

  public static function getOperationArgument2(array $abstractSyntaxTree): array
  {
    return $abstractSyntaxTree[self::KEY_OPERATION_ARGUMENT_2];
  }
}

class AssemblyConverter
{
  /**
   * @var string[]
   */
  private array $assemblyCommands;

  public function __construct(private array $abstractSyntaxTree)
  {
    $this->assemblyCommands = $this->computeAssemblyCommands();
  }

  /**
   * @return string[]
   */
  private function computeAssemblyCommands(): array
  {
    return $this->getCommandsToComputeTreeToR0($this->abstractSyntaxTree);
  }

  /**
   * @param array $abstractSyntaxTree
   * @return string[]
   * @psalm-return list<string>
   */
  private function getCommandsToComputeTreeToR0(array $abstractSyntaxTree): array
  {
    if (AbstractSyntaxTreeUtils::isArgumentIndex($abstractSyntaxTree)) {
      $commands = [
        AssemblyUtils::Load_Argument_To_R0(AbstractSyntaxTreeUtils::getArgumentIndex($abstractSyntaxTree))
      ];
    } elseif (AbstractSyntaxTreeUtils::isConstantValue($abstractSyntaxTree)) {
      $commands = [
        AssemblyUtils::Load_Constant_To_R0(AbstractSyntaxTreeUtils::getConstantValue($abstractSyntaxTree))
      ];
    } elseif (AbstractSyntaxTreeUtils::isOperation($abstractSyntaxTree)) {
      $treeOfArgument1 = AbstractSyntaxTreeUtils::getOperationArgument1($abstractSyntaxTree);
      $commandsForArgument1 = $this->getCommandsToComputeTreeToR0($treeOfArgument1);

      $treeOfArgument2 = AbstractSyntaxTreeUtils::getOperationArgument2($abstractSyntaxTree);
      $commandsForArgument2 = $this->getCommandsToComputeTreeToR0($treeOfArgument2);

      $commandForOperation = $this->getOperationCommand(AbstractSyntaxTreeUtils::getOperationType($abstractSyntaxTree));

      if (AbstractSyntaxTreeUtils::isOperation($treeOfArgument1)) {
        $commands = [
          ...$commandsForArgument1,
          AssemblyUtils::Push_R0(),
          ...$commandsForArgument2,
          AssemblyUtils::Swap_R0_R1(),
          AssemblyUtils::Pop_To_R0(),
          $commandForOperation,
        ];
      } else {
        $commands = [
          ...$commandsForArgument2,
          AssemblyUtils::Swap_R0_R1(),
          ...$commandsForArgument1,
          $commandForOperation,
        ];
      }
    } else {
      throw new \LogicException('Bad program');
    }

    return $commands;
  }

  private function getOperationCommand(string $op): string
  {
    switch ($op) {
      case AbstractSyntaxTreeUtils::TYPE_OPERATION_ADD:
        return AssemblyUtils::Add_R1_To_R0();
      case AbstractSyntaxTreeUtils::TYPE_OPERATION_SUBTRACT:
        return AssemblyUtils::Subtract_R1_From_R0();
      case AbstractSyntaxTreeUtils::TYPE_OPERATION_MULTIPLY:
        return AssemblyUtils::Multiply_R0_By_R1();
      case AbstractSyntaxTreeUtils::TYPE_OPERATION_DIVIDE:
        return AssemblyUtils::Divide_R0_By_R1();
    }

    throw new \LogicException('Bad operation \'' . $op . '\'');
  }

  /**
   * @return string[]
   * @psalm-return list<string>
   */
  public function getAssemblyCommands(): array
  {
    return $this->assemblyCommands;
  }
}

class AssemblyUtils
{
  public static function Load_Constant_To_R0(int|float $constant): string
  {
    return 'IM ' . $constant;
  }

  public static function Load_Argument_To_R0(int $argumentIndex): string
  {
    return 'AR ' . $argumentIndex;
  }

  public static function Swap_R0_R1(): string
  {
    return 'SW';
  }

  public static function Push_R0(): string
  {
    return 'PU';
  }

  public static function Pop_To_R0(): string
  {
    return 'PO';
  }

  public static function Add_R1_To_R0(): string
  {
    return 'AD';
  }

  public static function Subtract_R1_From_R0(): string
  {
    return 'SU';
  }

  public static function Multiply_R0_By_R1(): string
  {
    return 'MU';
  }

  public static function Divide_R0_By_R1(): string
  {
    return 'DI';
  }
}

class CompilerKeywords
{
  public const FUNCTION_PARAMETERS_START = '[';
  public const FUNCTION_PARAMETERS_STOP  = ']';
  public const OPERATOR_ADD              = '+';
  public const OPERATOR_SUBTRACT         = '-';
  public const OPERATOR_MULTIPLY         = '*';
  public const OPERATOR_DIVIDE           = '/';
  public const SUB_EXPRESSION_START      = '(';
  public const SUB_EXPRESSION_STOP       = ')';
}
              

###############################################
        class Compiler
{
    const OPERATOR_ASSEMBLY_DICT = array(
        '+' => 'AD',
        '-' => 'SU',
        '*' => 'MU',
        '/' => 'DI',
    );

    const OPERATOR_PRECEDENCE_GROUPS = array(array('+', '-'), array('*', '/'));

    public function compile($program)
    {
        return pass3(pass2(pass1($program)));
    }

    public function tokenize($program)
    {
        /*
         * Turn a program string into an array of tokens.  Each token
         * is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
         * name or a number (as a string)
         */
        $tokens = preg_split('/\s+/', trim(preg_replace('/([-+*\/\(\)\[\]])/', ' $1 ', $program)));
        foreach ($tokens as &$token) {
            if (is_numeric($token)) {
                $token = intval($token);
            }
        }
        return $tokens;
    }

    public function pass1(String $program): array
    {
        // Returns an un-optimized AST
        $tokens = $this->tokenize($program);
        $args = $this->get_args($tokens);
        $expr = $this->get_expr($tokens);
        $ast = $this->get_abstract_syntax_tree($expr, $args);
        return $ast;
    }

    public function pass2(array $ast): array
    {
        // Returns an AST with constant expressions reduced
        if (in_array($ast['op'], array('imm', 'arg'), true)) {
            return $ast;
        }
        $ast['a'] = $this->pass2($ast['a']);
        $ast['b'] = $this->pass2($ast['b']);
        if ($ast['a']['op'] === 'imm' && $ast['b']['op'] === 'imm') {
            $a = $ast['a']['n'];
            $b = $ast['b']['n'];
            switch ($ast['op']) {
            case '+': $value = $a + $b; 
                break;
            case '-': $value = $a - $b; 
                break;
            case '*': $value = $a * $b; 
                break;
            case '/': $value = $a / $b; 
                break;
            }
            return array(
            'op' => 'imm',
            'n' => $value
            );
        }
        return $ast;
    }
    
    public function pass3(array $ast): array
    {
        // Returns assembly instructions
        $assembly = array();

        foreach(array('a', 'b') as $operand) {
            if($ast[$operand]['op'] === 'imm') {
                $assembly[] = 'IM ' . $ast[$operand]['n'];
                $assembly[] = 'PU';
            } elseif($ast[$operand]['op'] === 'arg') {
                $assembly[] = 'AR ' . $ast[$operand]['n'];
                $assembly[] = 'PU';
            } else {
                $assembly = array_merge($assembly, $this->pass3($ast[$operand]));
            }
        }
        
        $assembly[] = 'PO';
        $assembly[] = 'SW';
        $assembly[] = 'PO';
        $assembly[] = self::OPERATOR_ASSEMBLY_DICT[$ast['op']];
        $assembly[] = 'PU';

        return $assembly;
    }
  
    private function get_args(array $tokens): array
    {
        $args = array();
        foreach ($tokens as $token) {
            if ($token === ']') {
                break;
            }
            if ($token !== '[') {
                $args[] = $token;
            }
        }
        return array_flip($args);
    }
  
    private function get_expr(array $tokens): array
    {
        return array_slice($tokens, 1 + array_search(']', $tokens, true));
    }
  
    private function get_abstract_syntax_tree(array $expr, array $args): array
    {
        $expr = $this->strip_redundant_outer_brackets($expr);
    
        if (sizeof($expr) === 1) {
            return $this->get_imm_or_arg_leaf($expr, $args);
        }
    
        list('a' => $a, 'b' => $b, 'operator' => $operator) = $this->get_expr_a_and_b_with_operator($expr);
    
        $a = $this->get_abstract_syntax_tree($a, $args);
        $b = $this->get_abstract_syntax_tree($b, $args);
        return array(
        'op' => $operator,
        'a' => $a,
        'b' => $b,
        );
    }
  
    private function strip_redundant_outer_brackets(array $expr): array
    {
        $first_token = $expr[0];
        if ($first_token === '(') {
            $open_bracket_index = 0;
            $nesting_depth = 1;
            foreach ($expr as $index => $token) {
                if ($index === 0) {
                    continue;
                }
                if ($token === '(') {
                    $nesting_depth++;
                } elseif ($token === ')') {
                    $nesting_depth--;
                    if ($nesting_depth === 0) {
                        if ($index === array_key_last($expr)) {
                            return array_slice($expr, 1, -1);
                        } else {
                            break;
                        }
                    }
                }
            }
        }
        return $expr;
    }
  
    private function get_expr_a_and_b_with_operator(array $expr): array
    {
        foreach (self::OPERATOR_PRECEDENCE_GROUPS as $operator_precedence_group) {
            $nesting_depth = 0;
            for ($i = array_key_last($expr); $i > 0; $i--) {
                $token = $expr[$i];
                if ($token === ')') {
                    $nesting_depth++;
                } elseif ($token === '(') {
                    $nesting_depth--;
                } elseif ($nesting_depth === 0 && in_array($token, $operator_precedence_group, true)) {
                    return array(
                    'a' => array_slice($expr, 0, $i),
                    'b' => array_slice($expr, $i+1),
                    'operator' => $token
                    );
                }
            }
        }
    }
  
    private function get_imm_or_arg_leaf(array $token, array $args): array
    {
        list($token) = $token;
        if (in_array($token, array_keys($args), true)) {
            return array(
            'op' => 'arg',
            'n' => $args[$token]
            );
        }
        return array(
        'op' => 'imm',
        'n' => $token
        );
    }
}      
