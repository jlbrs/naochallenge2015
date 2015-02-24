import com.aldebaran.qimessaging.Object;
import com.aldebaran.qimessaging.Session;

public class DoThings {

	public static void main(String[] args) throws Exception {
		
		// Connect to the robot
		Session session = new Session("tcp://nao.local:9559");
		
		// Create links to NAOqi modules
		Object tts = session.service("ALTextToSpeech");
		Object motion = session.service("ALMotion");
		
		// Call functions from the modules
		tts.call("say", "Hello, world!").get();
		motion.call("moveTo", 1.0f, 0.0f, 0.0f).get();
	}	
}