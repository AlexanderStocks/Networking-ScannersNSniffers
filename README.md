# Networking-ScannersNSniffers
Ther second installment in my networking crusade. Here, I am building scripts that can be quickly thrown together to sniff, view and decode network traffic. By doing this I hope to both gain an understanding of the building blocks of how network packets are sent and recieved, while also gaining a true appreciation for the much larger tools such as Wireshark.

Again, I will be using socket to access the lower-level networking information, but this time I will be accessing the IP and ICMP headers. I will be using these to identify which hosts are active at a particular IP address by using the known behaviour of operating systems when handing closed UDP ports.

I chose UDP because there is no overhead when sending lots of messages across the subnet while waiting for a response, which simplifies my scanner so I can focus on decoding and analysing the netowrk protocol headers.
