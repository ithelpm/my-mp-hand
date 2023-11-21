package com.github.ithelpm;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.*;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {
    public static void main(String[] args) {
        // System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        launch(args);
    }

    public static InputStream receiveData() {
        Receiver tunnel;
        try {
            tunnel = new Receiver(
                new ServerSocket(8080, 100, InetAddress.getByName("localhost")));
            return tunnel.getSocket().getInputStream();
        } catch (IOException e) {
            System.out.println("No input socket!");
            return null;
        }
    }

    public static Mat decodeData(InputStream data) {
        if(data != null) {
            byte[] buffer = new byte[1024*8];
            int bytesRead;
            ByteArrayOutputStream os;
            try {
                os = new ByteArrayOutputStream(data.available());
                while ((bytesRead = data.read(buffer)) != -1) {
                    os.write(buffer, 0, bytesRead);
                }
                data.close();
                Mat encoded = new Mat(1, os.size(), CvType.CV_8U);
                encoded.put(0, 0, os.toByteArray());
                os.close();
                Mat decoded = Imgcodecs.imdecode(encoded, Imgcodecs.IMREAD_UNCHANGED);
                encoded.release();
                return decoded;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        
        URL fxmlLocation = getClass().getClassLoader().getResource("myFXML.fxml");
        System.out.println(fxmlLocation.toString());
        Scene scene = new Scene(
            FXMLLoader.load(fxmlLocation)
        );
        primaryStage.setScene(scene);
        primaryStage.show();
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
