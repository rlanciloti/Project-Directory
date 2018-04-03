package com.socketroom.server;

import java.net.InetAddress;

public class ServerClient {
	
	public String name;
	public InetAddress ip;
	public int port;
	private final String ID;
	public int attempt = 0;
	
	public ServerClient(String name, InetAddress ip, int port, final String id){
		this.name = name;
		this.ip = ip;
		this.port = port;
		this.ID = id;
	}
	public String getID(){
		return ID;
	}
}
