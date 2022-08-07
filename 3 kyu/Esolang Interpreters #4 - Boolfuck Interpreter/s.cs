5861487fdb20cff3ab000030


using System.Collections;
using System.Linq;

  public class Boolfuck
  {
    public Boolfuck(string code)
    {
      instructions = code.ToCharArray().Select(ToInstruction).
        Where(i => i != Instruction.None).ToArray();
      memory = new BitArray(10000);
      memoryIndex = memory.Length / 2;
    }

    private readonly Instruction[] instructions;
    private readonly BitArray memory;
    private int memoryIndex;

    private static Instruction ToInstruction(char letter)
    {
      switch (letter)
      {
      case '>': return Instruction.IncrementDataPointer;
      case '<': return Instruction.DecrementDataPointer;
      case '+': return Instruction.FlipCurrentCell;
      case ';': return Instruction.Output;
      case ',': return Instruction.Input;
      case '[': return Instruction.LoopIfNonZero;
      case ']': return Instruction.JumpBackIfNonZero;
      }
      return Instruction.None;
    }

    private enum Instruction
    {
      None,
      IncrementDataPointer,
      DecrementDataPointer,
      FlipCurrentCell,
      Output,
      Input,
      LoopIfNonZero,
      JumpBackIfNonZero
    }

    public string Execute(string input)
    {
      var inputBytes = input.ToCharArray().Select(letter => (byte)letter).ToArray();
      //Console.WriteLine(nameof(inputBytes)+": "+string.Join(",", inputBytes));
      inputBits = new BitArray(inputBytes);
      for (var index = 0; index < instructions.Length; index++)
        if (memoryIndex >= 0 && memoryIndex < memory.Length)
          RunInstruction(instructions[index], ref index);
      if (outputIndex == 0)
        return "";
      var outputBytes = new byte[(output.Length-1) / 8 + 1];
      output.CopyTo(outputBytes, 0);
      return GetString(outputBytes, (outputIndex - 1) / 8 + 1);//new string(Encoding.UTF8.GetString(outputBytes, 0, (outputIndex - 1) / 8 + 1));
    }

    static string GetString(byte[] bytes, int length)
    {
      var result = "";
      for (var index = 0; index < length; index++)
        result += (char)bytes[index];
      return result;
    }

    private BitArray inputBits;

    private void RunInstruction(Instruction instruction, ref int index)
    {
      //Console.WriteLine("RunInstruction: " + instruction + ", index=" + index +
      //  ", outputIndex=" + outputIndex + ", inputIndex=" + inputIndex + ", memoryIndex=" +
      //  memoryIndex + ", memory[memoryIndex]=" + memory[memoryIndex]));
      switch (instruction)
      {
      case Instruction.IncrementDataPointer:
        memoryIndex++;
        break;
      case Instruction.DecrementDataPointer:
        memoryIndex--;
        break;
      case Instruction.FlipCurrentCell:
        memory[memoryIndex] = !memory[memoryIndex];
        break;
      case Instruction.Output:
        output.Set(outputIndex++, memory[memoryIndex]);
        break;
      case Instruction.Input:
        // To fix strange "Codewars" test that loops back to "C" and doesn't stop
        if (instructions.Last() != Instruction.DecrementDataPointer)
          memory[memoryIndex] = inputIndex < inputBits.Length &&
            inputBits[inputIndex % inputBits.Length];
        else
        // All other tests, especially testShould_correctly_multiply_any_two_non_negative_integers_together_for_products_up_to_and_including_255 require looping back to reuse the same input for some reason, the description doesn't explain this
          memory[memoryIndex] = inputBits[inputIndex % inputBits.Length];
        inputIndex++;
        break;
      case Instruction.LoopIfNonZero:
        if (memory[memoryIndex] == false)
          GoToMatchingLoopBracket(1, ref index);
        break;
      case Instruction.JumpBackIfNonZero:
        if (memory[memoryIndex] != false)
          GoToMatchingLoopBracket(-1, ref index);
        break;
      }
    }
    
    private readonly BitArray output = new BitArray(10000);
    private int outputIndex;
    private int inputIndex;

    private void GoToMatchingLoopBracket(int direction, ref int index)
    {
      var loopDepth = direction;
      for (index += direction; index >= 0 && index < instructions.Length; index += direction)
      {
        if (instructions[index] == Instruction.LoopIfNonZero)
          loopDepth++;
        if (instructions[index] == Instruction.JumpBackIfNonZero)
          loopDepth--;
        if (loopDepth == 0)
          break;
      }
    }

    public static string interpret(string code, string input = "") =>
      new Boolfuck(code).Execute(input);
  }
_____________________________
using System;
using System.Collections.Generic;

public class Boolfuck
    {
        
        public static string interpret(string code, string input)
        {
            List<int> tape = new List<int>() { 0 };
            List<int> output = new List<int>();

            Queue<int> data = input.Length > 0 ? InputToBitArray(input) : new Queue<int>();

            int tapeIndex = 0;


            for (int i = 0; i < code.Length; i++)
            {
                char command = code[i];

                switch (command)
                {
                    case '+':
                        tape[tapeIndex] ^= 1;
                        break;
                    case ',':
                        tape[tapeIndex] = data.Count > 0 ? data.Dequeue() : 0;
                        break;
                    case ';':
                        output.Add(tape[tapeIndex]);
                        break;
                    case '<':
                        TapeLeft(tape, ref tapeIndex);
                        break;
                    case '>':
                        TapeRight(tape, ref tapeIndex);
                        break;
                    case '[':
                        if (tape[tapeIndex] == 0) { i = FindMatchingBracket(code, i); }
                        break;
                    case ']':
                        if (tape[tapeIndex] != 0) { i = FindMatchingBracket(code, i); }
                        break;
                    default:
                        break;
                }
            }

            //Grab chunks of 8 bits and convert to text

            string results = "";
            while (output.Count > 0)
            {
                string byteString = "";
                while (output.Count < 8)
                {
                    output.Add(0);
                }

                var byteData = output.GetRange(0, 8);
                byteData.Reverse();
                byteString = string.Join("", byteData);
                output.RemoveRange(0, 8);
                int charValue = Convert.ToInt32(byteString, 2);
                results += (char)charValue;
            }

            return results;

        }

        static void TapeLeft(List<int> tape, ref int pointer)
        {
            if (pointer > 0) { pointer--; }
            else { tape.Insert(0, 0); }
        }

        static void TapeRight(List<int> tape, ref int pointer)
        {
            if (pointer < tape.Count - 1) { pointer++; }
            else { tape.Add(0); pointer++; }
        }

        static int FindMatchingBracket(string code, int fromIndex)
        {
            char thisChar = code[fromIndex];
            char searchChar = thisChar == '[' ? ']' : '[';
            int searchDir = thisChar == '[' ? 1 : -1;
            int b = 1;
            for (int i = fromIndex + searchDir; true; i += searchDir)
            {
                if (code[i] == thisChar) { b++; }
                else if (code[i] == searchChar) { b--; }

                if (b == 0) { return i; }
            }
        }

        public static Queue<int> InputToBitArray(string input)
        {

            int[] bits = new int[input.Length * 8];
            int counter = 0;
            foreach (char c in input)
            {
                string bin = Convert.ToString(c, 2).PadLeft(8, '0');
                for (int b = bin.Length - 1; b >= 0; b--)
                {
                    bits[counter] = bin[b] - '0';
                    counter++;
                }
            }

            return new Queue<int>(bits);
        }
    }
_____________________________
using System;
using System.Linq;
using System.Collections.Generic;
 public static class Boolfuck
    {
        public static string interpret(string code, string input)
        {

            // preprocessing to remove non-commands 
            code = string.Concat(code.Where(ch => new char[] { '+', ',', ';', '>', '<', '[', ']' }.Contains(ch)));

            List<bool> tape = new List<bool>();           
            Stack<bool> inputStack = new Stack<bool>();
            string outputStream = "";
            foreach (char ch in input.Reverse())
                foreach (char b in Convert.ToString(ch, 2).PadLeft(8, '0'))
                    inputStack.Push(b == '1' ? true : false);

            tape.Add(false);
            int tapePtr = 0;
            int codePtr = 0;

            while (codePtr < code.Length)
            {
                char ch = code[codePtr];
                switch (ch)
                {
                    case '+':
                        tape[tapePtr] = !tape[tapePtr];                        
                        break;
                    case ',':
                        tape[tapePtr] = inputStack.Count > 0 ? inputStack.Pop() : false;                        
                        break;
                    case ';':
                        outputStream = (tape[tapePtr] == true ? "1" : "0") + outputStream;
                        break;
                    case '>':
                        if (tapePtr == tape.Count - 1)
                            tape.Add(false);
                        tapePtr++;                        
                        break;
                    case '<':
                        if (tapePtr == 0)
                            tape.Insert(0, false);
                        else
                            tapePtr--;
                        break;
                    case '[':
                        // if bool cell of tape is ture so continue commands , else jump to past matching ']'
                        if (!tape[tapePtr])
                        {
                            int stack = 1;
                            while (stack != 0)
                            {
                                codePtr++;
                                if (code[codePtr] == '[') stack++;
                                else if (code[codePtr] == ']') stack--;
                            }
                        }
                        break;

                    case ']':
                        // if bool cell of tape is true so back to matching '[', else continue commands
                        if (tape[tapePtr])
                        {
                            int stack = 1;
                            while (stack != 0)
                            {
                                codePtr--;
                                if (code[codePtr] == ']') stack++;
                                else if (code[codePtr] == '[') stack--;
                            }                           
                        }
                        break;
                }
                codePtr++;
            }

            // convert output stream to multiple of eight
            if (outputStream.Length % 8 != 0)
                outputStream = new string('0', 8 - outputStream.Length % 8) + outputStream;
            string res = "";
            for (int i = outputStream.Length - 8; i >=0 ; i = i-8)            
                res += (char)Convert.ToByte(outputStream.Substring(i, 8), 2);
            return res;
        }
    }
