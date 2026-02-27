import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import urllib.request

# Load pretrained ResNet model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

# Download ImageNet labels (only first time)
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
urllib.request.urlretrieve(LABELS_URL, "imagenet_classes.txt")

with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

# Image transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def detect_landmark(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)

    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    top_probs, top_catids = torch.topk(probabilities, 5)

    results = []
    for prob, catid in zip(top_probs, top_catids):
        results.append((labels[catid.item()], round(prob.item()*100, 2)))

    return results


if __name__ == "__main__":
    predictions = detect_landmark("test.jpg")
    print("\nTop 5 Predictions:")
    for label, confidence in predictions:
        print(f"{label} — {confidence}%")