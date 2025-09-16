/* Name: Julian Jaramillo
 * Class: CS1450
 * Description:
 * Learning to create and manipulate a linked list.
 */

//Imports
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.LinkedList;
import java.util.Queue;


public class JaramilloJulianAssignment10 {

	public static void main(String[] args) throws FileNotFoundException{
		// TODO Auto-generated method stub

		//Instance of binary tree class
		BinaryTree binaryTree = new BinaryTree();
		
		
		//Files
	    //File parrotsTestTxT = new File("parrotsTest.txt");
	    File parrotsTxT = new File("Parrots.txt");

        //Scanner reader1 = new Scanner(parrotsTestTxT);
	    Scanner reader1 = new Scanner(parrotsTxT);
		
	    while(reader1.hasNext()) {
	    	//read from file
	    	int id = reader1.nextInt();
	    	String name = reader1.next();
	    	String songword = reader1.next();

	    	//create/ add destination to binaryTree
	    	Parrot parrot = new Parrot(id, name, songword);
	    	binaryTree.insert(parrot);
	    }
	    
	    //Traversing the binary tree in level order
	    System.out.println("Parrot's Song\n-----------");
	    binaryTree.levelOrder();
	    
	    //Visiting the leaf nodes
	    System.out.println("\n\nParrots on Leaf Nodes\n-------------");
	    binaryTree.visitLeaves();
	}

}

//parrot class
class Parrot{
	
	//private data fields
	private int id;
	private String name;
	private String songWord;
	
	//constructor to initialize private data fields
	public Parrot(int id, String name, String songWord) {
		
		this.id = id;
		this.name = name;
		this.songWord = songWord;
	}
	
	//getter for name
	public String getName(){
		
		return name;
	}
	
	//Gets the parrots songWord
	public String sing() {
		
		return songWord;
	}
	//Comparing parrot Ids for the tree
	public int compareTo(Parrot otherParrot) {
		
		if (this.id < otherParrot.id) {
			return -1;
	    }
		else if (this.id > otherParrot.id) {
			return 1;
		}
	    else {
	    	return 0;
		}
		
	}
}//Parrot classs


//implements Comparable<BinaryTree>
class BinaryTree {
	
	//Instance variable that represents the top of the tree
	private TreeNode root;
	
	//Initializing the tree to an empty tree
	public BinaryTree() {
		
		root = null;
	}
	
	//Insets a new value into the tree
	public boolean insert(Parrot parrotToAdd) {
		
		if(root == null) {
			
			root = new TreeNode(parrotToAdd);
		}
		
		else {
			
			//Locate parent for new node
			TreeNode parent = null;
			TreeNode current = root;
			
			//While haven't reached bottom of tree
			while(current != null) {
				
				if(parrotToAdd.compareTo(current.parrot) < 0) {
					
					//move left
					parent = current;
					current = current.left;
				}
				
				else if(parrotToAdd.compareTo(current.parrot) > 0) {
					
					//Move right
					parent = current;
					current = current.right;
				}
				
				else {
					
					//Found a duplicate node
					return false;
				}
				
			}//While
			
			if(parrotToAdd.compareTo(parent.parrot) < 0) {
				
				parent.left = new TreeNode(parrotToAdd);
			}
			
			else {
				
				parent.right = new TreeNode(parrotToAdd);
			}
		}//else
		
		return true;
	}//Insert
	
	public void levelOrder() {
		
		if(root != null) {
			
			//load queue
			Queue<TreeNode> waitingQ = new LinkedList<>();
			waitingQ.offer(root);
			
			while(!waitingQ.isEmpty()) {
				
				TreeNode tempNode = waitingQ.remove();
				System.out.print(tempNode.parrot.sing()+ " ");
				
				
				//Adding tempNode's left and right children to the queue left first
				if(tempNode.left != null) {
					
					waitingQ.offer(tempNode.left);
				}
				
				if(tempNode.right != null) {
					
					waitingQ.offer(tempNode.right);
				}
			}//while
			
		}//if
	
	}//levelOrder
	
	//Only sending the private recursive method the root
	public void visitLeaves(){
		
		visitLeaves(root);
	}
	
	//recursive helper method
	private void visitLeaves(TreeNode aNode) {
		
		if(aNode != null) {
			
			//if the current node is a leaf print the name
			if(aNode.left == null && aNode.right == null) {
				
				System.out.println(aNode.parrot.getName());
			}
			
			//else keep traversing recursively
			else {
				
				visitLeaves(aNode.left);
				visitLeaves(aNode.right);
			}
		}
	}
	
	private class TreeNode{
		
		private Parrot parrot;
		private TreeNode left;
		private TreeNode right;
		
		public TreeNode(Parrot parrot) {
			this.parrot = parrot;
			this.left = null;
			this.right = null;
			
		}
		
	}//TreeNode
	
}//BinarySearchTree


















