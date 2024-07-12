package com.javafinal.n;

import org.pcap4j.packet.*;

import java.time.*;

public class Parser {
    private int pktCount = 0;
    private LocalDateTime startTimestamp = null;

    public String parsePacket(Packet packet) {
        if (startTimestamp == null)
            startTimestamp = LocalDateTime.now(); // 第一个数据包的时间戳

        StringBuilder strb = new StringBuilder();
        LocalDateTime timestamp = LocalDateTime.now();
        Duration dur = Duration.between(startTimestamp, timestamp);
        double sec = dur.toNanos() / 1_000_000_000.0;

        String srcIp = "", dstIp = "", protocol = "Unknown";
        int len = packet.length();

        // 网络层
        if (packet.contains(IpV4Packet.class)) {
            IpV4Packet IPv4pkt = packet.get(IpV4Packet.class);
            srcIp = IPv4pkt.getHeader().getSrcAddr().getHostAddress();
            dstIp = IPv4pkt.getHeader().getDstAddr().getHostAddress();
            protocol = IPv4pkt.getHeader().getProtocol().name();
        } 
        else if (packet.contains(IpV6Packet.class)) {
            IpV6Packet IPv6pkt = packet.get(IpV6Packet.class);
            srcIp = IPv6pkt.getHeader().getSrcAddr().getHostAddress();
            dstIp = IPv6pkt.getHeader().getDstAddr().getHostAddress();
            protocol = IPv6pkt.getHeader().getNextHeader().name();
        }
        // 传输层
        if (packet.contains(TcpPacket.class)) {
            protocol = "TCP";
        } 
        else if (packet.contains(UdpPacket.class)) {
            protocol = "UDP";
        }

        strb.append(++pktCount).append(",")
                .append(String.format("%.6f", sec)).append(",")
                .append(srcIp).append(",")
                .append(dstIp).append(",")
                .append(protocol).append(",")
                .append(len);

        return strb.toString();
    }
}