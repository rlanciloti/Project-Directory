package com.socketroom;

//import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;

import java.awt.Font;

import javax.swing.SwingConstants;
import javax.swing.border.BevelBorder;
import javax.swing.text.Document;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.JComboBox;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTextArea;
import javax.swing.JList;
import javax.swing.JButton;
import javax.swing.JTextPane;
import javax.swing.UIManager;

import org.eclipse.wb.swing.FocusTraversalOnArray;

import java.awt.Component;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

import javax.swing.DefaultComboBoxModel;

public class Client extends JFrame {

	private static final long serialVersionUID = 1L;

	private int Port;
	private DatagramSocket socket;
	private InetAddress ip;
	private String address;
	private String ID = "";

	private Thread send;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ClientWindow frame = new ClientWindow();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	public Client(int port, InetAddress add, String address){
		this.Port = port;
		this.ip = add;
		this.address = address;
		
		try {
			socket = new DatagramSocket();
			ip = InetAddress.getByName(address);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public String getID(){
		return this.ID;
	}
	public void setID(String id){
		this.ID = id;
	}
	
	public void send(final byte[] data){
		send = new Thread("Send"){
			public void run(){
				DatagramPacket packet = new DatagramPacket(data, data.length, ip, Port);
				try {
					socket.send(packet);
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		};
		send.start();
	}
	public String recieve(){
		byte[] data = new byte[1024];
		DatagramPacket packet = new DatagramPacket(data, data.length);
		try {
			socket.receive(packet);
			String message = new String(packet.getData());
			//System.out.println(message.length());
			return message;
		} catch (Exception e) {
			e.printStackTrace();
			return "";
		}
	}
	public boolean openConnection(String Name){
		String connection = "/c/" + Name;
		send(connection.getBytes());
		connection = "/m/" + Name + " is now connected to the server";
		send(connection.getBytes());
		return true;
	}
}























