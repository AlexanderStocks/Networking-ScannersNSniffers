
import java.net.*;

public class PortScanner {

  private static final int TIMEOUT = 200;

  private int lowerPort = 0;
  private int higherPort = 0;

  private boolean includeClosedPort = false;

  private String ipAddress = "";

  public PortScanner(String ipAddress, int portNum) {
    this.ipAddress = ipAddress;
    this.higherPort = portNum;
    this.lowerPort = portNum;
  }

  public PortScanner(String ipAddress, int lowerPort, int higherPort) {
    this.higherPort = higherPort;
    this.lowerPort = lowerPort;
    this.ipAddress = ipAddress;
  }

  public PortScanner(String ipAddress, int lowerPort, int higherPort, boolean includeClosedPort) {
    this.ipAddress = ipAddress;


  }



}

