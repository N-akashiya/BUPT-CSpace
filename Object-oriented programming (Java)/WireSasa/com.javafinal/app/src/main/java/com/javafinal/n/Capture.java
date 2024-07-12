package com.javafinal.n;

import org.pcap4j.core.PcapHandle;
import org.pcap4j.core.PcapNetworkInterface;
import org.pcap4j.packet.Packet;

import java.util.*;
import java.util.regex.Pattern;

public class Capture implements Runnable {
    private volatile boolean running = false; // 控制捕获线程的运行状态
    private final PacketHandler handler; // 处理器
    private final PcapNetworkInterface nif; // 网卡
    private final Parser parser;
    private final Logger logger;
    private String filterIp;
    private final Object lock = new Object(); // 同步filterIp的读写
    private List<String> capturedPackets = Collections.synchronizedList(new ArrayList<>()); // 存储数据包

    public Capture(PacketHandler handler, String filterIp, PcapNetworkInterface nif, Parser parser) {
        this.handler = handler;
        this.nif = nif;
        this.parser = parser;
        this.logger = Logger.getInstance();
        setFilter(filterIp);
    }

    @Override
    public void run() {
        running = true;
        int snaplen = 65536; // 包的最大长度
        int timeout = 100; // ms

        try (PcapHandle handle = nif.openLive(snaplen, PcapNetworkInterface.PromiscuousMode.PROMISCUOUS, timeout)) {
            while (running) {
                Packet packet = handle.getNextPacket();
                if (packet != null) {
                    String packetInfo = parser.parsePacket(packet);
                    String curFilter;
                    capturedPackets.add(packetInfo);
                    synchronized (lock) {
                        curFilter = this.filterIp;
                    }
                    if (curFilter.isEmpty() || packetInfo.contains(curFilter)) {
                        handler.handle(packetInfo);
                        logger.logPacketInfo(packetInfo);
                    }
                }
            }
        } 
        catch (Exception e) {
            handler.handle("Error: " + e.getMessage());
            logger.log("Error: " + e.getMessage());
        }
    }

    public void stop() {
        running = false;
    }

    public List<String> getCapturedPackets() {
        return new ArrayList<>(capturedPackets);
    }

    public void setFilter(String filter) {
        // 正则表达式判定合法IP格式
        if (filter.isEmpty() || Pattern.matches("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", filter)) {
            synchronized (lock) {
                this.filterIp = filter;
                if(filter.isEmpty())
                    logger.log("No Filter");
                else
                    logger.log("Filter: " + filter);
            }
        }
    }

    @FunctionalInterface
    public interface PacketHandler {
        void handle(String packet); // 定义处理数据包
    }
}