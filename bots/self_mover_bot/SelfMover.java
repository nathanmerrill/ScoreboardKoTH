import java.util.Scanner;

public class SelfMover {

    private Scanner stdIn;
    private final int id, name;
    private int position;
    
    public static void main(String[] args) {
        new SelfMover();
    }

    public SelfMover() {
        stdIn = new Scanner(System.in);
        Integer[] data = getData();
        id = data[0];
        position = data[1];
        name = data[2];
        mainLoop();
    }
    private void mainLoop() {
        while(true){
            Integer[] data = getData();
            if (data.length == 1){
                return;
            } else if (data.length == 2){
                switched(data[0], data[1]);
            } else {
                System.out.println(callID(data));
            }        
        }
    }
    private Integer[] getData(){
        String data = stdIn.nextLine().trim();
        if (data.equals("0")){
            System.exit(0);
        }
        String[] strData = data.split(",");
        Integer[] intData = new Integer[strData.length];
        for (int i = 0; i < strData.length; i++){
            intData[i] = Integer.parseInt(strData[i]);
        }
        return intData;
    }
    private void switched(int switcher, int newPosition){
        position = newPosition;
    }
    private int callID(Integer[] players){
        return id;
    }
        
}