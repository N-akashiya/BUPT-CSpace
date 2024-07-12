package com.javafinal.n;

import org.pcap4j.core.PcapNetworkInterface;
import org.pcap4j.core.Pcaps;

import javax.swing.*;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Controller {
    private UI ui;
    private Capture capture;
    private Thread captureThread;
    private Logger logger;
    private ExecutorService interactExe;

    public Controller(UI ui) {
        this.ui = ui;
        this.logger = Logger.getInstance();
        this.interactExe = Executors.newSingleThreadExecutor(); 
        
        ui.getFilterB().addActionListener(e -> {
            String newFilter = ui.getipField().getText().trim();
            updateFilter(newFilter);
        });
    }

    public void getInterfaceList() {
        try {
            List<PcapNetworkInterface> allDevs = Pcaps.findAllDevs();
            for (PcapNetworkInterface nif : allDevs) {
                ui.getInterfaceSele().addItem(nif.getName() + " - " + nif.getDescription());
            }
        } 
        catch (Exception e) {
            e.printStackTrace();
            logger.logError("Failed to get interfaces: " + e.getMessage());
        }
    }

    public void startCapture() {
        try {
            ui.clrTable(); // CLR
            String selectedInterface = (String) ui.getInterfaceSele().getSelectedItem();
            if (selectedInterface == null) {
                JOptionPane.showMessageDialog(ui.getFrame(), "No interface selected.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            String itf = selectedInterface.split(" - ")[0];
            PcapNetworkInterface nif = Pcaps.getDevByName(itf);
            if (nif == null) {
                JOptionPane.showMessageDialog(ui.getFrame(), "Error: Interface not found.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            String filter = ui.getipField().getText().trim();
            Parser parser = new Parser();

            capture = new Capture(packet -> {
                SwingUtilities.invokeLater(() -> ui.updateTable(packet));
            }, filter, nif, parser);
            captureThread = new Thread(capture);
            captureThread.start();

            ui.getStartB().setEnabled(false);
            ui.getStopB().setEnabled(true);
        } 
        catch (Exception e) {
            e.printStackTrace();
            logger.logError("Failed to start: " + e.getMessage());
        }
    }

    public void stopCapture() {
        if (capture != null) {
            capture.stop();
            try {
                captureThread.join(); // 等待线程结束
            } 
            catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.logError("Failed to stop: " + e.getMessage());
            }
            capture = null;
            captureThread = null;
        }
        ui.getStartB().setEnabled(true);
        ui.getStopB().setEnabled(false);
    }

    public void updateFilter(String newfilter) {
        interactExe.submit(() -> {
            if (capture != null) {
                capture.setFilter(newfilter);
                List<String> allPkts = capture.getCapturedPackets();
                SwingUtilities.invokeLater(() -> {
                    ui.clrTable();
                    for (String packet : allPkts) {
                        if (packet.contains(newfilter)) {
                            ui.updateTable(packet);
                        }
                    }
                });
            }
        });
    }

    public Capture getCapture() {
        return capture;
    }
}