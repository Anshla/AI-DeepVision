# Deep Vision Crowd Monitor

Deep Vision Crowd Monitor is an AI-based crowd density estimation system designed for **image-level crowd analysis**.  
The project uses deep learning models to estimate crowd count, visualize density distribution, and trigger **email alerts** when predefined thresholds are exceeded.

This system currently supports **single image uploads** and is optimized for **dense crowd scenarios**.

---

## Key Features

### Image-Based Crowd Density Estimation
- Upload single crowd images (JPG, PNG formats)
- Accurate crowd counting using CSRNet
- Density map generation for visual interpretation
- Designed for dense and highly populated scenes

### Hybrid Model Strategy
- CSRNet for density-based crowd estimation
- YOLOv8 for person detection in sparse scenes
- Automatic selection based on estimated crowd density

### Email Alert System
- Threshold-based alert mechanism
- Email notifications when crowd count exceeds limits
- Snapshot of the processed image included in alerts
- Cooldown interval to prevent repeated notifications

### Visualization
- Density heatmap output
- Total estimated crowd count display
- Minimal and user-friendly Streamlit interface

---

## System Requirements
- Python 3.8 or higher
- pip package manager

---

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/GKSJ-Deepvision/AI-DeepVision.git
cd AI-DeepVision



### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download Trained Model

Download the trained CSRNet model file and place it in the project root directory:

```text
best_csrnet_partB.pth```

---

## Running the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```
---

## Workflow Overview
1. User uploads a crowd image  
2. Image is preprocessed and passed to the model  
3. Crowd density map is generated  
4. Total crowd count is calculated  
5. Email alert is triggered if the threshold is exceeded  

---

## Models Used

### CSRNet
- Density-based crowd estimation model  
- VGG16 front-end with dilated convolution back-end  
- Suitable for dense crowd scenes  

### YOLOv8
- Object detection model  
- Used for sparse crowd estimation  
- Detects individual persons  

---

## Email Alert Configuration (Optional)

Create the following file:
```text
.streamlit/secrets.toml

```
Add SMTP configuration:
```toml
[smtp]
server = "smtp.gmail.com"
port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```
---

## Project Structure
```text
AI-DeepVision/
├── app.py
├── best_csrnet_partB.pth
├── requirements.txt
├── README.md
```
---

## Future Scope
```text
- Video-based crowd analysis
- Live webcam crowd monitoring
- Advanced analytics and reporting features
