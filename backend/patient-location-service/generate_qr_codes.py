import qrcode
import json
import os

# Create a directory for QR codes if it doesn't exist
if not os.path.exists('qr_codes'):
    os.makedirs('qr_codes')

# Room data template
room_data_template = {
    "room_number": None,
    #"floor": "1",
    #"wing": "A",
    #"type": "patient_room"
}

# Generate QR codes for rooms 1-8
for room_number in range(1, 9):
    # Create room data
    room_data = room_data_template.copy()
    room_data["room_number"] = str(room_number)
    
    # Convert data to JSON string
    qr_data = json.dumps(room_data)
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create image from QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code image
    filename = f'qr_codes/room_{room_number}_qr.png'
    qr_image.save(filename)
    
    print(f"Generated QR code for Room {room_number}: {filename}")

print("\nAll QR codes have been generated successfully!") 