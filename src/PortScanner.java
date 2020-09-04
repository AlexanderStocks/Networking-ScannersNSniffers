
import java.io.IOException;
import java.net.*;

public class PortScanner {

  private static final int TIMEOUT = 200;

  private int lowerPort = 0;
  private int higherPort = 0;

  private boolean includeClosedPort = false;

  private String ipAddress = "";

  public static void main(String[] args) {
    //instructions here
    PortScanner scan = new PortScanner("8.8.8.8", 1, 150, true);
    scan.startScan();
  }

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

  public int getLowerPort() {
    return lowerPort;
  }

  public int getHigherPort() {
    return higherPort;
  }

  public String getIpAddress() {
    return ipAddress;
  }

  public void setLowerPort(int lowerPort) {
    this.lowerPort = lowerPort;
  }

  public void setHigherPort(int higherPort) {
    this.higherPort = higherPort;
  }

  public void setIpAddress(String ipAddress) {
    this.ipAddress = ipAddress;
  }

  public void setIncludeClosedPort(boolean includeClosedPort) {
    this.includeClosedPort = includeClosedPort;
  }
}

