function unbleach(n: string): string {
  return (n || '').replace(/ /g, 's').replace(/\t/g, 't').replace(/\n/g, 'n');
}

// imp, command, [parameter]
type Program = ([string, string] | [string, string, string] | [string, string, number])[];

class Parser {
  private index = 0;
  constructor(private code: string) { }
  
  public parse(): Program {
    const program: Program = [];
    let imp: string;
    while (imp = this.pullImp()) {
      switch (imp) {
        case ' ': // Stack Manipulation
          const c = this.pullChar();
          if (c === ' ') {
            program.push([imp, c, this.pullNumber()]);
          } else if (c === '\t') {
            program.push([imp, c + this.pullSome(' ', '\n'), this.pullNumber()]);
          } else {
            program.push([imp, c + this.pullChar()]);
          }
          break;
        case '\t ': // Arithmetic
          program.push([imp, this.pullSome('  ', ' \t', ' \n', '\t ', '\t\t')]);
          break;
        case '\t\t': // Heap Access
          program.push([imp, this.pullSome(' ', '\t')]);
          break;
        case '\t\n': // Input/Output
          program.push([imp, this.pullSome('  ', ' \t', '\t ', '\t\t')]);
          break;
        case '\n': // Flow Control
          const cmd = this.pullSome('  ', ' \t', ' \n', '\t ', '\t\t', '\t\n', '\n\n');
          if (cmd === '\t\n' || cmd === '\n\n') {
            program.push([imp, cmd]);
          } else {
            program.push([imp, cmd, this.pullLabel()]);
          }
          break;
        default:
          throw new Error('Invalid IMP');
      }
    }
    return program;
  }
  
  private pullNumber(): number {
    const sign = this.pullChar();
    if (sign !== '\t' && sign !== ' ') {
      throw new Error('Invalid number sign');
    }
    
    const digits = this.pullUntil('\n');
    if (digits === '') {
      return 0;
    }
    return parseInt(digits.replace(/ /g, '0').replace(/\t/g, '1'), 2) * (sign === '\t' ? -1 : 1);
  }
  
  private pullLabel(): string {
    return this.pullUntil('\n');
  }
  
  private pullImp(): string {
    const c1 = this.pullChar();
    if (!c1) {
      return '';
    }
    if (c1 === '\t') {
      const c2 = this.pullChar();
      if (!c2) {
        throw new Error('Invalid IMP');
      }
      return c1 + c2;
    }
    return c1;
  }
  
  private pullUntil(terminal: string): string {
    let out = '';
    let c: string;
    while (c = this.pullChar()) {
      if (c === terminal) {
        return out;
      }
      out += c;
    }
    throw new Error('Unterminated parameter');
  }
  
  private pullSome(...options: string[]): string {
    const max = Math.max(...options.map(opt => opt.length));
    let out = '';
    let c: string;
    while (c = this.pullChar()) {
      out += c;
      if (out.length > max) {
        throw new Error('Invalid instruction');
      }
      if (options.includes(out)) {
        return out;
      }
    }
    throw new Error('No instruction found');
  }
  
  private pullChar(): string {
    while (this.index < this.code.length) {
      const c = this.code[this.index];
      this.index += 1;
      if (c === ' ' || c === '\t' || c === '\n') {
        return c;
      }
    }
    return '';
  }
}

class Interpreter {
  public output = '';
  private stack: number[] = [];
  private heap = new Map<number, number>();
  
  private pc = 0;
  private callstack: number[] = [];
  
  private inputIndex = 0;
  private labels = new Map<string, number>();
  
  constructor(private program: Program, private input: string) {
    for (const [i, [imp, cmd, arg]] of this.program.entries()) {
      if (imp === '\n' && cmd === '  ' && typeof arg === 'string') {
        if (this.labels.has(arg)) {
          throw new Error(`Duplicate label: ${unbleach(arg)}`);
        }
        this.labels.set(arg, i);
      }
    }
  }
  
  private pop(): number {
    const n = this.stack.pop();
    if (n === undefined) {
      throw new Error('pop on an empty stack');
    }
    return n;
  }
  
  private read(): string {
    const c = this.input[this.inputIndex];
    if (c === undefined) {
      throw new Error('read on empty input');
    }
    this.inputIndex += 1;
    return c;
  }
  
  private readUntil(terminator: string): string {
    let out = '';
    let c;
    while ((c = this.read()) !== terminator) {
      out += c;
    }
    return out;
  }
  
  private jump(label: string): void {
    const target = this.labels.get(label);
    if (target === undefined) {
      throw new Error(`Jump to unknown label: ${unbleach(label)}`);
    }
    this.pc = target + 1;
  }
  
  public run(): void {
    main:
    while (this.pc < this.program.length) {
      const [imp, cmd, arg] = this.program[this.pc];
      let a: number;
      let b: number;
      let s: string;
      let maybe: number | undefined;
      switch (imp + cmd) {
        // Stack Manipulation
        case '  ': // Push n onto the stack.
          this.stack.push(arg as number);
          break;
        case ' \t ': // Duplicate the nth value from the top of the stack and push onto the stack.
          maybe = this.stack[this.stack.length - (arg as number) - 1];
          if (maybe === undefined) {
            throw new Error('duplicate beyond stack')
          }
          this.stack.push(maybe);
          break;
        case ' \t\n': // Discard the top n values below the top of the stack from the stack. (For n<**0** or **n**>=stack.length, remove everything but the top value.)
          if ((arg as number) < 0 || (arg as number) >= this.stack.length) {
            this.stack = [this.pop()]
          } else {
            const top = this.pop();
            this.stack = this.stack.slice(0, this.stack.length - (arg as number));
            this.stack.push(top);
          }
          break;
        case ' \n ': // Duplicate the top value on the stack.
          a = this.pop();
          this.stack.push(a, a);
          break;
        case ' \n\t': // Swap the top two value on the stack.
          a = this.pop();
          b = this.pop();
          this.stack.push(a, b);
          break;
        case ' \n\n': 
          this.pop();
          break;
        // Arithmetic
        case '\t   ': 
          a = this.pop();
          b = this.pop();
          this.stack.push(b + a);
          break;
        case '\t  \t': 
          a = this.pop();
          b = this.pop();
          this.stack.push(b - a);
          break;
        case '\t  \n': 
          a = this.pop();
          b = this.pop();
          this.stack.push(b * a);
          break;
        case '\t \t ':  
          a = this.pop();
          b = this.pop();
          if (a === 0) {
            throw new Error('Division by zero');
          }
          this.stack.push(Math.floor(b / a));
          break;
        case '\t \t\t': 
          a = this.pop();
          b = this.pop();
          if (a === 0) {
            throw new Error('Remainder of division by zero');
          }
          this.stack.push(b - a * Math.floor(b / a));
          break;
        
        case '\t\t ': 
          a = this.pop();
          b = this.pop();
          this.heap.set(b, a);
          break;
        case '\t\t\t': 
          a = this.pop();
          maybe = this.heap.get(a);
          if (maybe === undefined) {
            throw new Error('Undefined heap address');
          }
          this.stack.push(maybe);
          break;
        // Input/Output
        case '\t\n  ': 
          this.output += String.fromCharCode(this.pop());
          break;
        case '\t\n \t': 
          this.output += this.pop();
          break;
        case '\t\n\t ': 
          s = this.read();
          b = this.pop();
          this.heap.set(b, s.charCodeAt(0));
          break;
        case '\t\n\t\t': 
          a = parseInt(this.readUntil('\n'));
          b = this.pop();
          this.heap.set(b, a);
          break;
        // Flow Control
        case '\n  ': 
          // no-op
          break;
        case '\n \t': 
          this.callstack.push(this.pc);
          this.jump(arg as string);
          continue main;
        case '\n \n': 
          this.jump(arg as string);
          continue main;
        case '\n\t ': 
          if (this.pop() === 0) {
            this.jump(arg as string);
            continue main;
          }
          break;
        case '\n\t\t': 
          if (this.pop() < 0) {
            this.jump(arg as string);
            continue main;
          }
          break;
        case '\n\t\n': 
          maybe = this.callstack.pop();
          if (maybe === undefined) {
            throw new Error('return without being in a subroutine');
          }
          this.pc = maybe + 1;
          continue main;
        case '\n\n\n': 
          return;
        default:
          throw new Error(`Unknown command: ${unbleach(imp + cmd)}`);
      }
      this.pc += 1;
    }
    throw new Error('Unclean termination');
  }
}

export function whitespace(code: string, input: string = ''): string {
  let parser = new Parser(code);
  let program = parser.parse();
  let interpreter = new Interpreter(program, input);
  interpreter.run();
  return interpreter.output;
};
                             
___________________________________________________
type Func0<A> = () => A
type Func1<A,B> = (a:A) => B
type Func2<A,B,C> = (a:A,b:B) => C
type Sequence<T> = Func0<IterableIterator<T>>

function hasOwnProperty<X extends {}, Y extends PropertyKey>
  (obj: X, prop: Y): obj is X & Record<Y, unknown> {
  return obj.hasOwnProperty(prop)
}

declare global {
  interface Object {
    pipe<TObj extends Object,TNew>( this:TObj, func:Func1<TObj,TNew> ):TNew
  }

}
Object.prototype.pipe = function<TObj extends Object,TNew>( this:TObj, func:Func1<TObj,TNew> ){
  return func(this);
}


//SEQUENCE LIB
//allows for composing generator functions.

//functions to build base generator functions
namespace NewSeq{
  export const fromRange = ( min:number, count:number ) => function*(){
    for( let i = 0; i < count; i++ ){
      yield min+i
    }
  }

  export const fromIterator = <T>( iterator:Iterator<T> ) => function*(){
    let result = iterator.next();
    while (!result.done) {
     yield result.value;
     result = iterator.next();
    }
  }
  export const singleItem = <T>( item:T ) => function*(){
    yield item;
  }

  export const fromArray = <T>(array:Array<T>) => () => array[Symbol.iterator]

  export const empty = <T>() => function*(){}
}


//generator function combinators and evaluators
namespace Seq {
  export const take = <T>( maxCount:number ) => (sequence:Sequence<T>) => function*(){
    if( maxCount < 1 ) return;

    let totalReturned = 0
    for( let x of sequence() ){
      yield x;
      totalReturned++;
      if( totalReturned >= maxCount ) return;
    }
  }

    export const lastOr = <A,B>( alternative:B ) => ( sequence:Sequence<A> ) => {
      let returnValue:(A|B) = alternative;
      for( const x of sequence() ){
        returnValue = x;
      }
      return returnValue;
    }

    export const firstOr = <A,B>( alternative:B ) => ( sequence:Sequence<A> ):A|B => {
      for( const x of sequence() ){
        return x;
      }
      return alternative
    }

    export const skip = <T>( skipCount:number ) => ( sequence:Sequence<T> ) => function*(){
      const generatorSequence = NewSeq.fromIterator( sequence() );
      generatorSequence.pipe( take(skipCount) ).pipe( lastOr( undefined ) );
      yield* generatorSequence()
    }

    export const flatMap = <A,B>( func:Func1<A,Sequence<B>> ) => ( sequence:Sequence<A> ) => function*(){
      for( const a of sequence() ) {
        for( const b of func(a)() ) {
          yield b;
        }
      }
    }

    export const map = <A,B>( func:Func1<A,B> ) => flatMap<A,B>( a => NewSeq.singleItem( func(a) ) );

    export const filter = <A>( predicate:Func1<A,boolean> ) => flatMap<A,A>( a => predicate(a)? NewSeq.singleItem(a): NewSeq.empty<A>() );
}

declare global {
  interface Array<T> {
    fold<TAcc>( this:Array<T>, initialValue:TAcc, folder:Func2<TAcc,T,TAcc> ):TAcc
    foldRight<TAcc>( this:Array<T>, initialValue:TAcc, folder:Func2<TAcc,T,TAcc> ):TAcc
  }
}

Array.prototype.fold = 
function<T,TAcc>( this:Array<T>, initialValue:TAcc, folder:Func2<TAcc,T,TAcc> ):TAcc {
  let accumulator = initialValue;
  this.forEach( x => accumulator = folder(accumulator,x) );
  return accumulator;
}

Array.prototype.foldRight =
function<T,TAcc>( this:Readonly<Array<T>>, initialValue:TAcc, folder:Func2<TAcc,T,TAcc> ):TAcc{
  let accumulator = initialValue
  for( let i = this.length -1; i> -1; i-- ){
    accumulator = folder( accumulator,this[i] );
  }

  return accumulator;
}


//PARSING LIBRARY
type ParsingContext = Readonly<{ text:string, nextIndex:number }>


class ParseFailure{
  public constructor(){}
  static instance = new ParseFailure();
}

class ParseResult<T> { constructor( public readonly context:ParsingContext, public readonly value:T|ParseFailure ){} }
type ParserFunction<T> = Func1<ParsingContext,ParseResult<T>>

class Parser<T> {
  constructor( public func:ParserFunction<T> ){}

  readonly flatMap = <U>( mapFunc:Func1<T,Parser<U>>) => new Parser<U>( context => {
    const result = this.func( context );
    if( result.value instanceof ParseFailure ) return result;
    return mapFunc( result.value ).func( result.context );

  } );

  readonly parse = ( str:string, index?:number ):ParseResult<T> => {
    
    const result = this.func( { text:str, nextIndex:index ?? 0 } );
    return result;
  } 
    

  readonly map = <U>( mapFunc:Func1<T,U> ):Parser<U> => this.flatMap( (x:T) => P.fromValue( mapFunc( x ) ) )

  readonly or = <T2>( fallback:Parser<T2> ) => new Parser<T|T2>(context => {
    const firstTry = this.func( context );
    if( firstTry.value instanceof ParseFailure ) return fallback.func( context );
    return firstTry;
  })

  readonly then = <U> ( next:Parser<U> ):Parser<[T,U]> => this.flatMap( x => next.map( y => [x,y] ) );

  readonly discardThen = <U>( next:Parser<U> ):Parser<U> => this.flatMap( _ => next );

  readonly thenDiscard = <U>( next:Parser<U> ):Parser<T> => this.flatMap( x => next.discardThen( P.fromValue(x) ) );

  readonly validate = ( predicate:Func1<T,boolean> ):Parser<T> => this.flatMap( x => predicate(x) ? P.fromValue(x): P.fail() );

  readonly validateParseCompleted = () => this.thenDiscard( P.getContext().validate( x => x.nextIndex === x.text.length ) )

  readonly zeroOrMore = ():Parser<T[]> => 
    P.getContext()
    .flatMap( (context) =>{
      const thisParser = this;
      let currentContext = context;
      return P.fromValue( 
        Array.from(
          function*(){
            while( true ){
              const parseResult = thisParser.func( currentContext )
              if( parseResult.value instanceof ParseFailure ) return;
              currentContext = parseResult.context

              yield parseResult.value
            }
          }()
        )
      )
      .thenDiscard( P.putContext( currentContext ) )
    } );

    readonly oneOrMore = ():Parser<T[]> => this.zeroOrMore().validate( x => x.length > 0 );
}

//base parser combinators
namespace P{
  export const fromValue = <T>( value:T ) => new Parser<T>( (context) => new ParseResult<T>( context, value ) )

  export const fail = <T>() => new Parser<T>( ( context ) => new ParseResult<T>( context, ParseFailure.instance ) )

  const getContextValue = new Parser<ParsingContext>( (context:ParsingContext) => new ParseResult( context, context ) );
  export const getContext = () => getContextValue;

  export const putContext = ( context:ParsingContext ):Parser<void> => new Parser<void>( () => new ParseResult<void>( context, undefined ) );

  const anyCharValue = 
    getContext()
    .validate( context => context.nextIndex < context.text.length )
    .flatMap( (context:ParsingContext) => 
      P.fromValue( context.text[context.nextIndex] )
      .thenDiscard( P.putContext( { text:context.text, nextIndex:context.nextIndex + 1 } ) )
      )
  export const anyChar = () => anyCharValue;

  export const char = ( c:String ) => anyChar().validate( x => x === c )

  export const fork = <TTest,TResult>( test:Parser<TTest>, ifTestSucceeded:Parser<TResult>, ifTestFailed:Parser<TResult> ) =>
    test.map( _ => true )
      .or( P.fromValue(false) )
      .flatMap( (testSucceeded) => testSucceeded ? ifTestSucceeded : ifTestFailed );

  export const match = <TTest,TResult>( ...tests:[Parser<TTest>,Parser<TResult>][] ) =>
    tests.foldRight( fail<TResult>(), (acc,[nextTest,nextParser]) => fork( nextTest, nextParser, acc ) )

  export const concat = <T>( parsers:Parser<T>[] ):Parser<T[]> => 
    P.getContext()
    .flatMap(context => {
      let currentContext = context;
      let succeeded = false;

      const resultArray = Array.from<T>( function*(){
        for( let parser of parsers ) {
          const parseResult = parser.func( currentContext )
          if( parseResult.value instanceof ParseFailure ) return;

          currentContext = parseResult.context;
          yield parseResult.value;
        }
        succeeded = true;
      }() );

      if( !succeeded ) return P.fail();

      return P.fromValue( resultArray )
      .thenDiscard( P.putContext( currentContext ) )
    })

  export const choose = <T>( parsers:Parser<T>[] ) =>
    parsers.reduce( (acc,next) => acc.or(next) );

}


//Whitespace program abstractions
interface ICommandWithValue<T>{
  readonly value:T
}
type ICommandWithNumber = ICommandWithValue<number>

class DuplicateValueAtPosition implements ICommandWithNumber { constructor( public value:number ){} }
class RemoveNValuesUnderTop implements ICommandWithNumber { constructor( public value:number ){} }
class PushNumberCommand implements ICommandWithNumber { constructor( public value:number ){} }
type StackCommand = 
  |RemoveNValuesUnderTop
  |PushNumberCommand
  |DuplicateValueAtPosition
  |"DuplicateTopValue"
  |"SwapTopTwoValues"
  |"DiscardTopValue"


const arithmeticCommand = [ "Add","Subtract","Multiply", "Divide","Modulus" ] as const
type ArithmeticCommand = typeof arithmeticCommand[number]

const isArithmeticCommand = ( x:unknown ):x is ArithmeticCommand =>{
  return typeof(x) === 'string' && arithmeticCommand.includes( x as ArithmeticCommand )
}

type IOCommand = 
  | "OutputChar"
  | "OutputNumber"
  | "InputCharToHeap"
  | "InputNumberToHeap"

type HeapCommand = 
  | "StoreAAtAddressB"
  | "PopAThenPushHeapAddressA"


class NewLabelCommand{ constructor( public label:string ){} }
class CallSubroutineCommand{ constructor( public label:string ){} }
class JumpToCommand{ constructor( public label:string ){} }
class PopAndJumpIf{ constructor( public label:string, public condition:Func1<number,boolean> ){} }

type FlowCommand = 
  | NewLabelCommand
  | CallSubroutineCommand
  | JumpToCommand
  | PopAndJumpIf
  | "ExitSubroutine"
  | "ExitProgram"

type WSCommand = 
  | StackCommand
  | IOCommand
  | FlowCommand
  | HeapCommand
  | ArithmeticCommand


//parsers that are specific to whitespace
namespace WSP {
  type Space = "space"
  type Tab = "tab"
  type NewLine = "newline"
  type Whitespace = Space | Tab | NewLine

  const whitespaceChars:Readonly<string[]> = [ " ", "\t", "\n" ]
  const pComment = P.anyChar().validate( c => !whitespaceChars.includes( c ) ).zeroOrMore()

  const pSingleSpace:Parser<Space> = P.char( " " ).map<Space>( _ => "space" );
  const pSingleTab:Parser<Tab> = P.char( "\t" ).map( _ => "tab" );
  const pSingleNewLine:Parser<NewLine> = P.char( "\n" ).map( _ => "newline" );
  

  const pTab:Parser<Tab> = pSingleTab.thenDiscard( pComment )
  const pSpace:Parser<Space> = pSingleSpace.thenDiscard( pComment )
  const pNewLine:Parser<NewLine> = pSingleNewLine.thenDiscard( pComment )

  const baseParsers:Record<Whitespace,Parser<Whitespace>> = {
    "tab":pTab,
    "space":pSpace,
    "newline":pNewLine
  }

  const route = <TCommand>( ...mappings:[Whitespace[]|Whitespace,Parser<TCommand>| TCommand ][] ):Parser<TCommand> => {
    const parsers:[Parser<Whitespace[]>,Parser<TCommand>][] = mappings.map( 
      ([headerOrHeaders,commandOrParser]) => {

        const headers = (headerOrHeaders instanceof Array ? headerOrHeaders : [headerOrHeaders]).map( x => baseParsers[x] );
        const parser = commandOrParser instanceof Parser ? commandOrParser : P.fromValue( commandOrParser );
        return [P.concat(headers),parser];
      })
    return P.match( ...parsers );
  }

  const unsignedNumberFromBinary = ( bits:boolean[] ) =>
  [false, ...bits]
  .map( Number )
  .reduce( (x,y) => 2*x+y );

  const pUnsignedNumber:Parser<number> = 
    route( ["space",false], ["tab",true] )
      .zeroOrMore()
      .map( unsignedNumberFromBinary )

  const pNumberSign:Parser<number> =
    route( ["space",1], ["tab",-1] )

  const pNumber:Parser<number> = 
    pNumberSign
    .then(pUnsignedNumber)
    .map( ([x,y]) => x * y )
    .thenDiscard( pNewLine )

  const pLabel:Parser<string> = route<string>(
    ["tab","t"],
    ["space","s"]
  )
  .zeroOrMore()
  .thenDiscard( pNewLine )
  .map( x => x.join('') )

const pIOCommand:Parser<IOCommand> = route<IOCommand>(
  [["space","space"],"OutputChar"], // Pop a value off the stack and output it as a character
  [["space","tab"],"OutputNumber"], //Pop a value off the stack and output it as a number.
  [["tab","space"],"InputCharToHeap"], //Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
  [["tab","tab"],"InputNumberToHeap"], //Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.
);

const pStackCommand = route<StackCommand>(
  ["space", pNumber.map( x => new PushNumberCommand(x) )], // push a number onto the stack
  [["tab", "space"], pNumber.map( x => new DuplicateValueAtPosition(x) ) ], // duplicate nth value and place on the stack (0 indexed)
  [["tab", "newline"], pNumber.map( x => new RemoveNValuesUnderTop(x) )], // Discard the top n values below the top of the stack from the stack. (For n<**0** or **n**>=stack.length, remove everything but the top value.)
  [["newline", "space"], "DuplicateTopValue" ], //Duplicate the top value on the stack.
  [["newline","tab"], "SwapTopTwoValues" ], //Swap the top two values on the stack
  [["newline", "newline"], "DiscardTopValue"], // Discard the top value on the stack
)

const pArithmeticCommand:Parser<ArithmeticCommand> = route(
  [["space", "space" ], "Add" ],
  [["space", "tab" ], "Subtract" ],
  [["space", "newline" ], "Multiply" ],
  [["tab", "space" ], "Divide" ],
  [["tab", "tab" ], "Modulus" ],
)
const pHeapAccessCommand:Parser<HeapCommand> = route<HeapCommand>(
  ["space", "StoreAAtAddressB"], //[space]: Pop a and b, then store a at heap address b.
  ["tab", "PopAThenPushHeapAddressA" ] //[tab]: Pop a and then push the value at heap address a onto the stack.
)

const pFlowCommand:Parser<FlowCommand> = route<FlowCommand>(
  [["space","space"], pLabel.map( x => new NewLabelCommand( x ) )], // mark a location in the program with a label
  [["space","tab"], pLabel.map( x => new CallSubroutineCommand( x ) )], //Call a subroutine with the location specified by label n.
  [["space","newline"], pLabel.map( x => new JumpToCommand( x ) )], //Jump unconditionally to the position specified by label n.
  [["tab","space"], pLabel.map( x => new PopAndJumpIf( x, num => num === 0 ) )], //Pop a value off the stack and jump to the label specified by n if the value is zero.
  [["tab","tab"], pLabel.map( x => new PopAndJumpIf( x, num => num < 0 ) )], //Pop a value off the stack and jump to the label specified by n if the value is less than zero.
  [["tab","newline"], "ExitSubroutine"], //Exit a subroutine and return control to the location from which the subroutine was called.
  [["newline","newline"], "ExitProgram"], //Exit the program
);

const pCommand = route<WSCommand>(
    ["space", pStackCommand],
    [["tab","space"], pArithmeticCommand],
    [["tab","tab"], pHeapAccessCommand],
    [["tab","newline"], pIOCommand],
    ["newline", pFlowCommand],
  )

  export const pProgram:Parser<WSCommand[]> = pComment.discardThen( pCommand.zeroOrMore() ).validateParseCompleted()

}

//an immutable stack datastructure
class Stack<T>{

  readonly count:number
  private constructor( private data?:[Stack<T>,T] ){
    this.count = (data?.[0].count ?? -1) + 1
  }

  static readonly empty = <T>() => new Stack<T>();

  readonly push = ( newHead:T ) => new Stack<T>( [this,newHead] );

  readonly pop = ():[T,Stack<T>] => {
    if( !this.data ) throw new Error( "popping or peeking an empty stack is forbidden" );
    return [this.data[1],this.data[0]]
  }

  readonly pop2 = ():[T,T,Stack<T>] => {
    const [a,stackMinus1] = this.pop()
    const [b,stackMinus2] = stackMinus1.pop()
    return [a,b,stackMinus2];
  }

  readonly peek = ():T => this.pop()[0];
  static readonly fromArray = <T>( array:Array<T> ) => array.fold( Stack.empty<T>(), (stack,next) => stack.push(next) );

  //returns all of the stacks from top to bottom
  private static readonly doGetAllStacks = <T>( stack:Stack<T> ):Sequence<Stack<T>> => function*(){
    let currentStack = stack
    while( true ){
      yield currentStack;
      if( currentStack.count === 0 ) return;
      const [_,nextStack] = currentStack.pop();
      currentStack = nextStack;
    }
  }
    
  readonly allStacks:Sequence<Stack<T>> = Stack.doGetAllStacks(this)
  readonly allValues:Sequence<T> = this.allStacks.pipe( Seq.filter(x => x.count > 0) ).pipe( Seq.map( x => x.peek() ) )
}


class ExecutingProgramState {
  constructor(
    public readonly callStack:Stack<Stack<WSCommand>>,
    public readonly mathStack:Stack<number>,
    public readonly cInPosition:number )
    {}

    withStacks( callStack:Stack<Stack<WSCommand>>, mathStack:Stack<number> ){
      return new ExecutingProgramState(callStack,mathStack,this.cInPosition);
    }

    changeConsoleInputPosition( number:number  ){
      return new ExecutingProgramState( this.callStack, this.mathStack,number )
    }
}

type ProgramState = | ExecutingProgramState | "BadExit" | "GoodExit"

const pConsoleInputNumber:Parser<number> = function(){
  const digitChars = "0123456789" as const;
  const isDigit = (x:string) => digitChars.includes(x);

  return P
    .char('\n')
    .zeroOrMore()
    .discardThen( 
      P.anyChar()
      .validate(isDigit)
      .oneOrMore()
      .map( x => x.join('') )
      .map( x => Number.parseInt(x) )
  )
}()

const pConsoleInputChar:Parser<string> = P
  .char('\n')
  .zeroOrMore()
  .discardThen(P.anyChar())

//runs the next command of a program
function progressState(
  state:ExecutingProgramState,
  heap:Map<number,number>,
  cIn:Readonly<string>,
  subRoutines:Readonly<Map<string,Stack<WSCommand>>>
  ):[ProgramState,string]|ProgramState {
  if( state.callStack.count === 0 ) return 'BadExit';

  const currentRoutine = state.callStack.peek();
  
  if( currentRoutine.count === 0 ) return 'BadExit';
  
  const [command, remainingCallstack] = currentRoutine.pop();
  const newCallStack = state.callStack.pop()[1].push( remainingCallstack );

  if( command === 'ExitProgram' ) return 'GoodExit';
  if( command instanceof PushNumberCommand ) {
    const newMathStack = state.mathStack.push( command.value )
    const newState = state.withStacks( newCallStack, newMathStack );
    return newState;
  }
  if( command === "OutputNumber" || command === "OutputChar" ) {
    const [num,newMathStack] = state.mathStack.pop();
    const newState = state.withStacks( newCallStack, newMathStack );
    return [newState, command === "OutputNumber" ? String( num ) : String.fromCharCode( num )]
  }
  if( command === 'DuplicateTopValue' ){
    return state.withStacks( newCallStack, state.mathStack.push( state.mathStack.peek() ) )
  }
  if( command instanceof DuplicateValueAtPosition ){
    const position = command.value

    if( position < 0 || position >= state.mathStack.count ) throw new Error("Invalid Position " + position )
    const itemToDuplicate = state.mathStack.allValues.pipe( Seq.skip(position) ).pipe( Seq.firstOr( undefined ) );
    if( itemToDuplicate === undefined ) throw new Error( "no item at arithmetic stack position "+ position )

    const newMathStack = state.mathStack.push( itemToDuplicate )
    return state.withStacks( newCallStack, newMathStack );
  }
  if( command === 'SwapTopTwoValues' ){
    const newMathStack:Stack<number> = (() => {
      const [a,b,stackMinusTwo] = state.mathStack.pop2();
      return stackMinusTwo.push(a).push(b);

    })()

    return state.withStacks( newCallStack, newMathStack );
  }
  if( command === 'DiscardTopValue' ){
     if( state.mathStack.count === 0 ) throw new Error( "Unable to discard values on empty stack" )
    return state.withStacks( newCallStack, state.mathStack.pop()[1] )
  }
  if( command instanceof RemoveNValuesUnderTop ){
    const newMathStack:Stack<number> = (() => {
      const currentStack = state.mathStack;
      if( currentStack.count === 0 ) return currentStack;

      if( currentStack.count === 1 || command.value < 0 ) return Stack.empty<number>().push( currentStack.peek() )

      const newStack = 
        currentStack.allStacks
        .pipe( Seq.skip(command.value+1) )
        .pipe( Seq.firstOr( Stack.empty<number>() ) )
        .push( currentStack.peek() );
      return newStack;

    })()

    return state.withStacks( newCallStack, newMathStack )
  }
  if( command === 'StoreAAtAddressB' ){
    const [a,b,stackMinus2] = state.mathStack.pop2();
    heap.set(b,a);
    return state.withStacks( newCallStack, stackMinus2 );
  }
  if( command === 'PopAThenPushHeapAddressA' ){

    const [a,stackMinus1] = state.mathStack.pop();
    const valueFromHeap = heap.get(a)
    if( valueFromHeap === undefined ) throw new Error("Access Violation");
    return state.withStacks( newCallStack, stackMinus1.push(valueFromHeap) );
  }
  if( isArithmeticCommand(command) ){
    const [a,b,stackMinus2] = state.mathStack.pop2();

    const newValue = binaryOperators[command](a,b);
    if( newValue === Infinity || Number.isNaN(newValue) ) throw new Error( "Division and modulus by zero is forbidden" );

    const newStack = stackMinus2.push(newValue);
    return state.withStacks( newCallStack, newStack );
  }
  if( command === "InputNumberToHeap" ){
    
    const digitChars = "0123456789" as const;
    const isDigit = (x:string) => digitChars.includes(x);
    const parseResult = 
      pConsoleInputNumber
      .parse( cIn, state.cInPosition )

       if( parseResult.value instanceof ParseFailure ) throw new Error("Unable to retrieve an int from console input.")

      const numericValue = parseResult.value;
      const [b,stackMinus1] = state.mathStack.pop();
      heap.set( b, numericValue );
      return state.withStacks(newCallStack, stackMinus1).changeConsoleInputPosition( parseResult.context.nextIndex );
  }
  if( command === 'InputCharToHeap' ){

    const parseResult = 
      pConsoleInputChar
      .parse( cIn, state.cInPosition )

    if(parseResult.value instanceof ParseFailure) throw new Error( "Unable to parse a character from console input" )

      const char = parseResult.value
      const [b,stackMinus1] = state.mathStack.pop();
      heap.set(b, char.charCodeAt(0) )
      return state.withStacks(newCallStack,stackMinus1).changeConsoleInputPosition(parseResult.context.nextIndex);
  }
  if( command instanceof NewLabelCommand ) return state.withStacks(newCallStack, state.mathStack);


  const findSubroutine = (label:string) => {
    const subroutine = subRoutines.get( label )
    if( subroutine === undefined ) throw new Error( `no subroutine named '${label}' was found` )

    return subroutine;
  }

  if( command instanceof PopAndJumpIf ){
    const [a,stackMinus1] = state.mathStack.pop();
    const jumpTo = function(){
      if(command.condition(a)) return findSubroutine( command.label )

      return newCallStack.peek()
    }()
    return state.withStacks( newCallStack.pop()[1].push(jumpTo), stackMinus1 );
  }
  if( command instanceof JumpToCommand ){
    const subroutine = findSubroutine( command.label )
    return state.withStacks( newCallStack.pop()[1].push(subroutine), state.mathStack );
  }
  if( command instanceof CallSubroutineCommand ){
    const subroutine = findSubroutine( command.label )
    return state.withStacks( newCallStack.push(subroutine), state.mathStack );
  }
  if( command === 'ExitSubroutine' ){
    return state.withStacks( newCallStack.pop()[1], state.mathStack );
  }

  const endResult:never = command;
  throw new Error( "A command was unaccounted for!" )
}


const negativeMod = (a:number, n:number) => a - n * Math.floor(a / n)

const binaryOperators:Record<ArithmeticCommand,Func2<number,number,number>> = {
  "Add" : ((a:number , b:number) => b+a),
  "Subtract" : (a,b)=> b-a,
  "Multiply":(a,b)=>b*a,
  "Divide":(a,b)=> Math.floor(b/a),
  "Modulus":(a:number, b:number) => negativeMod(b,a)
}

//executes the program, yielding console output as it goes.
const runProgram = function*( initialState:ExecutingProgramState, consoleInput:string ):Generator<string,void,unknown>{

  let currentState:ExecutingProgramState = initialState
  const heap = new Map<number,number>()

  const subRoutinesSequence:Sequence<[string,Stack<WSCommand>]> = 
    initialState.callStack.peek().allStacks
    .pipe( Seq.filter( x => x.count > 0 && x.peek() instanceof NewLabelCommand ) )
    .pipe(Seq.map( stack => [( (stack.peek() as NewLabelCommand).label ),stack.pop()[1]] ) )

  const subroutines:Readonly<Map<string,Stack<WSCommand>>> = new Map<string,Stack<WSCommand>>();

  for(const [label,subroutine] of subRoutinesSequence()){

    if(subroutines.has(label)) throw new Error( "All labels must be unique" )
    subroutines.set(label,subroutine);
  }

  while( true ){
    const progressionResult = progressState(currentState,heap,consoleInput,subroutines)
    const [nextState,consoleOutput] = progressionResult instanceof Array ? progressionResult : [progressionResult,undefined]

    if( consoleOutput ) yield consoleOutput;
    if( nextState === 'BadExit' ) throw new Error( "abnormal program termination" );
    if( nextState === 'GoodExit' ) return;
    currentState = nextState
  }
}

const startProgram = ( programList:WSCommand[], consoleInput:string ):string => {

  //outer stack represents call stack.  Inner stack represents a sequence of commands to run.
  const program:Stack<Stack<WSCommand>> = 
    Array.from(programList).reverse()
    .pipe( Stack.fromArray )
    .pipe( x => [x] )
    .pipe(Stack.fromArray)

  const initialState = new ExecutingProgramState( program, Stack.empty<number>(), 0 );
  const programResult = Array.from(runProgram( initialState, consoleInput )).join('');
  return programResult;
}

  export function whitespace(code:string, input?:string):string {
    const parseResult = WSP.pProgram.parse( code );
    if( parseResult.value instanceof ParseFailure ) throw new Error( 'parse failed' );

    const commands = parseResult.value;
    const result = startProgram( commands, input ?? '' )
    return result;
  }
    
___________________________________________________
function unbleach(n: string): string {
  return (n || '').replace(/ /g, 's').replace(/\t/g, 't').replace(/\n/g, 'n');
}

// imp, command, [parameter]
type Program = ([string, string] | [string, string, string] | [string, string, number])[];

class Parser {
  private index = 0;
  constructor(private code: string) { }
  
  public parse(): Program {
    const program: Program = [];
    let imp: string;
    while (imp = this.pullImp()) {
      switch (imp) {
        case ' ': // Stack Manipulation
          const c = this.pullChar();
          if (c === ' ') {
            program.push([imp, c, this.pullNumber()]);
          } else if (c === '\t') {
            program.push([imp, c + this.pullSome(' ', '\n'), this.pullNumber()]);
          } else {
            program.push([imp, c + this.pullChar()]);
          }
          break;
        case '\t ': // Arithmetic
          program.push([imp, this.pullSome('  ', ' \t', ' \n', '\t ', '\t\t')]);
          break;
        case '\t\t': // Heap Access
          program.push([imp, this.pullSome(' ', '\t')]);
          break;
        case '\t\n': // Input/Output
          program.push([imp, this.pullSome('  ', ' \t', '\t ', '\t\t')]);
          break;
        case '\n': // Flow Control
          const cmd = this.pullSome('  ', ' \t', ' \n', '\t ', '\t\t', '\t\n', '\n\n');
          if (cmd === '\t\n' || cmd === '\n\n') {
            program.push([imp, cmd]);
          } else {
            program.push([imp, cmd, this.pullLabel()]);
          }
          break;
        default:
          throw new Error('Invalid IMP');
      }
    }
    return program;
  }
  
  private pullNumber(): number {
    const sign = this.pullChar();
    if (sign !== '\t' && sign !== ' ') {
      throw new Error('Invalid number sign');
    }
    
    const digits = this.pullUntil('\n');
    if (digits === '') {
      return 0;
    }
    return parseInt(digits.replace(/ /g, '0').replace(/\t/g, '1'), 2) * (sign === '\t' ? -1 : 1);
  }
  
  private pullLabel(): string {
    return this.pullUntil('\n');
  }
  
  private pullImp(): string {
    const c1 = this.pullChar();
    if (!c1) {
      return '';
    }
    if (c1 === '\t') {
      const c2 = this.pullChar();
      if (!c2) {
        throw new Error('Invalid IMP');
      }
      return c1 + c2;
    }
    return c1;
  }
  
  private pullUntil(terminal: string): string {
    let out = '';
    let c: string;
    while (c = this.pullChar()) {
      if (c === terminal) {
        return out;
      }
      out += c;
    }
    throw new Error('Unterminated parameter');
  }
  
  private pullSome(...options: string[]): string {
    const max = Math.max(...options.map(opt => opt.length));
    let out = '';
    let c: string;
    while (c = this.pullChar()) {
      out += c;
      if (out.length > max) {
        throw new Error('Invalid instruction');
      }
      if (options.includes(out)) {
        return out;
      }
    }
    throw new Error('No instruction found');
  }
  
  private pullChar(): string {
    while (this.index < this.code.length) {
      const c = this.code[this.index];
      this.index += 1;
      if (c === ' ' || c === '\t' || c === '\n') {
        return c;
      }
    }
    return '';
  }
}

class Interpreter {
  public output = '';
  private stack: number[] = [];
  private heap = new Map<number, number>();
  
  private pc = 0;
  private callstack: number[] = [];
  
  private inputIndex = 0;
  private labels = new Map<string, number>();
  
  constructor(private program: Program, private input: string) {
    for (const [i, [imp, cmd, arg]] of this.program.entries()) {
      if (imp === '\n' && cmd === '  ' && typeof arg === 'string') {
        if (this.labels.has(arg)) {
          throw new Error(`Duplicate label: ${unbleach(arg)}`);
        }
        this.labels.set(arg, i);
      }
    }
  }
  
  private pop(): number {
    const n = this.stack.pop();
    if (n === undefined) {
      throw new Error('pop on an empty stack');
    }
    return n;
  }
  
  private read(): string {
    const c = this.input[this.inputIndex];
    if (c === undefined) {
      throw new Error('read on empty input');
    }
    this.inputIndex += 1;
    return c;
  }
  
  private readUntil(terminator: string): string {
    let out = '';
    let c;
    while ((c = this.read()) !== terminator) {
      out += c;
    }
    return out;
  }
  
  private jump(label: string): void {
    const target = this.labels.get(label);
    if (target === undefined) {
      throw new Error(`Jump to unknown label: ${unbleach(label)}`);
    }
    this.pc = target + 1;
  }
  
  public run(): void {
    main:
    while (this.pc < this.program.length) {
      const [imp, cmd, arg] = this.program[this.pc];
      let a: number;
      let b: number;
      let s: string;
      let maybe: number | undefined;
      switch (imp + cmd) {
        // Stack Manipulation
        case '  ': // Push n onto the stack.
          this.stack.push(arg as number);
          break;
        case ' \t ': // Duplicate the nth value from the top of the stack and push onto the stack.
          maybe = this.stack[this.stack.length - (arg as number) - 1];
          if (maybe === undefined) {
            throw new Error('duplicate beyond stack')
          }
          this.stack.push(maybe);
          break;
        case ' \t\n': // Discard the top n values below the top of the stack from the stack. (For n<**0** or **n**>=stack.length, remove everything but the top value.)
          if ((arg as number) < 0 || (arg as number) >= this.stack.length) {
            this.stack = [this.pop()]
          } else {
            const top = this.pop();
            this.stack = this.stack.slice(0, this.stack.length - (arg as number));
            this.stack.push(top);
          }
          break;
        case ' \n ': // Duplicate the top value on the stack.
          a = this.pop();
          this.stack.push(a, a);
          break;
        case ' \n\t': // Swap the top two value on the stack.
          a = this.pop();
          b = this.pop();
          this.stack.push(a, b);
          break;
        case ' \n\n': // Discard the top value on the stack.
          this.pop();
          break;
        // Arithmetic
        case '\t   ': // Pop a and b, then push b+a.
          a = this.pop();
          b = this.pop();
          this.stack.push(b + a);
          break;
        case '\t  \t': // Pop a and b, then push b-a.
          a = this.pop();
          b = this.pop();
          this.stack.push(b - a);
          break;
        case '\t  \n': // Pop a and b, then push b*a.
          a = this.pop();
          b = this.pop();
          this.stack.push(b * a);
          break;
        case '\t \t ': // Pop a and b, then push b/a*. If a is zero, throw an error. 
          a = this.pop();
          b = this.pop();
          if (a === 0) {
            throw new Error('Division by zero');
          }
          this.stack.push(Math.floor(b / a));
          break;
        case '\t \t\t': // Pop a and b, then push b%a*. If a is zero, throw an error.
          a = this.pop();
          b = this.pop();
          if (a === 0) {
            throw new Error('Remainder of division by zero');
          }
          this.stack.push(b - a * Math.floor(b / a));
          break;
        // Heap Access
        case '\t\t ': // Pop a and b, then store a at heap address b.
          a = this.pop();
          b = this.pop();
          this.heap.set(b, a);
          break;
        case '\t\t\t': // Pop a and then push the value at heap address a onto the stack.
          a = this.pop();
          maybe = this.heap.get(a);
          if (maybe === undefined) {
            throw new Error('Undefined heap address');
          }
          this.stack.push(maybe);
          break;
        // Input/Output
        case '\t\n  ': // Pop a value off the stack and output it as a character.
          this.output += String.fromCharCode(this.pop());
          break;
        case '\t\n \t': // Pop a value off the stack and output it as a number.
          this.output += this.pop();
          break;
        case '\t\n\t ': // Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
          s = this.read();
          b = this.pop();
          this.heap.set(b, s.charCodeAt(0));
          break;
        case '\t\n\t\t': // Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.
          a = parseInt(this.readUntil('\n'));
          b = this.pop();
          this.heap.set(b, a);
          break;
        // Flow Control
        case '\n  ': // Mark a location in the program with label n.
          // no-op
          break;
        case '\n \t': // Call a subroutine with the location specified by label n.
          this.callstack.push(this.pc);
          this.jump(arg as string);
          continue main;
        case '\n \n': // Jump unconditionally to the position specified by label n.
          this.jump(arg as string);
          continue main;
        case '\n\t ': // Pop a value off the stack and jump to the label specified by n if the value is zero.
          if (this.pop() === 0) {
            this.jump(arg as string);
            continue main;
          }
          break;
        case '\n\t\t': // Pop a value off the stack and jump to the label specified by n if the value is less than zero.
          if (this.pop() < 0) {
            this.jump(arg as string);
            continue main;
          }
          break;
        case '\n\t\n': // Exit a subroutine and return control to the location from which the subroutine was called.
          maybe = this.callstack.pop();
          if (maybe === undefined) {
            throw new Error('return without being in a subroutine');
          }
          this.pc = maybe + 1;
          continue main;
        case '\n\n\n': // Exit the program.
          return;
        default:
          throw new Error(`Unknown command: ${unbleach(imp + cmd)}`);
      }
      this.pc += 1;
    }
    throw new Error('Unclean termination');
  }
}

export function whitespace(code: string, input: string = ''): string {
  let parser = new Parser(code);
  let program = parser.parse();
  let interpreter = new Interpreter(program, input);
  interpreter.run();
  return interpreter.output;
};
                             
___________________________________________________
const SPACE =                    'SPACE'
const TAB =                      'TAB'
const NEW_LINE =                 'NEW_LINE'
const EXIT_COMMAND =             '$EXIT$'
const JUMP_COMMAND =             '$JUMP$:'
const allowedCharacters =        { ' ': SPACE, '\t' : TAB, '\n' : NEW_LINE }
type SentenceChar =              typeof SPACE
    | typeof TAB
    | typeof NEW_LINE

enum OperationTypes {
    STACK_PUSH =                        'STACK_PUSH',
    STACK_DUPLICATE_ONE =               'STACK_DUPLICATE_ONE',
    STACK_DUPLICATE_NTH =               'STACK_DUPLICATE_NTH',
    STACK_DISCARD_ONE =                 'STACK_DISCARD_ONE',
    STACK_DISCARD_MANY =                'STACK_DISCARD_MANY',
    STACK_SWAP =                        'STACK_SWAP',
    ARITHMETICS_SUM =                   'ARITHMETICS_SUM',
    ARITHMETICS_SUBTRACT =              'ARITHMETICS_SUBTRACT',
    ARITHMETICS_MUL =                   'ARITHMETICS_MUL',
    ARITHMETICS_DIV =                   'ARITHMETICS_DIV',
    ARITHMETICS_MOD =                   'ARITHMETICS_MOD',
    IO_OUTPUT_NUMBER =                  'IO_OUTPUT_NUMBER',
    IO_OUTPUT_CHARACTER =               'IO_OUTPUT_CHARACTER',
    IO_READ_NUMBER =                    'IO_READ_NUMBER',
    IO_READ_CHARACTER =                 'IO_READ_CHARACTER',
    FLOW_CONTROL_MARK =                 'FLOW_CONTROL_MARK',
    FLOW_CONTROL_JUMP_ZERO =            'FLOW_CONTROL_JUMP_ZERO',
    FLOW_CONTROL_JUMP_LESS =            'FLOW_CONTROL_JUMP_LESS',
    FLOW_CONTROL_JUMP =                 'FLOW_CONTROL_JUMP',
    FLOW_CONTROL_SUB_CALL =             'FLOW_CONTROL_SUB_CALL',
    FLOW_CONTROL_SUB_EXIT =             'FLOW_CONTROL_SUB_EXIT',
    FLOW_CONTROL_EXIT =                 'FLOW_CONTROL_EXIT',
    HEAP_STORE =                        'HEAP_STORE',
    HEAP_PUSH =                         'HEAP_PUSH'
}

enum DataTypes {
    NUMBER =                            'NUMBER',
    LABEL =                             'LABEL',
    INPUT_STREAM =                      'INPUT_STREAM'
}

type OperationObject = {
    SPACE? :                            object,
    TAB? :                              object,
    NEW_LINE? :                         object,
    operation? :                        OperationTypes,
    argument? :                         DataTypes
}

enum SentenceStates {
    READY =                             'READY',
    IN_PROGRESS =                       'IN_PROGRESS',
    WAITING_FOR_NUMBER =                'WAITING_FOR_NUMBER',
    WAITING_FOR_LABEL =                 'WAITING_FOR_LABEL',
    WAITING_FOR_INPUT_STREAM =          'WAITING_FOR_INPUT_STREAM'
}

type SentenceIterator = {
    [Symbol.iterator](): {
        next():  {
            done: boolean,
            value: Sentence | undefined
        }
    }
}

enum Errors {
    STACK_IS_EMPTY = 'Stack is empty. Cannot perform requested operation',
    STACK_LESS_THAN_2 = 'Stack has less than 2 values. Cannot perform requested operation',
    DIVISION_BY_ZERO = 'Can not perform division by 0',
    OUT_OF_BOUNDARY_INDEX = 'Out of boundary index',
    NO_SUCH_MARK = 'No such mark',
    MARKS_REPEAT = 'Marks repeat',
    UNCLEAN_TERMINATION = 'Program wasn\'t correctly terminated',
    SUB_RETURN_OUTSIDE_SUB_CALL = 'Cannot return from subroutine outside of subroutine call'
}

class Utils {
    static getRandomInt (min: number, max: number): number {
        return ~~(Math.random() * (max - min) + min)
    }

    static encodeNumber (number: number): string {
        let encodedNumber = number.toString(2)
            .replace(/1/g, '\t')
            .replace(/0/g, ' ')
            .replace('-', '\t')
        return number > 0 ? ' ' + encodedNumber : encodedNumber
    }

    static getSourceCodeForPushingNNumbersIntoTheStack (...args: number[]): string {
        if (args.length) {
            return args.reduce((sourceCode, arg) => sourceCode + `  ${Utils.encodeNumber(arg)}\n`, '')
        } else return '   \n   \t\n'
    }

    static mod (n1: number, n2: number): number {
        return ((n1 % n2) + n2) % n2;
    }
}


interface IMemory {
    push (number: number): void
}

class Memory implements IMemory {
    private static instance: Memory
    private stack: number[] = []
    private heap: number[] = []
    private marks: Map<string, number> = new Map()
    private subRoutineCallPosition: number[] = []

    constructor () {
        if (Memory.instance) {
            return Memory.instance
        }

        Memory.instance = this
    }

    heapGet (location: number): number | undefined {
        return this.heap[location]
    }

    heapStore (location: number, value: number) {
        this.heap[location] = value
    }

    push (number: number) {
        this.stack.push(number)
    }

    pop (): number {
        if (!this.stack.length) throw new Error(Errors.STACK_IS_EMPTY)
        return this.stack.pop()!
    }

    swap () {
        if (this.stack.length <= 1) throw new Error(Errors.STACK_LESS_THAN_2)
        const length = this.stack.length
        let tmp = this.stack[length - 1]
        this.stack[length - 1] = this.stack[length - 2]
        this.stack[length - 2] = tmp
    }

    discard (): void
    discard (n: number): void
    discard (n?: number): void {
        if (!this.stack.length) throw new Error(Errors.STACK_IS_EMPTY)
        if (!n) {
            this.stack.pop()
        } else {
            const lastValue = this.stack[this.stack.length - 1]
            if (n < 0 || n >= this.stack.length) {
                this.stack = [lastValue]
            } else {
                this.stack = this.stack.slice(0, this.stack.length - 1 - n)
                this.stack.push(lastValue)
            }
        }
    }

    duplicate (): void
    duplicate (n: number): void
    duplicate (n?: number): void {
        if (!this.stack.length) throw new Error(Errors.STACK_IS_EMPTY)
        if (this.stack.length) {
            if (!n) {
                this.stack.push(this.stack[this.stack.length - 1])
            } else {
                if (this.stack[this.stack.length - n - 1]) {
                    this.stack.push(this.stack[this.stack.length - n - 1])
                } else throw new Error(Errors.OUT_OF_BOUNDARY_INDEX)
            }
        }
    }

    saveMark (mark: string, position: string) {
        if (this.marks.has(mark)) throw new Error(Errors.MARKS_REPEAT)
        this.marks.set(mark, Number.parseInt(position))
    }

    getPosition (mark: string): number {
        if (!this.marks.get(mark)) throw new Error(Errors.NO_SUCH_MARK)
        return this.marks.get(mark)!
    }

    getStack () {
        return [...this.stack]
    }

    getHeap () {
        return [...this.heap]
    }

    reset () {
        this.stack = []
        this.heap = []
        this.marks = new Map()
        this.subRoutineCallPosition = []
    }


    subRoutinePush (position: number) {
        this.subRoutineCallPosition.push(position)
    }

    subRoutinePop (): number {
        return this.subRoutineCallPosition.pop()!
    }
}

interface IOperation {
    run (arg?: string | number, inputStream?: string | null): void | string
}

class Div implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error (Errors.STACK_LESS_THAN_2)
        const n1 = new Memory().pop()
        const n2 = new Memory().pop()
        if (n1 === 0 || n1 === -0) throw new Error(Errors.DIVISION_BY_ZERO)
        else new Memory().push(Math.floor(n2 / n1))
    }
}

class Mod implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error (Errors.STACK_LESS_THAN_2)
        const n1 = new Memory().pop()
        const n2 = new Memory().pop()
        if (n1 === 0 || n1 === -0) throw new Error(Errors.DIVISION_BY_ZERO)
        else new Memory().push(Utils.mod(n2, n1))
    }
}

class Mul implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error (Errors.STACK_LESS_THAN_2)
        const n1 = new Memory().pop()
        const n2 = new Memory().pop()
        new Memory().push(n1 * n2)
    }
}

class Subtract implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error (Errors.STACK_LESS_THAN_2)
        const n1 = new Memory().pop()
        const n2 = new Memory().pop()
        new Memory().push(n2 - n1)
    }
}

class Sum implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error (Errors.STACK_LESS_THAN_2)
        const n1 = new Memory().pop()
        const n2 = new Memory().pop()
        new Memory().push(n1 + n2)
    }
}

class Exit implements IOperation {
    run (): string {
        new Memory().reset()
        return EXIT_COMMAND
    }
}

class Jump implements IOperation {
    run (arg: string): string | void {
        const [mark,] = arg.split(':')
        return JUMP_COMMAND + new Memory().getPosition(mark).toString()
    }
}

class JumpLess implements IOperation {
    run (arg: string): string | void {
        const condition = new Memory().pop()
        if (condition < 0) {
            const [mark,] = arg.split(':')
            return JUMP_COMMAND + new Memory().getPosition(mark).toString()
        }
    }
}

class JumpZero implements IOperation {
    run (arg: string): string | void {
        const condition = new Memory().pop()
        if (!condition) {
            const [mark,] = arg.split(':')
            return JUMP_COMMAND + new Memory().getPosition(mark).toString()
        }
    }
}

class SubCall implements IOperation {
    run (arg: string): void | string {
        const [mark, location] = arg.split(':')
        new Memory().subRoutinePush(Number.parseInt(location))
        return JUMP_COMMAND + new Memory().getPosition(mark).toString()
    }
}

class SubExit implements IOperation {
    run (): string {
        const backPosition = new Memory().subRoutinePop()
        if (backPosition === undefined) throw new Error (Errors.SUB_RETURN_OUTSIDE_SUB_CALL)
        return JUMP_COMMAND + backPosition.toString()
    }
}

class HeapPushInStack implements IOperation {
    run () {
        const location = new Memory().pop()
        const valueToPush = new Memory().heapGet(location)
        if (valueToPush !== undefined) {
            new Memory().push(valueToPush)
        }
    }
}

class Store implements IOperation {
    run () {
        if (new Memory().getStack().length <= 1) throw new Error(Errors.STACK_LESS_THAN_2)
        const value = new Memory().pop()
        const location = new Memory().pop()
        new Memory().heapStore(location, value)
    }
}

class OutputCharacter implements IOperation {
    run (): string {
        const charCode = new Memory().pop()
        return String.fromCharCode(charCode)
    }
}

class OutputNumber implements IOperation {
    run (): string {
        const number = new Memory().pop()
        return number.toString(10)
    }
}

class ReadCharacter implements IOperation {
    run (_: string, inputStream: string): void {
        const location = new Memory().pop()
        new Memory().heapStore(location, inputStream.charCodeAt(0))
    }
}

class ReadNumber implements IOperation {
    run (_: string, inputStream: string): void {
        const location = new Memory().pop()
        if (!Number.isNaN(Number.parseInt(inputStream))) {
            new Memory().heapStore(location, Number.parseInt(inputStream))
        }
    }
}

class DiscardMany implements IOperation {
    run (arg: number) {
        new Memory().discard(arg)
    }
}

class DiscardOne implements IOperation {
    run () {
        new Memory().discard()
    }
}

class DuplicateNth implements IOperation {
    run (arg: number) {
        new Memory().duplicate(arg)
    }
}

class DuplicateOne implements IOperation {
    run () {
        new Memory().duplicate()
    }
}

class Push implements IOperation {
    run (number: number) {
        new Memory().push(number)
    }
}

class Swap implements IOperation {
    run () {
        new Memory().swap()
    }
}

class OperationFactory {
    getOperation (type: OperationTypes): IOperation {
        switch (type) {
            case OperationTypes.STACK_PUSH: return new Push()
            case OperationTypes.STACK_SWAP: return new Swap()
            case OperationTypes.STACK_DISCARD_ONE: return new DiscardOne()
            case OperationTypes.STACK_DISCARD_MANY: return new DiscardMany()
            case OperationTypes.STACK_DUPLICATE_ONE: return new DuplicateOne()
            case OperationTypes.STACK_DUPLICATE_NTH: return new DuplicateNth()
            case OperationTypes.ARITHMETICS_SUM: return new Sum()
            case OperationTypes.ARITHMETICS_SUBTRACT: return new Subtract()
            case OperationTypes.ARITHMETICS_MUL: return new Mul()
            case OperationTypes.ARITHMETICS_DIV: return new Div()
            case OperationTypes.ARITHMETICS_MOD: return new Mod()
            case OperationTypes.IO_OUTPUT_NUMBER: return new OutputNumber()
            case OperationTypes.IO_OUTPUT_CHARACTER: return new OutputCharacter()
            case OperationTypes.IO_READ_NUMBER: return new ReadNumber()
            case OperationTypes.IO_READ_CHARACTER: return new ReadCharacter()
            case OperationTypes.FLOW_CONTROL_EXIT: return new Exit()
            case OperationTypes.HEAP_PUSH: return new HeapPushInStack()
            case OperationTypes.HEAP_STORE: return new Store()
            case OperationTypes.FLOW_CONTROL_JUMP_ZERO: return new JumpZero()
            case OperationTypes.FLOW_CONTROL_JUMP_LESS: return new JumpLess()
            case OperationTypes.FLOW_CONTROL_JUMP: return new Jump()
            case OperationTypes.FLOW_CONTROL_SUB_CALL: return new SubCall()
            case OperationTypes.FLOW_CONTROL_SUB_EXIT: return new SubExit()
            default: throw new Error('Not implemented yet ' + type)
        }
    }
}

const operations = {
    SPACE: {
        SPACE: {
            operation: OperationTypes.STACK_PUSH,
            argument: DataTypes.NUMBER
        },
        TAB: {
            SPACE: {
                operation: OperationTypes.STACK_DUPLICATE_NTH,
                argument: DataTypes.NUMBER
            },
            NEW_LINE: {
                operation: OperationTypes.STACK_DISCARD_MANY,
                argument: DataTypes.NUMBER
            }
        },
        NEW_LINE: {
            SPACE: {
                operation: OperationTypes.STACK_DUPLICATE_ONE
            },
            TAB: {
                operation: OperationTypes.STACK_SWAP
            },
            NEW_LINE: {
                operation: OperationTypes.STACK_DISCARD_ONE
            }
        }
    },
    TAB: {
        SPACE: {
            SPACE: {
                SPACE: {
                    operation: OperationTypes.ARITHMETICS_SUM
                },
                TAB: {
                    operation: OperationTypes.ARITHMETICS_SUBTRACT
                },
                NEW_LINE: {
                    operation: OperationTypes.ARITHMETICS_MUL
                }
            },
            TAB: {
                SPACE: {
                    operation: OperationTypes.ARITHMETICS_DIV
                },
                TAB: {
                    operation: OperationTypes.ARITHMETICS_MOD
                }
            }
        },
        NEW_LINE: {
            SPACE: {
                TAB: {
                    operation: OperationTypes.IO_OUTPUT_NUMBER
                },
                SPACE: {
                    operation: OperationTypes.IO_OUTPUT_CHARACTER
                }
            },
            TAB: {
                TAB: {
                    operation: OperationTypes.IO_READ_NUMBER,
                    argument: DataTypes.INPUT_STREAM
                },
                SPACE: {
                    operation: OperationTypes.IO_READ_CHARACTER,
                    argument: DataTypes.INPUT_STREAM
                }
            }
        },
        TAB: {
            SPACE: {
                operation: OperationTypes.HEAP_STORE
            },
            TAB: {
                operation: OperationTypes.HEAP_PUSH
            }
        }
    },
    NEW_LINE: {
        NEW_LINE: {
            NEW_LINE: {
                operation: OperationTypes.FLOW_CONTROL_EXIT
            }
        },
        SPACE: {
            SPACE: {
                operation: OperationTypes.FLOW_CONTROL_MARK,
                argument: DataTypes.LABEL
            },
            NEW_LINE: {
                operation: OperationTypes.FLOW_CONTROL_JUMP,
                argument: DataTypes.LABEL
            },
            TAB: {
                operation: OperationTypes.FLOW_CONTROL_SUB_CALL,
                argument: DataTypes.LABEL
            }
        },
        TAB: {
            SPACE: {
                operation: OperationTypes.FLOW_CONTROL_JUMP_ZERO,
                argument: DataTypes.LABEL
            },
            TAB: {
                operation: OperationTypes.FLOW_CONTROL_JUMP_LESS,
                argument: DataTypes.LABEL
            },
            NEW_LINE: {
                operation: OperationTypes.FLOW_CONTROL_SUB_EXIT
            }
        }
    }
}

class Sentence {
    private sentenceCharsChain: OperationObject = operations
    private _operationType: OperationTypes | null = null
    private state: SentenceStates = SentenceStates.IN_PROGRESS
    private sign: typeof SPACE | typeof TAB | null = null
    private number: string | number = '0'
    private _label: string = ''
    private inputStream: string | undefined = undefined

    constructor (private readonly _startPosition: number) {}

    public feed (sentenceChar: SentenceChar) {
        if (this.sentenceCharsChain[sentenceChar] !== undefined) {
            this.sentenceCharsChain = this.sentenceCharsChain[sentenceChar] as OperationObject
        } else throw new Error ('Cannot parse source code')
        this.updateSentenceReadiness()
    }

    public feedNumber (sentenceChar: SentenceChar) {
        if (!this.sign) {
            if (sentenceChar === NEW_LINE) throw new Error ('Cannot parse number code')
            this.sign = sentenceChar
        } else {
            if (sentenceChar === NEW_LINE) {
                this.state = SentenceStates.READY
                this.number = Number.parseInt(this.number as string, 2)
            }
            else {
                this.number += sentenceChar === SPACE ? '0' : '1'
            }
        }
    }

    feedInputStream (inputStream: string) {
        this.inputStream = inputStream
        this.state = SentenceStates.READY
    }

    public getSentenceReadiness () {
        return this.state
    }

    public updateSentenceReadiness () {
        if (Object.keys(this.sentenceCharsChain).includes('operation')) {
            this._operationType = this.sentenceCharsChain.operation!
            switch (this.sentenceCharsChain.argument) {
                case DataTypes.INPUT_STREAM: this.state = SentenceStates.WAITING_FOR_INPUT_STREAM; break
                case DataTypes.NUMBER: this.state = SentenceStates.WAITING_FOR_NUMBER; break
                case DataTypes.LABEL: this.state = SentenceStates.WAITING_FOR_LABEL; break
                default: this.state = SentenceStates.READY
            }
        }
    }

    public execute (): void | string {
        if (this.state === SentenceStates.READY) {
            const operationFactory = new OperationFactory()
            const operation = operationFactory.getOperation(this.operationType!)
            if (this.label) {
                return operation.run(this.label)
            } else {
                return operation.run(this.sign === SPACE ? this.number : -this.number, this.inputStream !== undefined ? this.inputStream : null)
            }
        }
    }

    feedLabel (sentenceChar: SentenceChar, position: number) {
        if (sentenceChar === NEW_LINE) {
            this.state = SentenceStates.READY
            this._label += '\n:' + position.toString(10)
        } else {
            this._label += sentenceChar === SPACE ? ' ' : '\t'
        }
    }

    get operationType (): OperationTypes | null {
        return this._operationType
    }

    get label (): string {
        return this._label
    }

    get startPosition (): number {
        return this._startPosition
    }
}

class SentencesBuilder {
    private inputTimes: number = 0
    private readonly inputStream: string[] = []
    private sourceCode: string
    private _sourceCodePointer: number = 0

    constructor (sourceCode: string, inputStreamString: string = '') {
        this.sourceCode = sourceCode
        if (inputStreamString.includes('\n'))
            this.inputStream = inputStreamString.split('\n')
        else {
            let tmp = []
            for (let char of inputStreamString) tmp.push(char)
            this.inputStream = tmp
        }
    }

    private static parseChar (char: string): SentenceChar | null {
        return char in allowedCharacters ? allowedCharacters[char as ' ' | '\t' | '\n'] as SentenceChar : null
    }

    public buildSentences (): SentenceIterator {
        const that = this
        return {
            [Symbol.iterator]() {
                return {
                    next () {
                        const sentence = new Sentence(that._sourceCodePointer)
                        let done = false
                        while (sentence.getSentenceReadiness() !== SentenceStates.READY) {
                            if (sentence.getSentenceReadiness() === SentenceStates.IN_PROGRESS ||
                                sentence.getSentenceReadiness() === SentenceStates.WAITING_FOR_LABEL ||
                                sentence.getSentenceReadiness() === SentenceStates.WAITING_FOR_NUMBER) {
                                if (that.sourceCode.length === that._sourceCodePointer) {
                                    done = true
                                    break
                                }
                                const currentChar = SentencesBuilder.parseChar(that.sourceCode[that._sourceCodePointer++])
                                if (currentChar) {
                                    switch (sentence.getSentenceReadiness()) {
                                        case SentenceStates.IN_PROGRESS: sentence.feed(currentChar); break
                                        case SentenceStates.WAITING_FOR_LABEL: sentence.feedLabel(currentChar, that._sourceCodePointer); break
                                        case SentenceStates.WAITING_FOR_NUMBER: sentence.feedNumber(currentChar); break
                                    }
                                }
                            } else if (sentence.getSentenceReadiness() === SentenceStates.WAITING_FOR_INPUT_STREAM) {
                                sentence.feedInputStream(that.inputStream[that.inputTimes++])
                            }
                        }
                        return done ? {
                            value: undefined,
                            done: true
                        } : {
                            value: sentence,
                            done: false
                        }
                    }
                }
            }
        }
    }

    findMarks () {
        const sB = new SentencesBuilder(this.sourceCode)
        let acc = 0
        for (let sentence of sB.buildSentences()) {
            if (sentence && sentence.operationType === OperationTypes.FLOW_CONTROL_MARK) {
                const [mark, position] = sentence.label.split(':')
                const diff = Number.parseInt(position) - sentence.startPosition
                const newPosition = (Number.parseInt(position) - diff - acc).toString()
                this.sourceCode = this.sourceCode.substring(0, sentence.startPosition - acc) + this.sourceCode.substring(Number.parseInt(position) - acc, this.sourceCode.length)
                new Memory().saveMark(mark, newPosition)
                acc += diff
            }
        }
    }

    set sourceCodePointer (value: number) {
        this._sourceCodePointer = value
    }
}

class Whitespace {
    private readonly sourceCode: string
    private readonly inputStream: string
    private output: string = ''

    constructor (sourceCode: string, inputStream: string = '') {
        this.sourceCode = sourceCode
        this.inputStream = inputStream
    }

    readSourceCode (): string | void {
        const sB = new SentencesBuilder(this.sourceCode, this.inputStream)
        sB.findMarks()
        for (let sentence of sB.buildSentences()) {
            try {
                if (sentence) {
                    const result = sentence.execute()
                    if (result) {
                        if (result === '$EXIT$') {
                            return this.output
                        } else if (/\$JUMP\$/.test(result)) {
                            const [, position] = result.split(':')
                            sB.sourceCodePointer = Number.parseInt(position)
                        } else {
                            this.output += result
                        }
                    }
                }
            } catch (e) {
                throw new Error(e.message)
            }
        }
        throw new Error(Errors.UNCLEAN_TERMINATION)
    }
}

export function whitespace (sourceCode: string, inputStream: string = ''): string | void {
    new Memory().reset()
    if (!sourceCode) throw new Error('Source code cannot be empty')
    const ws = new Whitespace(sourceCode, inputStream)
    return ws.readSourceCode()
}

        Best Practices0
        Clever0
    0
    Fork
    Link

Lidiya13, ryryurueu

function unbleach (n: string) {
  if (n) return n.replace(/ /g, 's').replace(/\t/g, 't').replace(/\n/g, 'n');
}

export function whitespace(code:string, input?:string):string {
  let output = '', stack: any[] = []; const heap: any = {};
  const p = parser(code)
  const labels: any = {}
  while (true) {
    const cmd = p.next()
    if (cmd === null) {
      break
    }
    if (cmd.cmd === "mark-label") {
      if (typeof labels[cmd.label] !== "undefined") {
        throw new Error("duplicate label not allowed")
      }
      labels[cmd.label] = p.position()
    }
  }

  p.jumpTo(0)
  const returns = []
  loop: for (let i = 0; i < 100; i++) {
    const cmd = p.next()
    console.log(cmd)
    switch(cmd.cmd) {
      case "push-onto-stack":
        stack.push(cmd.num)
        break
      case "duplicate-stack-top":
        if (stack.length == 0) {
          throw new Error("cannot duplicate empty stack")
        }
        const top = stack.pop()
        stack.push(top, top)
        break
      case "duplicate-stack-n":
        if (stack.length == 0) {
          throw new Error("cannot duplicate on empty stack")
        }
        if (cmd.n < 0 || cmd.n >= stack.length) {
          throw new Error("duplicate out of bound stack value")
        }
        const value = stack[stack.length - 1 - cmd.n]
        stack.push(value)
        break
      case "swap-stack-top":
        if (stack.length == 0) {
          throw new Error("cannot swap on empty stack")
        }
        const a = stack[stack.length - 1]
        stack[stack.length - 1] = stack[stack.length - 2]
        stack[stack.length - 2] = a
        break
      case "discard-top":
        if (stack.length == 0) {
          throw new Error("cannot discard from empty stack")
        }
        stack.pop()
        break
      case "discard-n":
        if (stack.length == 0) {
          throw new Error("cannot discard from empty stack")
        }
        if (cmd.n < 0 || cmd.n >= stack.length) {
          stack = [stack.pop()]
        } else {
          stack = stack.slice(0, stack.length - 1 - cmd.n).concat([stack.pop()])
        }
        break
      case "pop-out-num":
        if (stack.length == 0) {
          throw new Error("cannot pop from empty stack")
        }
        output += "" + stack.pop()
        break
      case "pop-out-char":
        if (stack.length == 0) {
          throw new Error("cannot pop from empty stack")
        }
        output += String.fromCharCode(stack.pop())
        break
      case "heap-write":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
      {
        const a = stack.pop()
        const b = stack.pop()
        heap[b] = a
        break
      }
      case "read-in-num":
        if (stack.length < 1) {
          throw new Error("stack is smaller than 1")
        }
        // @ts-ignore
        const ind = input.indexOf("\n")
        if (ind < 0) {
          throw new Error("input empty")
        }
        // @ts-ignore
        const num = parseInt(input.slice(0, ind))
        // @ts-ignore
        input = input.slice(ind+1)
        heap[stack.pop()] = num
        break
      case "read-in-char":
        if (stack.length < 1) {
          throw new Error("stack is smaller than 1")
        }
        // @ts-ignore
        if (input.length < 1) {
          throw new Error("input empty")
        }
        // @ts-ignore
        const char = input[0]
        // @ts-ignore
        input = input.slice(1)
        heap[stack.pop()] = char.charCodeAt(0)
        break
      case "heap-read":
        if (stack.length < 1) {
          throw new Error("stack is smaller than 1")
        }
      {
        const a = stack.pop()
        if (typeof heap[a] === "undefined") {
          throw new Error("heap address "+ a +" not defined")
        }
        stack.push(heap[a])
        break
      }
      case "addition":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
        stack.push(stack.pop() + stack.pop())
        break
      case "subtraction":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
      {
        const a = stack.pop()
        const b = stack.pop()
        stack.push(b-a)
      }
        break
      case "multiplication":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
        stack.push(stack.pop() * stack.pop())
        break
      case "division":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
      {
        const a = stack.pop()
        if (a === 0) {
          throw new Error("division by zero")
        }
        const b = stack.pop()
        stack.push(Math.floor(b/a))
      }
        break
      case "modulo":
        if (stack.length < 2) {
          throw new Error("stack is smaller than 2")
        }
      {
        const a = stack.pop()
        if (a === 0) {
          throw new Error("modulo by zero")
        }
        const b = stack.pop()
        const res = b-(Math.floor(b/a)*a)
        stack.push(res)
      }
        break
      case "jump-if-zero":
        if (stack.length < 1) {
          throw new Error("stack is smaller than 1")
        }
      {
        const a = stack.pop()
        if (a === 0) {
          p.jumpTo(labels[cmd.label])
        }
      }
        break
      case "jump-if-lt-zero":
        if (stack.length < 1) {
          throw new Error("stack is smaller than 1")
        }
      {
        const a = stack.pop()
        if (a < 0) {
          p.jumpTo(labels[cmd.label])
        }
      }
        break
      case "jump":
        p.jumpTo(labels[cmd.label])
        break
      case "call-subroutine":
        returns.push(p.position())
        p.jumpTo(labels[cmd.label])
        break
      case "exit-subroutine":
        if (returns.length < 1) {
          throw new Error("nothing to return to")
        }
        p.jumpTo(returns.pop())
        break
      case "exit":
        break loop
      case "mark-label": // ignored
        break
      default:
        throw new Error("unimplemented cmd: " + cmd.cmd)
    }
  }
  return output;
};

function parser(code: any) {
  let offset = 0
  const eat = (token: any) => {
    if (code[offset] === token) {
      offset++
      return true
    }
    return false
  }
  const skipComments = () => {
    while(offset < code.length && code[offset] !== SPACE && code[offset] !== TAB && code[offset] !== LINEFEED) {
      offset++
    }
  }
  const swtch = (group: any, cases: any) => () => {
    skipComments()
    const c = Object.keys(cases);
    for(let i = 0; i < c.length; i++) {
      if (eat(c[i])) {
        const cmd = cases[c[i]]
        if (typeof cmd === "function") {
          return cmd()
        }
        return cmd
      }
    }
    console.log(unbleach(code.slice(offset)))
    throw new Error(
      "[" + group + "] unexpected token: " +
      unbleach(code[offset]) + ", expected one of: [" +
      unbleach(c.join(",") + "]")
    )
  }
  const parseCommand = swtch("global", {
    [SPACE]: swtch("stack-manipulation", {
      [SPACE]: () => {
        return {
          cmd: "push-onto-stack",
          num: parseNumber()
        }
      },
      [LINEFEED]: swtch("stack-manipulation-linefeed", {
        [SPACE]: {
          cmd: "duplicate-stack-top"
        },
        [TAB]: {
          cmd: "swap-stack-top"
        },
        [LINEFEED]: {
          cmd: "discard-top"
        }
      }),
      [TAB]: swtch("stack-manipulation-tab", {
        [SPACE]: () => ({
          cmd: "duplicate-stack-n",
          n: parseNumber(),
        }),
        [LINEFEED]: () => ({
          cmd: "discard-n",
          n: parseNumber(),
        })
      })
    }),
    [TAB]: swtch("tab-global", {
      [LINEFEED]: swtch("IO", {
        [SPACE]: swtch("IO-out", {
          [SPACE]: {
            cmd: "pop-out-char"
          },
          [TAB]: {
            cmd: "pop-out-num"
          }
        }),
        [TAB]: swtch("IO-in", {
          [SPACE]: () => ({
            cmd: "read-in-char"
          }),
          [TAB]: () => ({
            cmd: "read-in-num"
          })
        })
      }),
      [TAB]: swtch("heap-access", {
        [SPACE]: {
          cmd: "heap-write",
        },
        [TAB]: {
          cmd: "heap-read"
        }
      }),
      [SPACE]: swtch("arithm", {
        [SPACE]: swtch("arithm-space", {
          [SPACE]: {
            cmd: "addition",
          },
          [TAB]: {
            cmd: "subtraction"
          },
          [LINEFEED]: {
            cmd: "multiplication"
          }
        }),
        [TAB]: swtch("arithm-tab", {
          [SPACE]: {
            cmd: "division"
          },
          [TAB]: {
            cmd: "modulo"
          }
        })
      })
    }),
    [LINEFEED]: swtch("flow-control", {
      [TAB]: swtch("flow-control-tab", {
        [SPACE]: () => ({
          cmd: "jump-if-zero",
          label: parseLabel()
        }),
        [TAB]: () => ({
          cmd: "jump-if-lt-zero",
          label: parseLabel()
        }),
        [LINEFEED]: () => ({
          cmd: "exit-subroutine",
        })
      }),
      [SPACE]: swtch("flow-control-space", {
        [SPACE]: () => ({
          cmd: "mark-label",
          label: parseLabel()
        }),
        [TAB]: () => ({
          cmd: "call-subroutine",
          label: parseLabel(),
        }),
        [LINEFEED]: () => ({
          cmd: "jump",
          label: parseLabel(),
        })
      }),
      [LINEFEED]: swtch("flow-control-linefeed", {
        [LINEFEED]: {
          cmd: "exit"
        }
      })
    })
  })
  const parseLabel = () => {
    let label = ""
    while (true) {
      const n = swtch("label", {
        [SPACE]: "s",
        [TAB]: "t",
        [LINEFEED]: null
      })()
      console.log(n)
      if (n === null) {
        break
      }
      label += n
    }
    return label
  }
  const parseNumber = () => {
    
    const sign = swtch("sign", {
      // @ts-ignore
      [TAB]: () => a => -a,
      // @ts-ignore
      [SPACE]: () => a => a
    })()
    const bits = []
    while(true) {
      const n = swtch("number", {
        [SPACE]: "0",
        [TAB]: "1",
        [LINEFEED]: null,
      })()
      if (n === null) {
        break
      }
      bits.push(n)
    }
    if (bits.length == 0) {
      return 0
    }
    return sign(parseInt(bits.join(""), 2))
  }
  return {
    next: () => {
      if (offset >= code.length) {
        return null
      }
      return parseCommand()
    },
    position: () => {
      return offset
    },
    jumpTo: (pos: any) => {
      offset = pos
    }
  }
}

const SPACE = " "
const TAB = "\t"
const LINEFEED = "\n"
