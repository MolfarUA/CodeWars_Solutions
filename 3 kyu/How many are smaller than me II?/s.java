56a1c63f3bc6827e13000006


import java.util.*;

public class Smaller {
	  /*
     * Solution complexity O(n·log n)
     * After days of experiments i reach this solution thinking in a divide
     * and conquer scheme. I finally realized what I was doing was a Merge Sort
     * with one modification to count smallers. Easy peasy after all...
     */
  
    /** as we realize some kind of sort, we need to conserve real index
        of each element and its smallers. We will work with Wrappers.*/
    static class Wrapper {
        int val, realIndex, smallers;

        public Wrapper(int val, int realIndex) {
            this.val = val;
            this.realIndex = realIndex;
            this.smallers = 0;
        }
    }
    
  
    // standard sort, no changes
    public static void sort(Wrapper[] in) {
        if (in.length < 2) { return;  }
        
        int mid = in.length / 2;
        Wrapper[] left = new Wrapper[mid];
        Wrapper[] right = new Wrapper[in.length - mid];
      
        for (int i = 0; i < mid; i++) left[i] = in[i];
        for (int i = 0; i < in.length - mid; i++) right[i] = in[mid + i];
      
        sort(left);
        sort(right);
        merge(left, right, in);
    }

    // modified merge
    private static void merge(Wrapper[] a, Wrapper[] b, Wrapper[] all) {
        int i = 0, j = 0, k = 0;
        while (i < a.length && j < b.length) {
            if (a[i].val > b[j].val) {
                a[i].smallers += b.length-j; // count smallers!
                all[k] = a[i];
                i++;
            } else {
                all[k] = b[j];
                j++;
            }
            k++;
        }
        while (i < a.length) { all[k++] = a[i++]; }
        while (j < b.length) { 
            all[k++] = b[j++]; 
        }
    }
    
    public static int[] smaller(int[] unsorted) {
        int[] result = new int[unsorted.length];
        Wrapper[] u = new Wrapper[unsorted.length];
        for(int i = 0; i < result.length; i++) {
            u[i] = (new Wrapper(unsorted[i], i));
        }
        sort(u);
        
        for(int i = 0; i < result.length; i++) {
            result[u[i].realIndex] = u[i].smallers;
        }
        
        return result;
    }
}
______________________________________
//import java.util.*;

public class Smaller {
	
	public static int[] smaller(int[] unsorted) {
    int l=unsorted.length;
    int[] sorted=new int[l];
    sorted[l-1]=0;
    int max=0;int min=0;
    for (int i=0;i<l;i++){
      if(unsorted[i]>max)
        max=unsorted[i];
      if(unsorted[i]<min)
        min=unsorted[i];
    }
    int[] arr=new int[max-min+1];
    for (int i=l-1;i>=0;i--){
       arr[unsorted[i]-min]++;
      
      for (int j=unsorted[i]-min-1;j>=0;j--)
        sorted[i]+=arr[j];
    } 
		return sorted ;
	}
}
______________________________________
import java.util.Arrays;
import java.util.TreeMap;

public class Smaller {

	public static int[] smaller(int[] array) {
		int[] counts = new int[array.length];

		Tree tree = new Tree();

		tree.insert(array[array.length - 1]);
		for (int i = array.length - 2; i >= 0; i--) {
			int number = array[i];
			int smallerChildCount = tree.getSmallerChildCount(number);
			counts[i] = smallerChildCount;
			tree.insert(number);
		}


		return counts;
	}

	public static class Tree {

		private Node root;

		static class Node {
			int smallChildrenCount;
			int frequency = 1;
			int value;
			Node left, right;

			Node(int value) {
				this.value = value;
				left = null;
				right = null;
			}
		}

		public void insert(int value) {
			if (root == null) {
				root = new Node(value);
			} else {
				insert(root, value);
			}
		}

		public int getSmallerChildCount(int value) {
			return getSmallerChildCount(root, value);
		}

		private int getSmallerChildCount(Node node, int value) {
			if (value < node.value) {
				if (node.left != null) {
					return getSmallerChildCount(node.left, value);
				} else {
					return 0;
				}
			} else if (value > node.value) {
				if (node.right != null) {
					return node.smallChildrenCount + node.frequency + getSmallerChildCount(node.right, value);
				} else {
					return node.smallChildrenCount + node.frequency;
				}
			} else {
				return node.smallChildrenCount;
			}
		}

		private void insert(Node node, int value) {
			if (value < node.value) {
				node.smallChildrenCount++;
				if (node.left != null) {
					insert(node.left, value);
				} else {
					node.left = new Node(value);
				}
			} else if (value > node.value) {
				if (node.right != null) {
					insert(node.right, value);
				} else {
					node.right = new Node(value);
				}
			} else {
				node.frequency++;
			}
		}
	}
}
