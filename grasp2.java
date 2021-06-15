import java.util.Scanner; // scan liblery

public class grasp2 { // main function
   

   public static void main (String[] args){ //main function

      Scanner sc = new Scanner(System.in);
      double total_cost = 0;
      double pay = 0;
      
      System.out.print("Please insult restaurant cost : "); 
      int res_cost = sc.nextInt();
      System.out.print("Please insult number of people : ");
      int people = sc.nextInt();
      
      pay = res_cost / people;
      
      if(pay < 20 && pay >= 0) {
         total_cost = (pay * 1.1);
      }
      
      else if(pay >= 20 && pay < 50) {
         total_cost = (pay * 1.15);
      }
      
      else if(pay >= 50) {
         total_cost = (pay * 1.2);
      }
      
      else {
         System.out.print("Please type again\n");
      }
      
      System.out.print("Total cost is " + total_cost);
      
      // Restaurant total cost :
      // number of people : 
      // each people pay < $20 tip 10%
      // pay > 50$ tip 15%
      //else 20%
      // total cost ( tip include)
   
      }
   
}