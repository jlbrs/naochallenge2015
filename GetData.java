import com.aldebaran.qimessaging.Object;
import com.aldebaran.qimessaging.Session;

public class GetData {

	public static void main(String[] args) throws Exception {
		
		// Connect to the robot
		Session session = new Session("tcp://nao.local:9559");
		
		// Create links to NAOqi modules
		Object mem = session.service("ALMemory");
		
		// Call functions from the modules
		String value = mem.<String>call("getData", "myApplication/myData").get();
		System.out.println("Value read from the robot: " + value);
	}	
}
