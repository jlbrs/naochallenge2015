import com.aldebaran.qimessaging.Application;
import com.aldebaran.qimessaging.Object;
import com.aldebaran.qimessaging.Session;

public class ReactToEvents {

	public static class CallBackFunctions {
		// Define a function to be called when events occur
		public void onEvent(java.lang.Object value) {
			System.out.println("Event occured!");
		}
	}

	public static void main(String[] args) throws Exception {

		// Just here to setup everything correctly
		Application application = new Application(args);

		// Connect to the robot
		Session session = new Session("tcp://nao.local:9559");

		// Link to the ALMemory module
		Object memory = session.service("ALMemory");
		
		// Get a subscription to the event
		Object subscription = memory.<Object>call("subscribe","frontTactileTouched").get();
		
		// Instantiate the callback functions class
		CallBackFunctions myCallbackFunctions = new CallBackFunctions();

		// Link the callback function to the event subscribed		
		// you need to describe the type of arguments. m = any type
		subscription.connect("signal::(m)", "onFallen::(m)", myCallbackFunctions);

		// Infinite loop that does nothing
		application.run();
	}
}