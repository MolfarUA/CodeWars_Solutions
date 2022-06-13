import java.util.ArrayList;
import java.util.List;

public class DeadFish {
  public static int[] parse(String data) {
    int value = 0;
    List<Integer> result = new ArrayList<>();
    for(char letter : data.toCharArray()) {
      switch(letter) {
        case 'i': value++; break;
        case 'd': value--; break;
        case 's': value *= value; break;
        case 'o': result.add(value); break;
        default: throw new IllegalArgumentException("Not valid code letter");
      }
    }
    return result.stream().mapToInt(Integer::intValue).toArray();
  }
}
__________________________________________
import java.util.ArrayList;
import java.util.List;

public class DeadFish {
    /**
     * i - increment
     * d - decrement
     * s - square
     * o - output
     *
     * @param data
     * @return
     */
    public static int[] parse(String data) {
        List<Integer> output = new ArrayList<>();
        int counter = 0;
        CommandFactory commandFactory = new CommandFactory(output);
        for (char code: data.toCharArray()) {
            Command command = commandFactory.getCommand(code);
            counter = command.execute(counter);
        }
        return output.stream().mapToInt(i -> i).toArray();
    }
}

class CommandFactory {

    private final List<Integer> output;

    public CommandFactory(List<Integer> output) {
        this.output = output;
    }

    Command getCommand(char code) {
        switch (code) {
            case 'i': return new IncrementCommand();
            case 'd': return new DecrementCommand();
            case 's': return new SquareCommand();
            case 'o': return new OutputCommand(output);
        }
        throw new RuntimeException("error");
    }
}

interface Command {
    int execute(int data);
}

class IncrementCommand implements Command {

    @Override
    public int execute(int data) {
        return data+1;
    }
}

class DecrementCommand implements Command {

    @Override
    public int execute(int data) {
        return data-1;
    }
}

class SquareCommand implements Command {

    @Override
    public int execute(int data) {
        return data*data;
    }
}

class OutputCommand implements Command {

    private final List<Integer> output;

    public OutputCommand(List<Integer> output) {
        this.output = output;
    }

    @Override
    public int execute(int data) {
        output.add(data);
        return data;
    }
}
__________________________________________
import java.util.ArrayList;
public class DeadFish {
    public static int[] parse(String data) {
        ArrayList<Integer> result = new ArrayList<>();
        int number = 0;
        for(int i = 0; i < data.length(); i++){
          if(data.charAt(i) == 'i'){
            number++;
          }
          else if(data.charAt(i) == 'd'){
            number--;
          }
          else if(data.charAt(i) == 's'){
            number = number * number;
          }
          else if(data.charAt(i) == 'o'){
            result.add(number);
          }
        }
      return result.stream().mapToInt(i -> i).toArray();
    }
}
__________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DeadFish {
    public static int[] parse(String data) {
        List<Integer> result = new ArrayList<Integer>();
        int temp = 0;
        for (String s : data.split("")) {
            switch (s){
                case "i": temp++ ; break;
                case "d": temp-- ; break;
                case "s": temp *= temp; break;
                case "o": result.add(temp);
            }
        }
        return result.stream().mapToInt(i->i).toArray();
    }
}
