package com.github.ithelpm;

import java.io.IOException;
import java.io.InputStream;
import java.net.*;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;

public class App extends Application {
    public static void main(String[] args) {
        launch(args);
    }

    public static InputStream receiveData() {
        Receiver tunnel;
        try {
            tunnel = new Receiver(
                new ServerSocket(8080, 100, InetAddress.getByName("localhost")));
            return tunnel.getSocket().getInputStream();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        
    }
}

class Receiver {
    private Socket socket;
    public Receiver(ServerSocket socket) {
        this.connect(socket);
    }

    private void connect(ServerSocket sock) {
        try {
            this.socket = sock.accept();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public Socket getSocket() {
        return this.socket;
    }
}
