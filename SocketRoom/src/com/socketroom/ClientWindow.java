package com.socketroom;

import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.SwingConstants;
import javax.swing.UIManager;
import javax.swing.border.BevelBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.text.Document;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;

import org.eclipse.wb.swing.FocusTraversalOnArray;

public class ClientWindow extends JFrame implements Runnable{
	
	private JPanel contentPane;
	private JPasswordField txtChatPass;
	private static JTextField txtName;
	@SuppressWarnings("rawtypes")
	private JComboBox txtColor;
	private static JTextPane txtChatBox;
	private static boolean connected = false;
	
	private static String Name;
	private static String Ucolor;
	private static String ChatPass;
	private JTextField txtPort;
	
	private static int Port;
	public final static String address = "localhost";
	private InetAddress ip;
	
	private Client client;
	
	private boolean running = true;
	private Thread Recieve, run;
	
	public ClientWindow(){
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			e.printStackTrace();
		} 
		
		setName("frmClient");
		setTitle("Socket Chat Login");
		setResizable(false);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 570, 466);
		contentPane = new JPanel();
		contentPane.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblChatRoom = new JLabel("Chat History");
		lblChatRoom.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblChatRoom.setBounds(6, 6, 77, 21);
		contentPane.add(lblChatRoom);
		
		txtChatBox = new JTextPane();
		txtChatBox.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		JScrollPane scrollChat = new JScrollPane(txtChatBox);
		scrollChat.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		scrollChat.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		txtChatBox.setEditable(false);
		scrollChat.setBounds(6, 28, 367, 253);
		contentPane.add(scrollChat);
		
		JLabel lblMessage = new JLabel("Message");
		lblMessage.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblMessage.setBounds(6, 281, 60, 21);
		contentPane.add(lblMessage);
		
		JTextArea txtMessage = new JTextArea();
		txtMessage.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		JScrollPane scrollMes = new JScrollPane(txtMessage);
		txtMessage.setWrapStyleWord(true);
		txtMessage.setLineWrap(true);
		/*txtMessage.addKeyListener(new KeyAdapter() {
			public void keyPressed(KeyEvent e) {
				if(e.getKeyCode() == KeyEvent.VK_ENTER){
					send(txtMessage.getText());
					if(connected){
						txtMessage.setText("");
					}
				}
			}
		});*/
		scrollMes.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		scrollMes.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		scrollMes.setBounds(6, 300, 367, 106);
		contentPane.add(scrollMes);

		JLabel lblNewLabel = new JLabel("Users\n");
		lblNewLabel.setVerticalAlignment(SwingConstants.TOP);
		lblNewLabel.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblNewLabel.setBounds(385, 9, 42, 21);
		contentPane.add(lblNewLabel);
		JScrollPane scrollUsers = new JScrollPane();
		scrollUsers.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		scrollUsers.setBounds(383, 28, 181, 244);
		contentPane.add(scrollUsers);
		
		JLabel lblNewLabel_2 = new JLabel("Chat Port:");
		lblNewLabel_2.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblNewLabel_2.setBounds(385, 281, 77, 21);
		contentPane.add(lblNewLabel_2);
		
		JLabel lblName = new JLabel("Name: ");
		lblName.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblName.setBounds(385, 352, 42, 21);
		contentPane.add(lblName);
		
		JLabel lblColor = new JLabel("Name Color:");
		lblColor.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblColor.setBounds(385, 382, 69, 21);
		contentPane.add(lblColor);
		
		JLabel lblChatPassword = new JLabel("Chat Password:");
		lblChatPassword.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		lblChatPassword.setBounds(385, 314, 106, 21);
		contentPane.add(lblChatPassword);
		
		txtChatPass = new JPasswordField();
		txtChatPass.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		txtChatPass.setBounds(470, 310, 94, 28);
		contentPane.add(txtChatPass);
		txtChatPass.setColumns(10);
		
		txtName = new JTextField();
		txtName.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		txtName.setColumns(10);
		txtName.setBounds(421, 350, 143, 28);
		contentPane.add(txtName);
		
		txtColor = new JComboBox();
		txtColor.setModel(new DefaultComboBoxModel(new String[] {"Black", "Blue", "Cyan", "Dark Gray", "Gray", "Green", "Yellow", "Light Gray", "Magenta", "Orange", "Pink", "Red"}));
		txtColor.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		txtColor.setBounds(458, 378, 106, 28);
		contentPane.add(txtColor);
		
		JButton btnMessage = new JButton("Send Message");
		btnMessage.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				String mes = txtMessage.getText();
				if(!(mes.equals(""))){
					client.send(mes.replaceAll("\n", " ").getBytes());
				}else{
					return;
				}
				if(connected){
					txtMessage.setText("");
				}
			}
		});
		btnMessage.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		btnMessage.setBounds(0, 411, 117, 29);
		contentPane.add(btnMessage);
		
		JButton btnConnect = new JButton("Connect\n");
		btnConnect.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(!connected){
					txtChatBox.setText("");
					try{
						Port = Integer.parseInt(txtPort.getText());
						client = new Client(Port, ip, address);
						listen();
						connected = connect(txtName.getText(), "" + txtColor.getSelectedItem(), txtChatPass.getText(), Port);
						if(!connected){
							clientMes(String.format("Connection to LocalHost:%s has failed, please try again", Port));
						}
					} catch(Exception exception){
						clientMes("Please enter in a valid port number");
					}	
				}
			}
		});
		btnConnect.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		btnConnect.setBounds(338, 411, 117, 29);
		contentPane.add(btnConnect);
		
		JButton btnDisconnect = new JButton("Disconnect\n");
		btnDisconnect.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				if(connected){
					connected = false;
					Recieve.interrupt();
					txtChatBox.setText("");
					clientMes(String.format("Disconnecting User %s from LocalHost:%s...", Name, Port));
				}
			}
		});
		btnDisconnect.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		btnDisconnect.setBounds(447, 411, 117, 29);
		contentPane.add(btnDisconnect);
		
		JList lstUsers = new JList();
		lstUsers.setBounds(385, 28, 177, 244);
		contentPane.add(lstUsers);
		lstUsers.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		
		txtPort = new JTextField();
		txtPort.setFont(new Font("Lucida Grande", Font.PLAIN, 11));
		txtPort.setBounds(447, 281, 117, 23);
		contentPane.add(txtPort);
		txtPort.setColumns(10);
		contentPane.setFocusTraversalPolicy(new FocusTraversalOnArray(new Component[]{btnMessage, txtMessage, txtChatPass, txtName, txtColor, btnConnect, btnDisconnect}));
		
		run = new Thread(this, "Client");
		run.start();
	}
	public void run(){
		//listen();
	}
	
	private void console(String mes, String name, String color){
		if(connected){
			SimpleAttributeSet set = new SimpleAttributeSet();
			StyleConstants.setBold(set, true);
			StyleConstants.setForeground(set, getColor(color));
			try{
				Document doc = txtChatBox.getDocument();
				doc.insertString(doc.getLength(), name + ": ", set);
				doc.insertString(doc.getLength(), mes+"\n", null);
				}catch(Exception e){
				e.printStackTrace();
			}
		}else{
			clientMes("Please connect to a chat room");
		}
	}
	private boolean connect(String name, String color, String chatPass, int port){
		int num = (int)(Math.random()*9900 + 100);
		if(name.equals("")){
			Name = "Guest" + num ;
		}else{
			Name = name;
		}
		Port = port;
		Ucolor = color;
		ChatPass = chatPass;
		
		clientMes(String.format("Attempting to connect User %s to LocalHost:%s...", Name, port));
		
		return client.openConnection(Name);
	}
	
	public void listen(){
		Recieve = new Thread("Recieve"){
			public void run(){
				System.out.println("Test");
				while(running){	
					System.out.println("I'm Listening");
					String message = client.recieve();
					
					if(message.startsWith("/m/")){
						message = message.substring(3,message.length());
						//System.out.println("ClientMes: " +message);
					}else if(message.startsWith("/c/")){
						client.setID(message.substring(3, message.length()));
						message = ""+client.getID();
						//System.out.println("ClientCon: "+message);
					}else{
						System.out.println(message);
						message = "Error 404: It would seem something is missing";
					}
					console(message, "Ryan", "Blue");
				}
			}
		};
		Recieve.start();
	}
	
	private static void clientMes(String mes){
		SimpleAttributeSet set = new SimpleAttributeSet();
		StyleConstants.setBold(set, true);
		StyleConstants.setForeground(set, Color.black);
		try {
		      Document doc = txtChatBox.getDocument();
		      doc.insertString(doc.getLength(), "Client: ", set);
		      doc.insertString(doc.getLength(), mes+"\n", set);
		   } catch(Exception exc) {
		      exc.printStackTrace();
		   }
	}
	private Color getColor(String color){
		if(color.equals("Black")){
			return Color.black;
		}else if(color.equals("Blue")){
			return Color.blue;
		}else if(color.equals("Cyan")){
			return Color.cyan;
		}else if(color.equals("Dark Gray")){
			return Color.darkGray;
		}else if(color.equals("Gray")){
			return Color.gray;
		}else if(color.equals("Green")){
			return Color.green;
		}else if(color.equals("Yellow")){
			return Color.yellow;
		}else if(color.equals("Light Gray")){
			return Color.lightGray;
		}else if(color.equals("Magenta")){
			return Color.magenta;
		}else if(color.equals("Orange")){
			return Color.orange;
		}else if(color.equals("Pink")){
			return Color.pink;
		}else if(color.equals("Red")){
			return Color.red;
		}else {
			return Color.black;
		}
	}
}
