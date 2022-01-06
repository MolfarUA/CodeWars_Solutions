import java.util.*;

public class MorseCodeDecoder {
    public static String decodeMorse(String morseCode) {
        StringBuilder sb = new StringBuilder();
        for (String code: morseCode.split(" {1,2}"))
            sb.append("".equals(code) ? " " : MorseCode.get(code));
        return sb.toString().trim();
    }
    
    public static String decodeBitsAdvanced(String bits) {
        bits = bits.replaceAll("^0*(.*?)0*$","$1");
        int maxGroupOf1Length = Arrays.stream(bits.split("0+"))
                                      .mapToInt(String::length)
                                      .max().orElse(1);
        var stats = Arrays.stream(bits.split("(?=1)(?<=0)|(?=0)(?<=1)"))
                          .mapToInt(String::length)
                          .summaryStatistics();
                                              
        int bound = (int)Math.ceil((stats.getMin()+maxGroupOf1Length) / 2.0);
        if (maxGroupOf1Length == stats.getMin()) bound++;
        int wordbound = (int)Math.ceil((bound + stats.getMax()) / 2.0);
        wordbound = Math.max(wordbound, 5 * stats.getMin());

        return bits.replaceAll(String.format("1{%d,}", bound), "-")
                    .replaceAll(String.format("1{1,%d}", bound), ".")
                    .replaceAll(String.format("0{%d,}", wordbound), "   ")
                    .replaceAll(String.format("0{%d,}",bound), " ")
                    .replaceAll("0","");
    }
}
_______________________________________________
public class MorseCodeDecoder {
    
    public static String decodeBitsAdvanced(String bits) {

        StringBuilder sBits = new StringBuilder(bits.replaceAll("^0+|0+$", "")).append(" ");

        int oneMin = Integer.MAX_VALUE;
        int oneMax = 0;
        int zeroMin = Integer.MAX_VALUE;
        int zeroMax = 0;

        char lastChar = '~';
        int count = 0;
        for (int i = 0; i < sBits.length(); i++) {

            if (sBits.charAt(i) != lastChar) {

                if (lastChar == '0') {
                    if (count < zeroMin) zeroMin = count;
                    if (count > zeroMax) zeroMax = count;
                }

                if (lastChar == '1') {
                    if (count < oneMin) oneMin = count;
                    if (count > oneMax) oneMax = count;
                }

                lastChar = sBits.charAt(i);
                count = 1;

            } else {
                count++;
            }

        }

        StringBuilder morse = new StringBuilder();

        lastChar = '~';
        count = 0;
        for (int i = 0; i < sBits.length(); i++) {
            if (sBits.charAt(i) != lastChar) {

                if (lastChar == '0') {

                    if (zeroMin == zeroMax) {
                        if (zeroMin >= (oneMin * 6)) morse.append("  ");
                        else if (zeroMin > oneMin) morse.append(" ");
                    }
                    else if (!minCloser(count, zeroMin, oneMax)) {
                        int between = 1 + (int) Math.ceil(( zeroMin + zeroMax) / 2.0 );
                        if ( between < count && (minCloser(count, zeroMax, oneMax) || oneMax < count)) morse.append("  ");
                        else morse.append(" ");
                    }

                }

                if (lastChar == '1') {
                    if (oneMin == oneMax) {
                        if (oneMin == zeroMin || zeroMin == Integer.MAX_VALUE) morse.append(".");
                        else if (oneMin < zeroMin) morse.append(".");
                        else morse.append("-");
                    }
                    else if (minCloser(count, oneMin, oneMax)) morse.append(".");
                    else morse.append("-");
                }

                lastChar = sBits.charAt(i);
                count = 1;


            } else {
                count++;
            }
        }

        return morse.append(" ").toString();
    }


    static boolean minCloser(int value, int min, int max){

        int rangeMin = Math.abs(min - value);
        int rangeMax = Math.abs(max - value);

        return  (rangeMin < rangeMax);
    }


    public static String decodeMorse(String morseCode) {

        String[] letters = morseCode.split(" ");
        StringBuilder answer = new StringBuilder();

        for (int i = 0; i < letters.length; i++) {
            if (letters[i].equals("")) answer.append(" ");
            else answer.append(MorseCode.get(letters[i]));
        }

        return answer.toString().trim();
    }
    
}
_______________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class MorseCodeDecoder {
    private static int tu;
    private static float thresh13;
    private static float thresh37;
    
     /**
     * Given a string of ones and its following strings of zeros,
     * returns the Morse symbol (e.g. dot, dash, new-letter, new-word)
     * which these ones and zeros signify).
     * This method works even when there is some variation in the length
     * of the time unit used.
     * 
     * @param one
     * @param zero
     * @return 
     */
    private static String nextTeleFuzzy(String one, String zero) {
        String tele = nextTeleFuzzy(one);
        if ((zero.length() >= thresh13) && (zero.length() < thresh37)) tele += " ";
        else if (zero.length() >= thresh37) tele += "   ";
        return tele;
    }
    
    /**
     * Given a string of ones, returns the Morse symbol
     * (i.e. dot or dash) which these ones signify.
     * This method works even when there is some variation in the length
     * of the time unit used.
     * 
     * @param one
     * @return 
     */
    private static String nextTeleFuzzy(String one) {
        String tele = "";
        if (one.length() <= thresh13) tele += ".";
        else tele += "-";
        return tele;
    }
    
    /**
     * Given a string of bits, which may or may not begin or end with '0's,
     * and which may have some variation in the length of the time unit used,
     * returns the Morse Code translation of this message.
     * @param bits
     * @return 
     */
    public static String decodeBitsAdvanced(String bits) {
        String morse = "";
        bits = bits.replaceAll("^[0]+", "");
        bits = bits.replaceAll("[0]+$", "");
        KMeans km = new KMeans(bits, 3);
        km.converge();
        thresh13 = (km.getTimeUnit(0) + km.getTimeUnit(1)) / 2;
        thresh37 = (km.getTimeUnit(1) + km.getTimeUnit(2)) / 2;
        if (bits.length() > 5) {
            thresh13 *= 1.2;
            thresh37 *= 1.1;
        }
        String[] ones = bits.split("0+");
        String[] zeros = bits.split("1+");
        for (int i = 0; i < zeros.length - 1; i++) {
            morse += nextTeleFuzzy(ones[i], zeros[i + 1]);
        }
        if (ones[0].length() > 0) morse += nextTeleFuzzy(ones[ones.length - 1]);
        return morse;
    }
    
    /**
     * Given a string in Morse Code, returns the English translation.
     * 
     * @param morseCode
     * @return 
     */
    public static String decodeMorse(String morseCode) {
        String results = "";
        morseCode = morseCode.trim().replaceAll(" {3}", " SPACE ");
        // Here, we'd like to trim leading and trailing whitespace.
        // We also know that three spaces are used to separate words.
        // Hence, we leave a symbol that can be tokenized for our while
        // loop to recognize as a [space] character.

        Scanner sc = new Scanner(morseCode);
        while (sc.hasNext()) { 
          String nxt = sc.next();
          if (nxt.equals("SPACE")) results += " ";
          else results += MorseCode.get(nxt);
        }
        return results;
    }
    
        /**
     * The Cluster class provides data structures and methods for clusters
     * in the KMeans algorithm.
     */
    private static class Cluster implements Comparable<Cluster> {
        private float location;
        private float centroid;
        private ArrayList<Integer> currentPoints = new ArrayList<>();
        private ArrayList<Integer> previousPoints = new ArrayList<>();
        
        /**
         * Constructors
         */
        private Cluster(float loc) {
            location = loc;
        }
        
        private Cluster() {
            location = -1;
        }
        
        /**
         * Methods for claiming currentPoints and calculating centroid.
         */
        private void addPoint(int i) {
            currentPoints.add(i);
        }
        
        private boolean didChange() {
            if (previousPoints.size() != currentPoints.size()) return true;
            else return !currentPoints.equals(previousPoints);
        }
        
        private void clearPoints() {
            previousPoints = (ArrayList<Integer>) currentPoints.clone();
            currentPoints.clear();
        }
        
        /**
         * After new points have been assigned to this cluster, this method
         * calculates the new centroid of the cluster and moves the cluster
         * to that location.
         */
        private void update() {
            float sum = 0;
            for (Integer p: currentPoints) {
                sum += p;
            }
            centroid = sum / currentPoints.size();
            setLocation(centroid);
        }
                
        /**
         * Getters and Setters.
         */
        private float getLocation() { return location; }
        private float getDistance(int point) {
            return Math.abs(location - point);
        }
        private void setLocation(float loc) { location = loc; }
        
        @Override
        public int compareTo(Cluster t) {
            if (this.getLocation() > t.getLocation()) return 1;
            else if (this.getLocation() < t.getLocation()) return -1;
            else return 0;
        }
    }
    
    private static class KMeans {    
        /**
         * KMeans attributes.
         */
        private boolean converged = false;
        private final Cluster[] clusters;
        private final String[] bitCollection; // for generating frequency dist.
        private float[] timeUnits = {0, 0, 0};
        private final HashMap<Integer, Integer> dist = new HashMap<>();
        List<Integer> keys;

        public KMeans(String stream, int numClusters) {
            this.clusters = new Cluster[numClusters];
            stream = stream.replaceAll("^[0]+", ""); // remove leading 0s
            stream = stream.replaceAll("[0]+$", ""); // remove trailing 0s

            /**
             * The following if/else block populates this.bitCollection.
             */
            if (stream.length() == 0) {
                bitCollection = new String[1];
                bitCollection[0] = "";
            }
            else {
                String[] ones = stream.split("0+");
                String[] zeros = stream.split("1+");

                if (zeros.length == 0) {
                    bitCollection = new String[1];
                    bitCollection[0] = ones[0];
                }
                else {
                    bitCollection = new String[ones.length + zeros.length - 1];
                    for (int i = 0; i < ones.length - 1; i++) {
                        bitCollection[2*i] = ones[i];
                        bitCollection[2*i+1] = zeros[i+1];
                    }
                    bitCollection[bitCollection.length - 1] = ones[ones.length - 1];
                }
            }

            /**
             * The following for loop populates the this.dist HashMap.
             */
            for (int i = 0; i < bitCollection.length; i++) {
                int l = bitCollection[i].length();
                if (!dist.containsKey(l)) {
                    dist.put(l, 1);
                }
                else dist.put(l, dist.get(l) + 1);
            }
            this.keys = new ArrayList<>(dist.keySet());
                        
            if (keys.size() == 1 || keys.size() == 2) {
                timeUnits[0] = keys.get(0);
                timeUnits[1] = keys.get(0) * 3;
                timeUnits[2] = keys.get(0) * 7;
                converged = true;
            }
            else {
                Collections.sort(keys);
                initializeClusters();
            }
        }

        /**
         * Populates this.clusters with this.numClusters Cluster objects,
         * whose initial locations are from this.keys (the minimum, the
         * maximum, and the middle between the two).
         */
        private void initializeClusters() {
            clusters[0] = new Cluster(keys.get(0));
            clusters[2] = new Cluster(keys.get(keys.size() - 1));
            clusters[1] = new Cluster(
                (keys.get(keys.size() - 1) + keys.get(0)) / 2 + 1);
        }

        /**
         * Assigns cluster-labels to each length-point from the fuzzy input,
         * which is subsequently used by the clusters to re-calculate their
         * centroids and move accordingly.
         */
        public void assignToClosestCluster() {
            clear();
            for (Integer i: keys) {
                Cluster bestCluster = new Cluster();
                float closest = Float.MAX_VALUE;
                for (Cluster c: clusters) {
                    float d = c.getDistance(i);
                    if (d < closest) {
                        closest = d;
                        bestCluster = c;
                    }
                }
                for(int j = 0; j < dist.get(i); j++) {
                    bestCluster.addPoint(i);
                }
            }
        }

        /**
         * Populates this.timeUnits[] with the first, second, and third cluster
         * means, representing the average length of 1 time unit,
         * 3 time units, and 7 time units respectively.
         */
        public void calculateTimeUnits() {
            Cluster[] sortedClusters = clusters.clone();
            Arrays.sort(sortedClusters);
            timeUnits[0] = sortedClusters[0].getLocation();
            timeUnits[1] = sortedClusters[1].getLocation();
            timeUnits[2] = sortedClusters[2].getLocation();
        }

        public void clear() {
            for (Cluster c: clusters) c.clearPoints();
        }

        /**
         * Assigns the closest Cluster to each point, calculates the centroid
         * for those Clusters based off of those points, moves the Clusters
         * to their respective centroids, and repeats until assignment on the next
         * iteration is the same.
         */
        public void converge() {
            if (!converged) {
                assignToClosestCluster();
                while (!converged) {
                    update();
                    assignToClosestCluster();
                    if (!didChange()) converged = true;
                }
                calculateTimeUnits();
            }
        }

        public boolean didChange() {
            for (Cluster c: clusters) if (c.didChange()) return true;
            return false;
        }

        public void update() {
            for (Cluster c: clusters) c.update();
        }

        /**
         * Getters and Setters.
         *
         */
        public float getTimeUnit(int index) { return this.timeUnits[index]; }
    }
}
_______________________________________________
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class MorseCodeDecoder {
    
    private static Pattern BITS_PATTERN  = Pattern.compile("0+|1+");
    private static Map<List<Boolean>,String> CONVERT_BITS = new HashMap<List<Boolean>,String>();
    static {CONVERT_BITS.put(Arrays.asList(true, true, true),    ".");
            CONVERT_BITS.put(Arrays.asList(true, false, true),   "-");
            CONVERT_BITS.put(Arrays.asList(true, false, false),  "-");
            CONVERT_BITS.put(Arrays.asList(false, true, true),   "");
            CONVERT_BITS.put(Arrays.asList(false, false, true),  " ");
            CONVERT_BITS.put(Arrays.asList(false, false, false), "   ");
    }
    
    public static String decodeBitsAdvanced(String bits) {
        String stripBits = bits.replaceAll("^0+|0+$", "");
        if (stripBits.length() == 0) return "";
        
        Map<Integer,Integer> ones = new HashMap<Integer,Integer>(),
                             full = new HashMap<Integer,Integer>();
        Matcher m = BITS_PATTERN.matcher(stripBits);
        while (m.find()) {
            String seq = m.group();
            full.put(seq.length(), full.getOrDefault(seq.length(), 0) + 1);
            if (seq.charAt(0) == '1')
                ones.put(seq.length(), ones.getOrDefault(seq.length(), 0) + 1);
        }
        
        int mi1 = Collections.min(ones.keySet()),
            ma1 = Collections.max(ones.keySet()),
            miF = Collections.min(full.keySet()),
            maF = Collections.max(full.keySet()),
            miG = -1, maG = -1;
        int[] limits = new int[2];
        
        Set<Integer> gaps1    = IntStream.range(mi1+1, ma1).filter(i -> !ones.containsKey(i)).boxed().collect(Collectors.toSet()),
                     gapsFull = IntStream.range(miF+1, maF).filter(i -> !full.containsKey(i)).boxed().collect(Collectors.toSet()),
                     gapsSep  = new HashSet<Integer>();
        if (!gapsFull.isEmpty()) {
            miG = Collections.min(gapsFull);
            maG = Collections.max(gapsFull);
            gapsSep = IntStream.range(miG, maG).filter(i -> !gapsFull.contains(i)).boxed().collect(Collectors.toSet());
        }
        
        if (!gapsFull.isEmpty() && !gapsSep.isEmpty() && !gaps1.isEmpty())  limits = new int[] {miG, maG};
        else if (gapsFull.isEmpty() && full.size() < 3)                     limits = new int[] {miF, maF};
        else if (!gapsFull.isEmpty() && gapsSep.isEmpty())                  limits = gapsFull.size()<3 ?  new int[] {miG, maF} : new int[] {miG, maG};
        else                                                                limits = Arrays.copyOfRange( IntStream.range(miF, maF)
                                                                                                                  .filter( i -> !full .containsKey(i) || full.getOrDefault(i+1,0) > full.get(i)*1.5)
                                                                                                                  .toArray(), 0, 2);
        StringBuilder sb = new StringBuilder ();
        m = BITS_PATTERN.matcher(stripBits);
        while (m.find()) {
            String seq = m.group();
            sb.append( CONVERT_BITS.get(Arrays.asList(seq.charAt(0) == '1', seq.length() <= limits[0], seq.length() <= limits[1])) );
        }
        return sb.toString();
    }
    
    public static String decodeMorse(String morseCode) {
        if (morseCode.length() == 0) return "";
        return Arrays.stream( morseCode.split("   ") )
                     .map( word -> Arrays.stream( word.split(" ") ).map( ch -> MorseCode.get(ch) ).collect(Collectors.joining("")) )
                     .collect(Collectors.joining(" "));
    }
}
