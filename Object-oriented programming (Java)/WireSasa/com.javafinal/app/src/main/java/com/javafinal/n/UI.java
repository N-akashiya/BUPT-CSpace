package com.javafinal.n;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.regex.Pattern;

public class UI {
    private JFrame frame;
    private ImageIcon icon;
    private JComboBox<String> interfaceSele;
    private JTextField ipField;
    private JButton startB, stopB, filterB;
    private JTable packetTable;
    private DefaultTableModel tableModel;
    private Controller ctrl;

    public UI() {
        frame = new JFrame("WireSasa");
        icon = new ImageIcon(getClass().getResource("/icon.png"));
        frame.setIconImage(icon.getImage());
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1200, 800);
        frame.setLayout(new BorderLayout());

        interfaceSele = new JComboBox<>();
        JLabel interfaceLabel = new JLabel("Select Interface:");

        ipField = new JTextField(20);
        JLabel ipLabel = new JLabel("Filter(e.g. 10.3.9.161):");

        startB = new JButton("Start!!");
        stopB = new JButton("Stop!!");
        stopB.setEnabled(false);
        filterB = new JButton("➤");

        JPanel topPanel = new JPanel(new BorderLayout());
        JPanel interactPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        interactPanel.add(interfaceLabel);
        interactPanel.add(interfaceSele);
        interactPanel.add(ipLabel);
        interactPanel.add(ipField);
        interactPanel.add(filterB);
        topPanel.add(interactPanel, BorderLayout.NORTH);
        frame.getContentPane().add(topPanel, BorderLayout.NORTH);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        buttonPanel.add(startB);
        buttonPanel.add(stopB);
        topPanel.add(buttonPanel, BorderLayout.WEST); 

        tableModel = new DefaultTableModel(new Object[]{"No.", "Time", "Source", "Destination", "Protocol", "Length"}, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false; // 禁止编辑
            }
        };
        packetTable = new JTable(tableModel);
        frame.getContentPane().add(new JScrollPane(packetTable), BorderLayout.CENTER);
        
        setCtrlListeners();
    }

    private void setCtrlListeners() {
        ctrl = new Controller(this);
        ctrl.getInterfaceList();
        startB.addActionListener(e -> ctrl.startCapture()); // 监听Start!!触发开始捕获
        stopB.addActionListener(e -> ctrl.stopCapture()); // 监听Stop!!触发停止捕获
        
        ipField.addKeyListener(new KeyAdapter() {
            @Override
            public void keyReleased(KeyEvent e) {
                String inputIP = ipField.getText().trim();
                // 非法输入禁用按钮
                filterB.setEnabled(inputIP.isEmpty() || Pattern.matches("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", inputIP));
            }
        });
    }

    public void clrTable() {
        tableModel.setRowCount(0);
    }

    public JFrame getFrame() {
        return frame;
    }

    public JComboBox<String> getInterfaceSele() {
        return interfaceSele;
    }

    public JTextField getipField() {
        return ipField;
    }

    public JButton getStartB() {
        return startB;
    }

    public JButton getStopB() {
        return stopB;
    }

    public JButton getFilterB() {
        return filterB;
    }
    
    public void updateTable(String packetInfo) {
        String[] parts = packetInfo.split(",");
        tableModel.addRow(parts);
    };

    public void show() {
        frame.setVisible(true);
    }
}