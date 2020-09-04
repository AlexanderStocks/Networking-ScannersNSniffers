
import java.io.IOException;
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

  public void startScan() {
    for (int i = 0; i <= higherPort; i++) {
      boolean portState = isPortOpen(ipAddress, i);

      if (portState) {
        System.out.println("Port: " + i + " is open.");
      } else if (includeClosedPort) {
        System.out.println("Port: " + i + " is open.");
      }
    }
  }

  public boolean isPortOpen(String ipAddress, int portNum) {
    try {
      Socket socket = new Socket();
      socket.connect(new InetSocketAddress(ipAddress, portNum), TIMEOUT);
      socket.close();
    } catch (IOException e) {
      return false;
    }
    return true;
  }





}

