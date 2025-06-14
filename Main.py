from ultralytics import YOLO
from Configurations.MqttConfig import PublishMessage
from Configurations.LogConfig import gerar_pdf
from datetime import datetime
from Configurations.LiveConfig import app

model = YOLO("./MachineLearningTraining/runs/detect/train2/weights/best.pt")
    
def main ():
    for result in model.predict(source="0", show=True, stream=True):
        caixa_errada = False

        for box in result.boxes:
            cls = int(box.cls[0])
            if model.names[cls] == "caixa errada":
                caixa_errada = True
                break

        if caixa_errada:
            frame = result.orig_img
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            descricao = f"Caixa errada detectada em {timestamp}"
            gerar_pdf(frame, descricao)
            PublishMessage("1")
        else:
            PublishMessage("0")

main()