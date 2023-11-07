from fastapi import FastAPI, File, UploadFile, HTTPException
from pymongo import MongoClient, collection
from PIL import Image
from io import BytesIO
from starlette.requests import Request
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from bson.objectid import ObjectId

app = FastAPI()

# Allow cross-origin requests (CORS) for the development environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sample"]
image_collection = db["images"]

@app.post("/upload/")
async def upload_image(file: UploadFile):
    # Open and compress the uploaded image
    image_data = await file.read()
    original_image = Image.open(BytesIO(image_data))
    compressed_image_buffer = BytesIO()
    original_image.save(compressed_image_buffer, "JPEG", quality=50)

    # Store the compressed image in MongoDB
    # Store the compressed image in MongoDB with the string representation of _id
    # Store the compressed image in MongoDB
    image_id = image_collection.insert_one({"image": compressed_image_buffer.getvalue()}).inserted_id



    return {"image_id":str(image_id) }

image_id = ("YOUR_OBJECT_ID")

@app.get("/image/{image_id}")
async def get_image(image_id: str):
    print("imageidprint",image_id)
    # Retrieve the compressed image from MongoDB
    image_data = image_collection.find_one({"_id":ObjectId(image_id)})
    print("image_id cheking",image_data)
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")

    if image_data is not None:
        # Access the compressed image data
        compressed_image_data = image_data["image"]
        image_bytes = BytesIO(compressed_image_data)
    

        return StreamingResponse(content=image_bytes, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Image not found")
