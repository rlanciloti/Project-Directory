package com.socketroom.server;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class Server implements Runnable{
	private DatagramSocket socket;
	private List<ServerClient> clients = new ArrayList<ServerClient>();
	
	public int port;
	public String password;
	
	private boolean running = true;
	private Thread run, manage, send, recieve;
	
	public Server(int port, String password){
		this.port = port;
		this.password = password;
		
		try {
			socket = new DatagramSocket(port);
		} catch (SocketException e) {
			e.printStackTrace();
		}
		run = new Thread(this, "Server");
		run.start();
	}
	public void run() {
		running = true;
		System.out.println("Server started on port: "+port);
		manageClients();
		recieve();
	}
	private void manageClients(){
		manage = new Thread("Manage"){
			public void run(){
				while(running){
					
				}
			}
		};
		manage.start();
	}
	private void recieve(){
		recieve = new Thread("Recieve"){
			public void run(){
				while(running){
					byte[] data = new byte[1024];
					DatagramPacket packet = new DatagramPacket(data, data.length);
					try {
						socket.receive(packet);
					} catch (IOException e) {
						e.printStackTrace();
					}
					process(packet);
					//System.out.println(clients.get(0).ip.toString() + ":" + clients.get(0).port);
				}
			}
		};
		recieve.start();
	}
	private void sendToAll(String string){
		for(int i = 0; i < clients.size(); i++){
			ServerClient client = clients.get(i);
			send(string.getBytes(), client.ip, client.port);
			//System.out.println("Send To All method: " + string + " ID: "+ client.getID());
		}
	}
	private void send(final byte[] data, final InetAddress ip, final int port){
		send = new Thread("Send"){
			public void run(){
				DatagramPacket packet = new DatagramPacket(data, data.length, ip, port);
				
				try{
					socket.send(packet);
				}catch(Exception e){
					System.out.println(e);
				}
			}
		};
		send.start();
	}
	private void process(DatagramPacket packet){
		String string = new String(packet.getData());
		//System.out.println("Process: "+string);
		if(string.startsWith("/c/")){
			UUID id = UUID.randomUUID();
			clients.add(new ServerClient(string.substring(3, string.length()), packet.getAddress(), packet.getPort(), id.toString()));
			//System.out.println("Client: "+ clients.get(0));
			//String ID = "/c/ID: "+ id.toString();
			//send(ID.getBytes(), packet.getAddress(), packet.getPort());
		} else if(string.startsWith("/m/")) {
			sendToAll(string);
			System.out.println(string.substring(3, string.length()));
		}
	}
}
