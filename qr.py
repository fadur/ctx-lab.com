# /// script
# dependencies = [
#     "qrcode",
#     "pillow"
# ]
# ///
import qrcode

# Generate and save the QR code
img = qrcode.make("https://ctx-lab.com")
img.save("qrcode.png")
print("QR code saved as qrcode.png")
