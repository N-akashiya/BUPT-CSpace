package com.javafinal.n;

import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Logger {
    private static Logger instance;
    private static final String LOG_FILE = "debug.log";

    private Logger() {}

    public static synchronized Logger getInstance() {
        if (instance == null) {
            clrLog();
            instance = new Logger();
        }
        return instance;
    }

    public void log(String message) {
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String currentTime = LocalDateTime.now().format(dtf);
        String logEntry = currentTime + " " + message;
        try (FileWriter fw = new FileWriter(LOG_FILE, true)) {
            fw.write(logEntry + "\n");
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void logPacketInfo(String packetInfo) {
        log("Packet Info: " + packetInfo);
    }

    public void logError(String errorMessage) {
        log("Error: " + errorMessage);
    }

    private static void clrLog() {
        try (FileWriter fw = new FileWriter(LOG_FILE, false)) {
            fw.write("");
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}