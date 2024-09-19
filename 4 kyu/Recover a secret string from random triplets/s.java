53f40dff5f9d31b813000774

import java.lang.String;
import java.lang.Character;
import java.util.List;
import java.util.LinkedList;
import java.util.Arrays;

public class SecretDetective {

    public String recoverSecret(char[][] triplets) {
        List<Character> wordList = new LinkedList<>();
        for (char[] triplet : triplets) {
            int pIndex = -1;
            for (int i = 0; i < 3; i++) {
                int cIndex = wordList.indexOf(triplet[i]);
                if (cIndex != -1) {
                    if (pIndex > cIndex) {
                        Character removed = wordList.remove(cIndex);
                        wordList.add(pIndex, removed);
                        cIndex = pIndex;
                    }
                    pIndex = cIndex;
                } else if (pIndex != -1) {
                    pIndex += 1;
                    wordList.add(pIndex, triplet[i]);
                } else {
                    wordList.add(0, triplet[i]);
                    pIndex = 0;
                }
            }
        }

        return wordList.stream().map(ch -> ch.toString()).reduce((p,n) -> p + n).get();
    }
  
}

################################
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;



public class SecretDetective {

  public static final char EMPTY_CHAR = '-';

  public String recoverSecret(char[][] triplets) {

        String result = getSecretString(triplets);

        return result;
  }
  



    private String getSecretString(char[][] triplets) {

        StringBuilder secretString = new StringBuilder();
        Map<Character,Triplet> firstElementsOfTripletMap = createTripletMapOfFirstElements(triplets);
        while (firstElementsOfTripletMap.size() > 0) {
            Triplet nextObjectOfSecretString = findNextCharacterOfSecretString(firstElementsOfTripletMap);
            secretString.append(nextObjectOfSecretString.firstCharOfTriplet);
            updateFirstElementsOfTripletMap(firstElementsOfTripletMap, nextObjectOfSecretString ,triplets);

        }
        return secretString.toString();
    }

    private void updateFirstElementsOfTripletMap(Map<Character, Triplet> firstElementsOfTripletMap , Triplet nextObjectOfSecretString, char[][] triplets) {
        firstElementsOfTripletMap.remove(nextObjectOfSecretString.firstCharOfTriplet);
        addFirstElementsOfTripletMap(firstElementsOfTripletMap, nextObjectOfSecretString, triplets);
    }

    private void addFirstElementsOfTripletMap(Map<Character, Triplet> firstElementsOfTripletMap, Triplet nextObjectOfSecretString, char[][] triplets) {
        for (int firstPosition : nextObjectOfSecretString.getFirstPositions()){
            char newFirstCharacter = triplets[firstPosition][1];

            triplets[firstPosition][0] = newFirstCharacter;
            triplets[firstPosition][1] = triplets[firstPosition][2];
            triplets[firstPosition][2] = EMPTY_CHAR;

            if (newFirstCharacter != EMPTY_CHAR) {
                Triplet newFirstElem = firstElementsOfTripletMap.get(newFirstCharacter);
                if ( newFirstElem != null){
                    newFirstElem.counterForSecondAndThirdPosition--;
                    newFirstElem.addFirstPosition(firstPosition);
                } else {
                    int counter = countElementsOnSecondAndThirdPosition(newFirstCharacter, triplets);
                    newFirstElem = new Triplet(counter, newFirstCharacter);
                    firstElementsOfTripletMap.put(newFirstCharacter, newFirstElem);
                }
            }
        }

    }

    private Triplet findNextCharacterOfSecretString(Map<Character, Triplet> firstElementsOfTripletMap) {

        if (firstElementsOfTripletMap.size() > 1) {
            return firstElementsOfTripletMap.values().stream()
                    .filter( e-> e.counterForSecondAndThirdPosition == 0)
                    .findFirst()
                    .get();
        }
        return firstElementsOfTripletMap.values().stream()
                .findFirst()
                .get();

    }

    public Map<Character,Triplet> createTripletMapOfFirstElements(char[][] triplets){
        Map<Character,Triplet> firstElementsOfTripletMap = new HashMap<>();
        for (int i =0 ; i< triplets.length ; i++) {
            char firstCharOfTriplet = triplets[i][0];
            Triplet firstElem = firstElementsOfTripletMap.get(firstCharOfTriplet);
            if ( firstElem == null ) {
                int counter = countElementsOnSecondAndThirdPosition(firstCharOfTriplet, triplets);
                firstElem = new Triplet(counter, firstCharOfTriplet);
//                 Task4 task4 = new Task4();
//                 task4.new Triplet();
                firstElementsOfTripletMap.put(firstCharOfTriplet, firstElem);
            }
            firstElem.addFirstPosition(i);
        }

        return firstElementsOfTripletMap;
    }

    private int countElementsOnSecondAndThirdPosition(char firstElemOfTriplet, char[][] triplets) {
        int counter = 0;
        for (int i =0; i < triplets.length ; i++) {
            if (triplets[i][1] == firstElemOfTriplet || triplets[i][2] == firstElemOfTriplet) {
                counter++;
            }
        }

        return counter;
    }


      public static class Triplet {

        private int counterForSecondAndThirdPosition = 0;
        private char firstCharOfTriplet;
        private List<Integer> firstPositions = new ArrayList<>();

        public Triplet(int counterForSecondAndThirdPosition, char firstCharOfTriplet ) {
            this.counterForSecondAndThirdPosition = counterForSecondAndThirdPosition;
            this.firstCharOfTriplet = firstCharOfTriplet;
        }

        public void addFirstPosition(int position){
            firstPositions.add(position);
        }

        public int getCounterForSecondAndThirdPosition() {
            return counterForSecondAndThirdPosition;
        }

        public char getFirstCharOfTriplet() {
            return firstCharOfTriplet;
        }

        public List<Integer> getFirstPositions() {
            return firstPositions;
        }
    }
  
}

##############################
public class SecretDetective {

public String recoverSecret(char[][] triplets) {
	    StringBuilder word = new StringBuilder();
	    String characters = getDistinct(triplets);
	    int pos = 0;
	    while(characters.length() > 0) {
	      char check = characters.charAt(pos);
	      if(isNextLetter(check, triplets, word.toString())) {
	        word.append(check);
	        characters = characters.replaceAll(check + "", "");
	        pos = 0;
	      } else {
	    	  pos++;
	      }
	    }
	    return word.toString();
	  }
	 
	  public boolean isNextLetter(char check, char[][] trips, String word) {
	    for(char [] ls : trips) {
	      if(new String(ls).replaceAll(word.length() > 0 ? "[" + word + "]" : "", "").indexOf(check) > 0) {
	        return false;
	      }
	    }
	    return true;
	  }

	  public String getDistinct(char [][] triplets) {
	    StringBuilder chars = new StringBuilder();
	    for(char [] ls : triplets) {
	      for(char c : ls) {
	        if(chars.toString().indexOf(c) == -1) {
	          chars.append(c);
	        }
	      }
	    }
	    return chars.toString();
	  }
}
