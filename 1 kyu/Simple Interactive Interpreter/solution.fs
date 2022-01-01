open System

type Result<'T, 'E> = 
  | Success of 'T
  | Failure of 'E

module PLib =
  type Position = int

  type Input<'M> = {
    Str : string;
    Position : Position;
    EOF : bool;
    Meta : 'M
  }

  let moveInput input = 
    let lng = input.Str.Length
    if input.EOF then
      (None, input)
    else
      match input.Position with
      | x when x < lng - 1 -> (Some input.Str.[input.Position], { input with Position = input.Position + 1 })
      | _ -> (Some input.Str.[input.Position], { input with EOF = true })


  type ParserResult<'T, 'M> = Result<'T * Input<'M>, string>

  type Parser<'T, 'M> = {
    Fn: Input<'M> -> ParserResult<'T, 'M>
    Label: string
  }

  let inputFromStr meta value =
    { Str = value; Position = 0; EOF = false; Meta = meta }

  let runParser parser input =
    match parser.Fn input with
    | Success (s, i) -> Success (s, i)
    | Failure f -> Failure (sprintf "Parser '%s' failed at %i with: %s" parser.Label input.Position f)


  let runParserStr parser identifier str =
    inputFromStr identifier str
    |> runParser parser

  let printResult result =
    match result with
    | Success (r, _) -> printfn "OK: %O" r
    | Failure e -> printfn "Parse error: %s" e

  let createParser fn label =
    { Fn = fn; Label = label }

  let withLog parser =
    let fnWrap i =
      //printfn "Executing { %s } at pos %i." parser.Label i.Position
      let result = parser.Fn i
      //match result with
      //| Success (s, i) -> printfn "OK."
      //| Failure _ -> printfn "Failed."
      result
    { parser with Fn = fnWrap}
    
  let withLabel label parser =
    { parser with Label = label }

  let withLabelLog label parser = ((withLabel label) >> withLog) parser

  let returnP value =
    createParser (fun i -> Success (value, i)) (sprintf "return(%O)" value)

  let failP msg =
    createParser (fun i -> Failure msg) (sprintf "fail(%s)" msg)

  let bindP fn parser = 
    createParser 
      (fun input ->
        // printfn "Executing: %s, at %O" parser.Label input
        match runParser parser input with
        | Success (s, i) -> 
          let newParser = fn s
          runParser newParser i
        | Failure f -> 
          Failure f)
      (sprintf "bind(%s)" parser.Label)
  let ( >>= ) p fn = bindP fn p
  let ( =<< ) fn p = bindP fn p

  let bindMeta fn parser =
    createParser
      (fun input ->
        match runParser parser input with
        | Success (s, i) -> 
          let newParser = fn (s, input.Meta)
          runParser newParser i
        | Failure f -> 
          Failure f)
      (sprintf "bindMeta(%s)" parser.Label)
  let ( !>>= ) p fn = bindP fn p
  let ( =<<! ) fn p = bindP fn p

  let mapP fn = 
    bindP (fn >> returnP)

  let ( <!> ) = mapP
  let ( |>> ) x f = mapP f x

  let fullBindP fs ff parser =
    createParser 
      (fun input ->
        match runParser parser input with
        | Success (s, i) -> 
          let newParser = fs s
          runParser newParser i
        | Failure f -> 
          let npf = ff f
          runParser npf input)
      (sprintf "bind(%s)" parser.Label)

  let applyP fnp arg1 =
    fnp >>= (fun fx -> arg1 >>= (fx >> returnP) )

  let ( <*> ) = applyP

  let lift2 fn a b =
    returnP fn <*> a <*> b

  let pChar char =
    createParser 
      (fun input -> 
        let c, newInput = moveInput input
        match c with 
        | Some inputChar ->
          if inputChar = char then
            Success (char, newInput)
          else
            Failure (sprintf "Expected '%c' but got '%c'." char inputChar)
        | None ->
          Failure "Reached end of input.")
      (sprintf "'%c'" char)

  let andThen p1 p2 =
    { 
      (p1 >>= (fun s1 ->
      p2 |>> (fun s2 -> (s1, s2)))) 
      with
        Label = sprintf "%s && %s" p1.Label p2.Label 
    }

  let ( .>>. ) = andThen


  let orElse p1 p2 =
    createParser 
      (fun input ->
        match runParser p1 input with
        | Success (s1, i1) -> Success (s1, i1)
        | Failure f1 ->
          match runParser p2 input with
          | Success (s2, i2) -> Success (s2, i2)
          | Failure f2 -> Failure f2)
      (sprintf "%s || %s" p1.Label p2.Label)
  let ( <|> ) = orElse


  let choise parsers =
    List.reduce (<|>) parsers

  let anyOf charList =
    choise (List.map pChar charList)

  let rec sequence parserList =
    let concat h t = h::t
    let concatP = lift2 concat
    match parserList with
    | [] -> returnP []
    | head::tail ->
      concatP head (sequence tail)

  let ( >>. ) p1 p2 =
    p1 .>>. p2 |>> (fun (_, s2) -> s2)
    |> withLabel (sprintf "%s >>. %s" p1.Label p2.Label)

  let ( .>> ) p1 p2 =
    p1 .>>. p2 |>> (fun (s1, _) -> s1)
    |> withLabel (sprintf "%s .>> %s" p1.Label p2.Label)

  let between p1 p2 p3 =
    p1 >>. p2 .>> p3
    |> withLabel (sprintf "%s >>. %s .>> %s" p1.Label p2.Label p3.Label)

  let rec private parseZeroOrMore limit parser input =
    match runParser parser input with
    | Failure _ -> Success ([], input)
    | Success (s, i) ->
      match limit with
      | 0 ->
        Success ([], input)
      | _ ->
        match parseZeroOrMore (if limit = -1 then -1 else limit - 1) parser i with
        | Failure _ -> 
          Success ([s], i)
        | Success (s1, i1) ->
          Success (s::s1, i1)
  
  let rec private parseExactRange amount parser input =
    if amount = 0 then
      Success ([], input)
    else
      match runParser parser input with
      | Failure _ -> Failure "Unable to parse exact amount"
      | Success (s, i) ->
        match parseExactRange (amount - 1) parser i with
        | Failure _ -> Failure "Unable to parse exact amount"
        | Success (s1, i1) ->
          Success (s::s1, i1)

  let many parser =
    createParser 
      (parseZeroOrMore -1 parser)
      (sprintf "many(%s)" parser.Label)
      
  let manyTake take parser =
    createParser 
      (parseZeroOrMore take parser)
      (sprintf "many(%s)" parser.Label)

  let manyExact take parser =
    createParser
      (parseExactRange take parser)
      (sprintf "many-e(%s)" parser.Label)

  let many1 parser =
    createParser
      (fun input -> 
        match runParser parser input with
        | Failure f -> Failure f
        | Success (s, i) -> 
          match parseZeroOrMore -1 parser i with
          | Success (s1, i1) ->
            Success (s::s1, i1)
          | Failure _ ->
            Success ([s], i))
      (sprintf "many1(%s)" parser.Label)

  let opt parser =
    { 
      (fullBindP 
          (Some >> returnP)
          (fun _ -> returnP None)
          parser)
      with Label = sprintf "opt(%s)" parser.Label
    }

  let sepBy parser sep =
    opt parser >>= (fun so -> 
      match so with
      | Some s ->
        many (sep >>. parser) |>> (fun x -> s::x)
      | None -> returnP [])
    |> withLabel (sprintf "%s[(%s) %s]*" parser.Label sep.Label parser.Label)
    
  let rec sepByWTake take parser sep =
    opt parser >>= (fun so -> 
      match so with
      | Some s ->
        manyTake (take - 1) (sep >>. parser) |>> (fun x -> s::x)
      | None -> returnP [])
    |> withLabel (sprintf "%s[(%s) %s]*" parser.Label sep.Label parser.Label)
  
  let sepByExactRange amount parser sep =
    if amount = 0 then
      returnP []
    else
      parser >>= (fun s ->
          manyExact (amount - 1) (sep >>. parser) |>> (fun x -> s::x))
      |> withLabel (sprintf "%s[(%s) %s]{%i}" parser.Label sep.Label parser.Label (amount - 1))

  let sepBy1 parser sep =
    parser .>>. many (sep >>. parser)
    |>> fun (p,pList) -> p::pList
    |> withLabel (sprintf "%s[(%s) %s]+" parser.Label sep.Label parser.Label)

  let toString charList = 
    String(charList |> Array.ofList)

  let asList parser =
    parser
    |>> (fun x -> [x])

  let pString str =
    str 
    |> Seq.map pChar
    |> List.ofSeq
    |> sequence
    |>> toString

  let createParserForwardedToRef<'t, 'm>() =
      let dummyParser= 
          let innerFn input : ParserResult<'t, 'm> = failwith "unfixed forwarded parser"
          {Fn=innerFn; Label="unknown"}
      let parserRef = ref dummyParser 

      let innerFn input = 
          runParser !parserRef input 
      let wrapperParser = {Fn=innerFn; Label="unknown"}
      wrapperParser, parserRef


module ExpressionModel =
  type Operator =
    | Add
    | Sub
    | Multiply
    | Divide
    | Module

  type Expression =
    {
      Left : Factor
      Operator : Operator
      Right : ExprOrFactor
    }

  and ExprOrFactor =
    | Expression of Expression
    | Factor of Factor

  and FunctionDef =
    {
      Name : string
      Parameters : string list
      Body : ExprOrFactor
    }

  and Factor =
    | Number of float
    | Variable of string
    | FunctionCall of string * ExprOrFactor list
    | Assignment of string * ExprOrFactor
    | Grouped of ExprOrFactor

  and Input =
    | FuncDef of FunctionDef
    | Expr of ExprOrFactor

  type Identity = 
    | Function of int 
    | Variable


module Rpn =
  open ExpressionModel
  type RpnItem = 
    | Num of float
    | Operation of Operator
    
  type Rpn =
    {
      PendingOperations : Operator list
      ReversedItems : RpnItem list
    }

  let initRpn =
    {
      PendingOperations = []
      ReversedItems = []
    }

  let getOperatorOrder op =
    match op with
    | Multiply | Divide | Module -> 1
    | Add | Sub -> 2
    
  let calc x y op =
    match op with
    | Add -> x + y
    | Sub -> x - y
    | Multiply -> x * y
    | Divide -> if (y <> 0.0) then x / y else failwith "ERROR: Unable to divide by zero."
    | Module -> x % y
  
  let reduceRpn existingItems opps = 
    opps
    |> List.rev
    |> List.fold 
      (fun items op -> 
        match items with
        | x::y::rest ->
          match x, y with
          | Num r, Num l ->
            let res = calc l r op
            (Num res)::rest
          | _ ->
            failwith "ERROR: Unbale to evaluate"
        | _ ->
          failwith "ERROR: Unbale to evaluate")
      existingItems

  let recreateRpn newEntry rpn =
    let rec addOperation pending newOp =
      match pending with
      | [] ->
        [newOp], []
      | h::t ->
        if getOperatorOrder newOp >= getOperatorOrder h then
          let newPending, toAdd = addOperation t newOp
          newPending, List.rev (h::toAdd)
        else
          newOp::pending, []

    match newEntry with
    | Operation o -> 
      let newPending, toEval = addOperation rpn.PendingOperations o
      let calculatedItems = reduceRpn rpn.ReversedItems toEval
      { rpn with PendingOperations = newPending; ReversedItems = calculatedItems }
    | Num n ->
      { rpn with ReversedItems = (Num n)::rpn.ReversedItems }

  let calcRpn rpn =
    match reduceRpn rpn.ReversedItems (List.rev rpn.PendingOperations) with
    | [Num x] -> Success x
    | _ -> Failure "Ivalid RPN."


module Parser =
  open PLib
  open ExpressionModel

  let whitespace = anyOf [' ';'\t']
  let whitespaces = many whitespace |> withLabelLog "wss"
  let whitespaces1 = many1 whitespace |> withLabelLog "wss1"
  let digit = anyOf ['0'..'9']
  let letter = anyOf (['a'..'z'] @ ['A'..'Z']) 
  let number = 
    let withDot = 
      many digit .>>. (pChar '.' >>. many1 digit)
      |>> (fun (l1, l2) -> 
        let numStr = toString l1 + "." + toString l2
        float numStr)
    let withoutDot =
      many1 digit
      |>> (toString >> float)
    (withDot <|> withoutDot)
    |> withLabelLog "number"

  let letterOrUnderscore = letter <|> pChar '_'

  let identifier = 
    letterOrUnderscore .>>. many (letterOrUnderscore <|> digit)
    |>> (fun (l, rest) -> [l] @ rest |> toString)
    |> withLabelLog "identifier"

  let identifierWs =
    between whitespaces identifier whitespaces

  let assignOp = pChar '=' |> withLabelLog "="
  let arrowOp = pString "=>" |> withLabelLog "=>"
  let operator =
    choise [
      pChar '*' |>> (fun _ -> Multiply); 
      pChar '/' |>> (fun _ -> Divide); 
      pChar '%' |>> (fun _ -> Module); 
      pChar '+' |>> (fun _ -> Add);
      pChar '-' |>> (fun _ -> Sub);
    ]
    |> withLabelLog "operator"

  let expr, exprRef = createParserForwardedToRef<ExprOrFactor, string -> Identity option>()

  let functionCall =
    bindMeta
      (fun (id, identify: string -> Identity option) -> 
        match identify id with
        | Some (Function num) ->
          sepByExactRange num expr whitespaces1 
          |>> (fun x -> FunctionCall (id, x))
        | Some Variable ->
          failP (sprintf "%s is no a function" id)
        | None ->
          failP "Unexpected identifier")
      (identifier .>> whitespaces)

  let inBraces parser =
    between
      (pChar '(' .>>. whitespaces)
      parser
      (whitespaces .>>. pChar ')')

  let assignment =
    identifier .>> (between whitespaces assignOp whitespaces) .>>. expr
    |>> Assignment
    |> withLabelLog "F_assign"
  let grouped =
    inBraces (expr |> withLabelLog "(EXPR)")
    |>> Grouped
    |> withLabelLog "F_grouped"

  let variable =
    identifier
    |> bindMeta
      (fun (id, identify: string -> Identity option) -> 
        match identify id with
        | Some (Function _) ->
          failP "Expected identifier but got function"
        | Some Variable ->
          returnP id
        | None ->
          returnP id)
    |> withLabelLog "variable"
  let factor =
    choise [
      assignment;
      functionCall;
      number |>> Factor.Number |> withLabelLog "F_number";
      variable |>> Factor.Variable |> withLabelLog "F_variable";
      grouped ]
    |> withLabelLog "FACT"
  
  let fnIdentifier =
    between whitespaces1 identifier whitespaces
  let fnParams =
    sepBy identifier whitespaces1
  let arrowOpWs =
    between whitespaces arrowOp whitespaces
  let functionDef =
    pString "fn" >>. fnIdentifier .>>. fnParams .>> arrowOpWs .>>. expr
    |>> (fun ((name, parameters), expr) -> 
      FuncDef { Name = name; Parameters = parameters; Body = expr })
    |> withLabelLog "F_DEF"
  
  let private wsOperator = between whitespaces operator whitespaces

  let exprParser =
    let factorAndOptExpr = 
      (factor) .>>. opt (wsOperator .>>. expr)
      |>> (fun (left, right) -> 
        match right with
        | Some (op, ex) -> 
          Expression { Left = left; Operator = op; Right = ex}
        | None -> 
          Factor left)
    factorAndOptExpr
    |> withLabelLog "EXPR"
  exprRef := exprParser

  let inputParser =
    functionDef <|> (expr |>> Input.Expr)

  type ParsedInput =
    | OK of Input
    | Error of string

  let parseInputString identifier input =
    let res = runParserStr inputParser identifier input
    match res with
    | Success (data, i) ->
      if i.EOF then
        OK data
      else 
        Error (sprintf "Unexpected character '%c' at col: %i." i.Str.[i.Position] i.Position)
    | Failure f ->
      Error f


module Solution =
  open System.Collections.Generic
  open ExpressionModel
  open Rpn

  type EvaluationResult =
    | Value of float
    | NameConflict
    | UnknownIdentifier of string
    | InvalidArguments of int * int
    | Unexpected
    | EvaluationError of string

  type Scope = 
    {
      Functions : IDictionary<string, FunctionDef>
      Variables : IDictionary<string, float>
    }
    
  let asNullable (value: 'a) =
    new Nullable<'a>(value)

  let resultToFloatSafe result =
    match result with
    | Value v -> asNullable v
    | _ -> Nullable()

  let addOrUpdateDict (key: 'a) (value: 'b) (dict: IDictionary<'a, 'b>) =
    if dict.ContainsKey(key) then
      dict.[key] <- value
    else
      dict.Add(key, value)

  let rec getVariable varName scope =
    match Seq.tryFind (fun x -> x = varName) scope.Variables.Keys with
    | Some vn ->
      Some scope.Variables.[vn]
    | None ->
        None

  let optValueAsResult varName = function
    | Some v -> Value v
    | None -> UnknownIdentifier varName

  let rec getFunction funcName scope =
    match Seq.tryFind (fun x -> x = funcName) scope.Functions.Keys with
    | Some vn ->
      Some scope.Functions.[vn]
    | None ->
      None

  let initScope =
    {
      Functions = Dictionary<string, FunctionDef>();
      Variables = Dictionary<string, float>();
    }

  let rec evaluateExpressionOrFact exprScope exprOrFact =
    let callFunction funcDef args scope =
      let funcScope = initScope
      let rec fillScope argList i parentScope =
        match argList with
        | [] ->
          (true, None)
        | h::t ->
          match h with
          | Value v ->
            let argName = funcDef.Parameters.[i]
            addOrUpdateDict argName v funcScope.Variables |> ignore
            fillScope t (i + 1) parentScope
          | rest ->
            (false, Some rest)

      match fillScope args 0 scope with
      | true, _ ->
        evaluateExpressionOrFact funcScope funcDef.Body
      | false, None ->
        Unexpected
      | false, Some err ->
        err

    let evaluateFunctionCall name args scope =
      match getFunction name scope with
      | Some fdef ->
        let evaluatedArgs = args |> List.map (evaluateExpressionOrFact scope)
        callFunction fdef evaluatedArgs scope
      | None ->
        UnknownIdentifier name

    let evaluateFactor factor scope =
      match factor with
      | Factor.Number n -> 
        Value n
      | Factor.Variable id ->
        scope
        |> getVariable id 
        |> optValueAsResult id
      | Factor.FunctionCall (name, args) ->
        evaluateFunctionCall name args scope 
      | Factor.Assignment (name, value) ->
        match getFunction name scope with
        | Some _ -> 
          NameConflict
        | None ->
          match evaluateExpressionOrFact scope value with
          | Value evaluatedExpr -> 
            addOrUpdateDict name evaluatedExpr scope.Variables |> ignore
            Value evaluatedExpr
          | rest ->
            rest
      | Factor.Grouped grouped ->
        evaluateExpressionOrFact scope grouped

    let evaluateExpression expr scope =
      let rec visit exp rpn =
        match evaluateFactor exp.Left scope with
        | Value left ->
          let newRpn = 
            rpn
            |> recreateRpn (Num left)
            |>recreateRpn (Operation exp.Operator)
          match exp.Right with
          | Factor f ->
            match evaluateFactor f scope with
            | Value right ->
              Success (newRpn |> recreateRpn (Num right))
            | _ ->
              Failure "ERROR: Unable to evaluate"
          | Expression rexpr ->
            visit rexpr newRpn
        | _ ->
          Failure "ERROR: Unable to evaluate"

      match visit expr initRpn with
      | Success rpn ->
        match calcRpn rpn with
        | Success value ->
          Value value
        | Failure err ->
          EvaluationError err
      | Failure err ->
        EvaluationError err

    match exprOrFact with
    | Factor factor ->
      evaluateFactor factor exprScope
    | Expression expr ->
      evaluateExpression expr exprScope

  type Interpreter ()=
    let nullResult = new Nullable<float>()
    let mutable rootScope = initScope

    let validateFuncDef fd =
      let rec valiadteBody exprOrFact = 
        match exprOrFact with
        | Factor f ->
          match f with
          | Factor.Variable v -> 
            List.contains v fd.Parameters
          | _ -> true
        | Expression expr ->
          valiadteBody (Factor expr.Left) 
            && valiadteBody expr.Right

      if not (valiadteBody fd.Body) then
        failwith "ERROR: Unknown identifier in function body."

    let declareFunction fd =
      if rootScope.Variables.ContainsKey(fd.Name) then
        failwithf "ERROR: Name conflict. Variable '%s' is already defined." fd.Name
      do validateFuncDef fd
      if rootScope.Functions.ContainsKey(fd.Name) then
        rootScope.Functions.[fd.Name] <- fd
      else
        rootScope.Functions.Add(fd.Name, fd)
      nullResult

    let identificator name =
      match getVariable name rootScope with
      | None ->
        match getFunction name rootScope with
        | None -> None
        | Some f -> Some (Identity.Function f.Parameters.Length)
      | Some _ -> Some Identity.Variable

    member this.input (input: string) : Nullable<float> =
      let parsed = Parser.parseInputString identificator (input.Trim())

      match parsed with
      | Parser.OK model ->
        match model with
        | FuncDef fd ->
          declareFunction fd
        | Expr expr -> 
          match evaluateExpressionOrFact rootScope expr with
          | Value v ->
            asNullable v
          | NameConflict ->
            failwith "ERROR: Name conflict."
          | UnknownIdentifier ui ->
            failwithf "ERROR: Unknown identifier '%s'." ui
          | InvalidArguments (expected, got) ->
            failwithf "ERROR: Invalid amount of argumets. Expected %i but got %i." expected got
          | Unexpected ->
            failwith "ERROR: Unexpected error."
          | EvaluationError err ->
            failwithf "ERROR: Evaluation error: %s." err
      | Parser.Error err ->
        failwithf "ERROR: %s" err
        
___________________________________________________________________________
module Solution = begin
  open System
  open System.Text.RegularExpressions
  open System.Collections.Generic

  type Operator = Plus | Minus | Mul | Div | Mod | Eq
  type Expression =
    | Num of float | Ident of string | Expr of Expression * Operator * Expression
    | Parens of Expression | Call of string * Expression list
  type StackPart = Ex of Expression | Op of Operator | OpParen | Sig of string * string list | FnName of string * int

  type Interpreter ()=
    let tokenize input = 
        [for i in (new Regex("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)")).Matches(input) -> i.Groups.[0].Value]

    let globals = new Dictionary<string, float>()
    let functions = new Dictionary<string, string list * Expression>()

    let (|ReduceCall|_|) (stack:StackPart list) =
        match stack with
        | FnName(name, 0)::_stack -> Some (Ex(Call(name, []))::_stack)
        | Ex expr1::FnName(name, 1)::_stack -> Some (Ex(Call(name, [expr1]))::_stack)
        | Ex expr2::Ex expr1::FnName(name, 2)::_stack -> Some (Ex(Call(name, [expr1; expr2]))::_stack)
        | Ex expr3::Ex expr2::Ex expr1::FnName(name, 3)::_stack -> Some (Ex(Call(name, [expr1; expr2; expr3]))::_stack)
        | _ -> None

    let (|ReducePrecedence|_|) (stack:StackPart list) =
        let needRotate op1 op2 =
            match op2 with
            | Mul | Div | Mod ->
                match op1 with
                | Plus | Minus | Eq -> true
                | _ -> false
            | Plus | Minus | Eq ->
                match op1 with
                | Eq -> true
                | _ -> false
        match stack with
        | Ex(Expr(Expr(expr1, op1, expr2), op2, expr3))::_stack when needRotate op1 op2 ->
            let newExpr = Expr(expr1, op1, (Expr(expr2, op2, expr3)))
            Some (Ex newExpr::_stack)
        | _ -> None

    let (|ReduceExpression|_|) (stack:StackPart list) =
        match stack with
        | Ex expr2::Op op::Ex expr1::_stack ->
            let newExpr = Expr(expr1, op, expr2)
            Some (Ex newExpr::_stack)
        | _ -> None

    let (|Number|_|) (tokens:string list) =
        match tokens with
        | number::rest ->
            match Double.TryParse number with
            | true, value -> Some (Num value, rest)
            | _ -> None
        | _ -> None

    let (|Operator|_|) (tokens:string list) =
        match tokens with
        | "+"::rest -> Some (Plus, rest) | "-"::rest -> Some (Minus, rest) | "*"::rest -> Some (Mul, rest)
        | "/"::rest -> Some (Div, rest) | "%"::rest -> Some (Mod, rest) | "="::rest -> Some (Eq, rest)
        | _ -> None

    let (|OpenParen|_|) (tokens:string list) =
        match tokens with
        | "("::rest -> Some (rest)
        | _ -> None

    let (|CloseParen|_|) (tokens:string list) =
        match tokens with
        | ")"::rest -> Some (rest)
        | _ -> None

    let (|Function|_|) (tokens:string list) =
        match tokens with
        | "fn"::name::rest ->
            let rec extractParams pars = function
                | "=>"::rest -> (pars |> List.rev, rest)
                | name::rest -> extractParams (name::pars) rest
                | _ -> failwith "Error"
            let pars, rest = extractParams [] rest
            Some (name, pars, rest)
        | _ -> None

    let (|FunctionCall|_|) (tokens:string list) =
        match tokens with
        | ident::rest ->
            match rest with
            | "="::_ -> None
            | _ ->
                match functions.TryGetValue ident with
                | true, (pars, _) -> Some (ident, List.length pars, rest)
                | _ -> None
        | _ -> None

    let (|Identifier|_|) (tokens:string list) =
        match tokens with
        | ident::rest -> Some (Ident ident, rest)
        | _ -> None

    let rec parse stack tokens =
        match stack with
        | ReduceCall _stack
        | ReducePrecedence _stack
        | ReduceExpression _stack -> parse _stack tokens
        | _ ->
            match tokens with
            | Number (number, rest) ->
                match stack with
                | Op op::Ex left::_stack -> parse (Ex(Expr(left, op, number))::_stack) rest
                | _ -> parse (Ex number::stack) rest
            | Operator (op, rest) -> parse (Op op::stack) rest
            | OpenParen rest -> parse (OpParen::stack) rest
            | CloseParen rest ->
                match stack with
                | Ex expr::OpParen::_stack -> parse (Ex(Parens expr)::_stack) rest
                | _ -> None
            | Function (name, pars, rest) -> parse (Sig(name, pars)::stack) rest
            | FunctionCall (name, num, rest) -> parse (FnName(name, num)::stack) rest
            | Identifier (ident, rest) ->
                match stack with
                | Op op::Ex left::_stack -> parse (Ex(Expr(left, op, ident))::_stack) rest
                | _ -> parse (Ex ident::stack) rest
            | [] -> stack |> List.rev |> Some
            | _ -> None

    let rec evalExpr expr (locals:IDictionary<string, float option>) =
        match expr with
        | Expr(Ident ident, Eq, expr) ->
            match functions.TryGetValue ident with
            | true, _ -> None
            | _ ->
                match evalExpr expr locals with
                | Some res ->
                    match globals.TryGetValue ident with | true, _ -> globals.[ident] <- res | _ -> globals.Add(ident, res)
                    Some res
                | _ -> None
        | Expr(expr1, op, expr2) ->
            match evalExpr expr1 locals, evalExpr expr2 locals with
            | Some res1, Some res2 ->
                let func = match op with | Plus -> (+) | Minus -> (-) | Mul -> (*) | Div -> (/) | Mod -> (%) | _ -> fun _ v -> v
                func res1 res2 |> Some
            | _ -> None
        | Num num -> Some num
        | Ident ident ->
            match locals.TryGetValue ident with
            | true, value -> value
            | _ ->
                match globals.TryGetValue ident with
                | true, value -> Some value
                | _ -> None
        | Parens expr -> evalExpr expr locals
        | Call(name, exprs) ->
            let results = exprs |> List.map (fun expr -> evalExpr expr locals)
            match functions.TryGetValue name with
            | true, (pars, expr) ->
                let locals = dict(List.zip pars results)
                evalExpr expr locals
            | _ -> None

    member this.input input : Nullable<float> =
        let tokens = tokenize input
        let tree = parse [] tokens
        match tree with
        | Some([Ex expr]) ->
            match evalExpr expr (dict[]) with
            | Some res -> new Nullable<float>(res)
            | _ -> new Nullable<float>()
        | Some(Sig(name, pars)::Ex expr::_) ->
            match functions.TryGetValue name with | true, _ -> functions.[name] <- (pars, expr) | _ -> functions.Add(name, (pars, expr))
            new Nullable<float>()
        | _ -> new Nullable<float>()
end

___________________________________________________________________________
module Solution = begin

  open System
  open System.Text.RegularExpressions
  open System.Collections.Generic
  
  let flip f x y = f y x
  let curry f a b = f (a, b)
  let const' x _ = x
  let cons h t = h :: t
  
  type Parser<'b, 'a> = Parser of ('b list -> ('a * 'b list) option)
  
  let runParser (Parser f) = f
  
  let parse (p: Parser<'b, 'a>) (s: seq<'b>) : 'a =
    match runParser p (Seq.toList s) with
    | Some (v, _) -> v
    | _ -> failwith "No parse"
  
  let value a = Parser (fun s -> Some (a, s))
  
  let (>>=) p f =
    Parser (fun s ->
      match runParser p s with
      | Some (v, s') -> runParser (f v) s'
      | None -> None)
  
  let empty = Parser (fun _ -> None)
  
  type ParserBuilder() =
    member x.Bind(p, f) = p >>= f
    member x.Return(v) = value v
    member x.ReturnFrom(p) = p
    member x.Zero() = empty
  
  let parser = ParserBuilder()
  
  let (<%>) f p = p >>= (f >> value)
  let (<%) v p = const' v <%> p
  let (<*>) p1 p2 = p1 >>= flip (<%>) p2
  let ( *> ) p1 p2 = p1 >>= (fun _ -> p2)
  let ( <* ) p1 p2 = p1 >>= (fun v -> p2 *> value v)
  
  let (<|>) p q =
    Parser (fun s ->
      match runParser p s with
      | None -> runParser q s
      | res -> res)
  
  let rec replicate n p =
    if n <= 0 then
      value []
    else
      cons <%> p <*> replicate (n - 1) p
  
  let item = Parser (function [] -> None | h :: t -> Some(h, t))
  let eof = Parser (function [] -> Some((), []) | _ -> None)
  let satisfy pred = item >>= fun c -> if pred c then value c else empty
  
  let chainl1 (p: Parser<'s, 'a>) (op: Parser<'s, 'a -> 'a -> 'a>) : Parser<'s, 'a> =
    let rec rest a = (op <*> value a <*> p >>= rest) <|> value a
    p >>= rest
  
  let delay p arg = Parser (fun s -> runParser (p arg) s)
  
  let rec many1 p = cons <%> p <*> many p
  and     many  p = delay many1 p <|> value []
  
  let oneOf s = satisfy (flip Seq.contains s)
  let token c = satisfy ((=) c)
  
  type Function = 
    { Arguments : string list
      Body : string list }
  
  type Environment = 
    { Variables : IDictionary<string, float>
      Functions : IDictionary<string, Function> }
    static member Empty = { Variables = Dictionary(); Functions = Dictionary() }
  
  let number = float <%> satisfy (fun (t: string) -> Char.IsNumber t.[0])
  let identifier = satisfy (fun (t: string) -> Char.IsLetter t.[0])
  let op (f: float -> float -> float) tok = f <% token tok
  
  let rec variable env = 
    parser {
      let! name = identifier
      if env.Variables.ContainsKey name then
        return env.Variables.[name]
      elif env.Functions.ContainsKey name then
        let f = env.Functions.[name]
        let! args = replicate (List.length f.Arguments) (expr env)
        return evalFunc f args
      else
        failwith ("Undefined variable: " + name)
    }
  and assignment env =
    parser {
      let! name = identifier <* token "="
      let! v = expr env
      if env.Functions.ContainsKey name then
        failwith ("Variable " + name + " overrides an existing function")
      else
        env.Variables.[name] <- v
        return v
    }
  and funcDecl env =
    parser {
      let! name = token "fn" *> identifier
      let! args = many identifier <* token "=>"
      let! body = many item
      if env.Variables.ContainsKey name then
        failwith ("Function " + name + " overrides an existing variable")
      else
        let f = { Arguments = args; Body = body }
        env.Functions.[name] <- f
        evalFunc f (Seq.initInfinite (const' 0.0)) |> ignore
        return Nullable<float>()
    }
  and factor env = number <|> variable env <|> (token "(" *> delay expr env <* token ")")
  and term   env = chainl1 (factor env) (op ( * ) "*" <|> op ( / ) "/" <|> op ( % ) "%")
  and expr   env = assignment env <|> chainl1 (term env) (op ( + ) "+" <|> op ( - ) "-")
  and evalFunc f (xs: seq<float>) =
    let env = { Environment.Empty with Variables = Seq.zip f.Arguments xs |> dict }
    parse (expr env <* eof) f.Body
  
  let result env = funcDecl env <|> (Nullable<float> <%> expr env <* eof)
  
  type Interpreter () =
    let tokenize input = 
        [for i in Regex(@"=>|[-+*/%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\.?[0-9]+)").Matches(input) -> i.Groups.[0].Value]
    
    let environment = Environment.Empty
  
    member this.input input : Nullable<float> =
        let tokens = tokenize input
        parse (result environment) tokens

end

___________________________________________________________________________
open System
open System.Text.RegularExpressions

type Operator = Add | Subtract | Multiply | Divide | Modulo

type Expression =
    | Number of double
    | Identifier of string
    | Assignment of string * Expression
    | FunctionCall of string * Expression list
    | Operation of Operator * Expression * Expression

type FunctionDefinition = 
    | FunctionDefinition of string * string list * Expression

type ParseResult = 
    | FVal of FunctionDefinition
    | Val of Expression
    | ParseError of string

let matchToken pattern input =
    let m = Regex.Match(input, sprintf @"^\s*(%s)(.*)" pattern)
    if m.Success then Some(m.Groups.[1].Value, m.Groups.[2].Value)
    else None
    
let (|ID|_|) = matchToken "[A-Za-z_][A-Za-z0-9_]*"
let (|NUM|_|) = matchToken @"[0-9]*\.?[0-9]+" >> Option.map (fun (x, rest) -> float x, rest)
    
let matchSymbol pattern input = matchToken pattern input |> Option.map snd

let (|ADD|_|) = matchSymbol @"\+"
let (|SUB|_|) = matchSymbol "-" 
let (|MUL|_|) = matchSymbol @"\*"
let (|MOD|_|) = matchSymbol "%"
let (|DIV|_|) = matchSymbol "/"
let (|LPAREN|_|) = matchSymbol @"\("
let (|RPAREN|_|) = matchSymbol @"\)"
let (|FN|_|) = matchSymbol "fn"
let (|EQUALS|_|) = matchSymbol "="
let (|ARR|_|) = matchSymbol "=>"

let (|FACTOP|_|) = function 
    | MUL rest -> Some(Multiply, rest) 
    | DIV rest -> Some(Divide, rest)
    | MOD rest  -> Some(Modulo, rest)
    | _ -> None

let (|SUMOP|_|) = function 
    | ADD rest -> Some(Add, rest) 
    | SUB rest -> Some(Subtract, rest)
    | _ -> None

let rec (|MANY|_|) f acc input =
    match f input with
    | Some(x, rest) -> (|MANY|_|) f (x::acc) rest
    | None -> Some(acc, input)

let rec (|EXACTLY|_|) n f acc input =
    match f input with
    | _ when acc |> List.length = n -> Some(acc, input)
    | Some(x, rest) -> (|EXACTLY|_|) n f (x::acc) rest
    | None -> None

let (|EOL|_|) input = if String.IsNullOrWhiteSpace input then Some() else None

let (|EXPRFULL|_|) vs fs = 
    let rec (|FACTOR|_|) = function
        | NUM (x, rest) -> Some (Number x, rest)
        | FNCALL(fc, rest) -> Some (fc, rest)
        | ID( n, EQUALS( EXPR(e, rest))) -> Some(Assignment(n, e), rest)
        | ID (id, rest) ->
            if vs |> List.contains id 
            then Some (Identifier id, rest)
            else failwithf "Unknown identifier '%s'." id
        | LPAREN( EXPR(e, RPAREN( rest))) -> Some (e, rest)
        | _ -> None

    and (|FNCALL|_|) = function
        | ID(fn, rest) when fs |> Map.containsKey fn ->
            let (FunctionDefinition(_, argIds, _)) = fs.[fn]
            let n = argIds.Length 
            match rest with
            | EXACTLY n (|EXPR|_|) [] (args, rest) -> Some(FunctionCall(fn, args), rest)
            | _ -> failwithf "Function '%s' expects %d arguments." fn n
        | _ -> None

    and factorExprs = function FACTOP(op, FACTOR(e, rest)) -> Some((op, e), rest) | _ -> None
    and sumExprs = function SUMOP(op, TERM(e, rest)) -> Some((op, e), rest) | _ -> None

    and (|TERM|_|) = function
        | FACTOR(e1, MANY factorExprs [] (exprs, rest)) ->
            match exprs |> List.rev with
            | [] -> Some(e1, rest)
            | exprs ->
                Some ((e1, exprs) ||> List.fold(fun acc (op, e) -> Operation(op, acc, e)), rest)
        | _ -> None

    and (|EXPR|_|) = function
        | TERM(e1, MANY sumExprs [] (exprs, rest)) ->
            match exprs |> List.rev with
            | [] -> Some(e1, rest)
            | exprs ->
                Some ((e1, exprs) ||> List.fold(fun acc (op, e) -> Operation(op, acc, e)), rest)
        | _ -> None

    function EXPR(e, EOL) -> Some e | _ -> None
    
let (|FUNC|_|) fs = function
    | FN( ID( name, MANY (|ID|_|) [] (args, ARR(rest)))) ->
        match rest with
        | EXPRFULL args fs (e) -> Some( FunctionDefinition(name, args, e))
        | _ -> failwith "Syntax error in function body."
    | _ -> None

let parse vs fs = function
    | FUNC fs (f) -> FVal f
    | EXPRFULL vs fs (e) -> Val e
    | _ -> ParseError "Syntax error."

let rec compute vs fs updatedVs expr =
    match expr with
    | Number x -> (x, updatedVs)
    | Identifier id -> (vs |> Map.find id, updatedVs)
    | Assignment (id, expr) ->
        let (x, uvs) = compute vs fs updatedVs expr
        x, (id, x)::uvs 
    | FunctionCall (name, argExprs) ->
        let (FunctionDefinition(_, argNames, fbody)) = fs |> Map.find name
        let computedArgs = 
          [ for name, expr in Seq.zip argNames argExprs do
                let (x, uvs) = compute vs fs updatedVs expr 
                yield (name, x), uvs ]
        let (args, uvsList) = computedArgs |> List.unzip
        let (result, _) = compute (Map args) fs updatedVs fbody
        result, List.concat uvsList
    | Operation (op, e1, e2) ->
        match compute vs fs updatedVs e1, compute vs fs updatedVs e2 with
        | (x1, vs1), (x2, vs2) ->
            match op with
            | Add -> (x1 + x2, vs1 @ vs2)
            | Subtract -> (x1 - x2, vs1 @ vs2)
            | Multiply -> (x1 * x2, vs1 @ vs2)
            | Divide when x2 <> 0.0 -> (x1 / x2, vs1 @ vs2)
            | Modulo when x2 <> 0.0 -> (x1 % x2, vs1 @ vs2)
            | _ -> failwith "Division by 0."
            
module Solution = 
    type Interpreter () =
    
        let mutable values = Map.empty<string, float>
        let mutable functions = Map.empty<string, FunctionDefinition>
    
        let execute input =
            let identifiers = (values |> Map.toList |> List.map fst)
            try match parse identifiers functions input with
                | Val e ->
                    let (result, newValues) = 
                        compute values functions [] e
                    let updatedValues = 
                        (values, newValues) 
                        ||> Seq.fold (fun acc (k, v) -> acc |> Map.add k v)
                    values <- updatedValues
                    Some result         
                | FVal (FunctionDefinition(name, _, _) as f) ->
                    functions <- functions.Add(name, f)
                    None
                | ParseError e -> printfn "%s" e; None
            with ex -> printfn "%s" ex.Message; None
       
        member this.input input =
            execute input 
            |> Option.toNullable
            
___________________________________________________________________________
open System
open System.Text.RegularExpressions

type Operator = Add | Subtract | Multiply | Divide | Modulo

type Expression =
    | Number of double
    | Identifier of string
    | Assignment of string * Expression
    | FunctionCall of string * Expression list
    | Operation of Operator * Expression * Expression

type FunctionDefinition = 
    | FunctionDefinition of string * string list * Expression

type ParseResult = 
    | FVal of FunctionDefinition
    | Val of Expression
    | ParseError of string

let matchToken pattern input =
    let m = Regex.Match(input, sprintf @"^\s*(%s)(.*)" pattern)
    if m.Success then Some(m.Groups.[1].Value, m.Groups.[2].Value)
    else None
    
let (|ID|_|) = matchToken "[A-Za-z_][A-Za-z0-9_]*"
let (|NUM|_|) = matchToken @"[0-9]*\.?[0-9]+" >> Option.map (fun (x, rest) -> float x, rest)
    
let matchSymbol pattern input = matchToken pattern input |> Option.map snd

let (|ADD|_|) = matchSymbol @"\+"
let (|SUB|_|) = matchSymbol "-" 
let (|MUL|_|) = matchSymbol @"\*"
let (|MOD|_|) = matchSymbol "%"
let (|DIV|_|) = matchSymbol "/"
let (|LPAREN|_|) = matchSymbol @"\("
let (|RPAREN|_|) = matchSymbol @"\)"
let (|FN|_|) = matchSymbol "fn"
let (|EQUALS|_|) = matchSymbol "="
let (|ARR|_|) = matchSymbol "=>"

let (|FACTOP|_|) = function 
    | MUL rest -> Some(Multiply, rest) 
    | DIV rest -> Some(Divide, rest)
    | MOD rest  -> Some(Modulo, rest)
    | _ -> None

let (|SUMOP|_|) = function 
    | ADD rest -> Some(Add, rest) 
    | SUB rest -> Some(Subtract, rest)
    | _ -> None

let rec (|MANY|_|) f acc input =
    match f input with
    | Some(x, rest) -> (|MANY|_|) f (x::acc) rest
    | None -> Some(acc, input)

let rec (|EXACTLY|_|) n f acc input =
    match f input with
    | _ when acc |> List.length = n -> Some(acc, input)
    | Some(x, rest) -> (|EXACTLY|_|) n f (x::acc) rest
    | None -> None

let (|EOL|_|) input = if String.IsNullOrWhiteSpace input then Some() else None

let (|EXPRFULL|_|) vs fs = 
    let rec (|ASSIGN|_|) = function
        | ID( n, EQUALS( EXPR(e, rest))) -> Some(Assignment(n, e), rest)
        | _ -> None
    
    and (|FACTOR|_|) = function
        | NUM (x, rest) -> Some (Number x, rest)
        | FNCALL(fc, rest) -> Some (fc, rest)
        | ASSIGN(a, rest) -> Some (a, rest)
        | ID (id, rest) ->
            if vs |> List.contains id 
            then Some (Identifier id, rest)
            else failwithf "Unknown identifier '%s'." id
        | LPAREN( EXPR(e, RPAREN( rest))) -> Some (e, rest)
        | _ -> None

    and (|FNCALL|_|) = function
        | ID(fn, rest) when fs |> Map.containsKey fn ->
            let (FunctionDefinition(_, argIds, _)) = fs.[fn]
            let n = argIds.Length 
            match rest with
            | EXACTLY n (|EXPR|_|) [] (args, rest) -> Some(FunctionCall(fn, args), rest)
            | _ -> failwithf "Function '%s' expects %d arguments." fn n
        | _ -> None

    and factorExprs = function FACTOP(op, FACTOR(e, rest)) -> Some((op, e), rest) | _ -> None
    and sumExprs = function SUMOP(op, TERM(e, rest)) -> Some((op, e), rest) | _ -> None

    and (|TERM|_|) = function
        | FACTOR(e1, MANY factorExprs [] (exprs, rest)) ->
            match exprs |> List.rev with
            | [] -> Some(e1, rest)
            | exprs ->
                Some ((e1, exprs) ||> List.fold(fun acc (op, e) -> Operation(op, acc, e)), rest)
        | _ -> None

    and (|EXPR|_|) = function
        | TERM(e1, MANY sumExprs [] (exprs, rest)) ->
            match exprs |> List.rev with
            | [] -> Some(e1, rest)
            | exprs ->
                Some ((e1, exprs) ||> List.fold(fun acc (op, e) -> Operation(op, acc, e)), rest)
        | _ -> None

    function EXPR(e, EOL) -> Some e | _ -> None
    
let (|FUNC|_|) fs = function
    | FN( ID( name, MANY (|ID|_|) [] (args, ARR(rest)))) ->
        match rest with
        | EXPRFULL args fs (e) -> Some( FunctionDefinition(name, args, e))
        | _ -> failwith "Syntax error in function body."
    | _ -> None

let parse vs fs = function
    | FUNC fs (f) -> FVal f
    | EXPRFULL vs fs (e) -> Val e
    | _ -> ParseError "Syntax error."

let rec compute vs fs updatedVs expr =
    match expr with
    | Number x -> (x, updatedVs)
    | Identifier id -> (vs |> Map.find id, updatedVs)
    | Assignment (id, expr) ->
        let (x, uvs) = compute vs fs updatedVs expr
        x, (id, x)::uvs 
    | FunctionCall (id, argExprs) ->
        let (FunctionDefinition(fn, argNames, fbody)) = fs |> Map.find id
        let computedArgs = 
          [ for name, expr in Seq.zip argNames argExprs do
                let (x, uvs) = compute vs fs updatedVs expr 
                yield (name, x), uvs ]
        let (args, uvsList) = computedArgs |> List.unzip
        let (result, _) = compute (Map args) fs updatedVs fbody
        result, List.concat uvsList
    | Operation (op, e1, e2) ->
        match compute vs fs updatedVs e1, compute vs fs updatedVs e2 with
        | (x1, vs1), (x2, vs2) ->
            match op with
            | Add -> (x1 + x2, vs1 @ vs2)
            | Subtract -> (x1 - x2, vs1 @ vs2)
            | Multiply -> (x1 * x2, vs1 @ vs2)
            | Divide when x2 <> 0.0 -> (x1 / x2, vs1 @ vs2)
            | Modulo when x2 <> 0.0 -> (x1 % x2, vs1 @ vs2)
            | _ -> failwith "Division by 0."

module Solution =
  type Interpreter () =
  
      let mutable values = Map.empty<string, float>
      let mutable functions = Map.empty<string, FunctionDefinition>
  
      let execute input =
          let identifiers = (values |> Map.toList |> List.map fst)
          try match parse identifiers functions input with
              | Val e ->
                  let (result, newValues) = 
                      compute values functions [] e
                  let updatedValues = 
                      (values, newValues) 
                      ||> Seq.fold (fun acc (k, v) -> acc |> Map.add k v)
                  values <- updatedValues
                  Some result         
              | FVal (FunctionDefinition(name, _, _) as f) ->
                  functions <- functions.Add(name, f)
                  None
              | ParseError e -> printfn "%s" e; None
          with ex -> printfn "%s" ex.Message; None
     
      member this.input input =
          execute input 
          |> Option.toNullable
