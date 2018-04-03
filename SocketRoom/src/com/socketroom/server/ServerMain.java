package com.socketroom.server;

public class ServerMain {
	
	private static int port;
	private static Server server;
	private static String password;
	
	public ServerMain(int port, String password){
		this.port = port;
		this.password = password;
		//System.out.println(port+"\n"+password);
		server = new Server(port, password);
	}
	
	public static void main(String[] args){
		
		if((args.length > 0 )&& (args[0].equals("-h"))){
			System.out.println("Usage: java -jar SocketRoomServer.jar (8192)[port] (\"Password\")[password] (\"Socket Room\")");
			return;
		}else if(args.length == 0){
			port = 8192;
			password = "";
		}else if(args.length == 1){
			try{
				port = Integer.parseInt(args[0]);
			}catch(Exception e){
				System.out.println("Argument port must be of type \"Integer\"");
				return;
			}
		}else if(args.length == 2){
			try{
				port = Integer.parseInt(args[0]);
			}catch(Exception e){
				System.out.println("Argument port must be of type \"Integer\"");
				return;
			}
			password = args[1];
		}else{
			System.out.println("Usage: java -jar SocketRoomServer.jar (integer)[port] (string)[password]");
			return;
		}
		new ServerMain(port, password);
	}
}
