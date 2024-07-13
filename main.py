import streamlit as st
import pyqrcode
from io import BytesIO
from PIL import Image
import cv2
import av
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
from streamlit_webrtc import webrtc_streamer
from pyzbar.pyzbar import decode
from streamlit_webrtc import (webrtc_streamer, VideoProcessorBase,WebRtcMode)

def live_detection(play_state):

   class BarcodeProcessor(VideoProcessorBase):

      def __init__(self) -> None:
         self.barcode_val = False
      
      def BarcodeReader(self, image):
         detectedBarcodes = decode(image)
         if not detectedBarcodes:
            print("\n No barcode! \n")
            return image, False

         else:
            for barcode in detectedBarcodes: 
               (x, y, w, h) = barcode.rect
               cv2.rectangle(image, (x-10, y-10),
                              (x + w+10, y + h+10),
                              (0, 255, 0), 2)

            if detectedBarcodes[0] != "":
               return image, detectedBarcodes[0]


      def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
         image = frame.to_ndarray(format="bgr24")

         annotated_image, result = self.BarcodeReader(image)
        
         if result == False:
            return av.VideoFrame.from_ndarray(image, format="bgr24")

         else:

            self.barcode_val = result[0]
            play_state = False
            return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

   stream = webrtc_streamer(
         key="barcode-detection",
         mode=WebRtcMode.SENDRECV,
         desired_playing_state=play_state,
         video_processor_factory=BarcodeProcessor,
         media_stream_constraints={"video": True, "audio": False},
         async_processing=True,
      )

def video_frame_callback(frame):
    print(111222)
    st.title("hello world #1")
    qr_codes = decode_qr_code(frame)
    print(22222)
    stframe = st.empty()
    # Display the frame
    st.write('hello world #2')
    stframe.image(frame, channels="BGR")

    # Display the decoded QR codes if it's a new message
    if qr_codes:
        st.write(qr_codes)
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:]

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
def decode_qr_code(frame):
    """
    Decodes QR codes in the given image frame.

    Parameters:
    frame (numpy.ndarray): The image frame to scan for QR codes.

    Returns:
    list: A list of decoded QR code data.
    """
    decoded_objects = pyzbar.decode(frame)
    qr_codes = [obj.data.decode('utf-8') for obj in decoded_objects]
    return qr_codes

def create_qr_code():
    st.title("QR Code Generator")
    data = st.text_input("Enter the data to encode in the QR code")  # input by user

    if data:
        qr_image = generate_qr_code(data)    # function generate_qr_code with data as argument
        img = Image.open(qr_image)

        st.image(img, caption="Generated QR Code", use_column_width=False)

        st.download_button(
            label="Download QR Code",
            data=qr_image,
            file_name="qrcode.png",
            mime="image/png"
        )

def scan_qr_code():
    st.title("QR Code Scanner")
    st.write("Click the button below to start the camera and scan a QR code.")

    # Initialize session state for control buttons and decoded message
    if "scanning" not in st.session_state:
        st.session_state.scanning = False

    if "decoded_message" not in st.session_state:
        st.session_state.decoded_message = None

    def start_scanning():
        st.session_state.scanning = True

    def stop_scanning():
        st.session_state.scanning = False

    if not st.session_state.scanning:
        if st.button('Start Scanning', key='start'):
            start_scanning()
    st.write('hello world')
    if st.session_state.scanning:
        detected_barcode = live_detection(True)

st.title("QR Code Toolkit")

option = st.radio(
    "Choose an option:",
    ("Create QR", "Scan QR")
)

if option == "Create QR":
    create_qr_code()
elif option == "Scan QR":
    scan_qr_code()

