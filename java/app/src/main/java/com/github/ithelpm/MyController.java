package com.github.ithelpm;

import java.io.InputStream;

import org.opencv.core.Mat;

import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.image.ImageView;
import com.github.ithelpm.utils.*;

public class MyController {
    @FXML
    ImageView camera;

    InputStream cameraDataStream;
    @FXML
    Button starter;
    boolean clicked = false;

    @FXML
    void start() {
        Task<Void> refreshImage = new Task<>() {

            @Override
            protected Void call() throws Exception {
                while (clicked) {
                    if(cameraDataStream!=null) {
                        Mat frame = App.decodeData(cameraDataStream);
                        camera.setImage(Utils.mat2Image(frame));
                    }
                }
                return null;
            }

        };
        if (starter.getText() == "start") {
            clicked = true;
            refreshImage.run();
            starter.setText("stop");
        } else {
            clicked = false;
            refreshImage.cancel();
            starter.setText("start");
        }
    }
}