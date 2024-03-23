import cv2
import base64
import uvicorn
import numpy as np

from PIL import Image
from io import BytesIO

from deepface import DeepFace

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from logger import print_log
from database import Database
from communication import Communication

from utils.hex import convert_hex_to_maxtrix_image


class FastAPIApp:
    def __init__(self):
        self.app = FastAPI()

        self.setup()

    def setup(self):
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        self.templates = Jinja2Templates(directory="templates")

        self._define_routes()

    def _define_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            return self.templates.TemplateResponse(
                "index.html", {"request": request}
            )

        @self.app.post("/signup", response_class=JSONResponse)
        async def signup(request: Request):
            print_log("info", "[POST] /signup")

            data = await request.json()

            name = data["name"]
            email = data["email"]

            print_log("info", "Connecting to serial port...")

            communication = Communication()
            communication.connect()

            communication.write("capture-person\r\n")

            print_log("info", "Capture command sent to serial port.")

            while True:
                data = communication.readline()

                if data:
                    if data.startswith("[ERROR]"):
                        error = data.replace("[ERROR] ", "")

                        print_log("error", "Error capturing image.")
                        print_log("error", f"Error: {error}")

                        return JSONResponse(status_code=400, content={"message": error.upper()})

                    matrix_image = convert_hex_to_maxtrix_image(data)
                    matrix_image = np.array(matrix_image, dtype=np.uint8)

                    color_matrix_image = cv2.cvtColor(matrix_image, cv2.COLOR_GRAY2BGR)

                    try:
                        result_deepface = DeepFace.represent(img_path=color_matrix_image, model_name="Facenet512")
                        embedding = result_deepface[0]["embedding"]
                    except ValueError:
                        print_log("error", "No face detected.")

                        return JSONResponse(status_code=400, content={"message": "NO FACE DETECTED!"})

                    database = Database()
                    created = database.create(email, {"name": name, "embeddings": [embedding]})

                    if not created:
                        print_log("error", "User already exists.")

                        return JSONResponse(status_code=400, content={"message": "USER ALREADY EXISTS!"})

                    print_log("info", "User registered successfully.")

                    image = Image.fromarray(color_matrix_image)

                    buffer = BytesIO()
                    image.save(buffer, format="PNG")

                    base64_image = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

                    return JSONResponse(content={"message": "success", "name": name, "image": base64_image})

        @self.app.post("/signin", response_class=JSONResponse)
        async def signin(request: Request):
            print_log("info", "[POST] /signin")

            data = await request.json()

            email = data["email"]

            print_log("info", "Connecting to serial port...")

            communication = Communication()
            communication.connect()

            communication.write("capture-person\r\n")

            print_log("info", "Capture command sent to serial port.")

            while True:
                data = communication.readline()

                if data:
                    if data.startswith("[ERROR]"):
                        error = data.replace("[ERROR] ", "")

                        print_log("error", "Error capturing image.")
                        print_log("error", f"Error: {error}")

                        return JSONResponse(status_code=400, content={"message": error.upper()})

                    matrix_image = convert_hex_to_maxtrix_image(data)
                    matrix_image = np.array(matrix_image, dtype=np.uint8)

                    color_matrix_image = cv2.cvtColor(matrix_image, cv2.COLOR_GRAY2BGR)

                    try:
                        result_deepface = DeepFace.represent(img_path=color_matrix_image, model_name="Facenet512")
                        current_embedding = result_deepface[0]["embedding"]
                    except ValueError:
                        print_log("error", "No face detected.")

                        return JSONResponse(status_code=400, content={"message": "NO FACE DETECTED!"})

                    database = Database()
                    user_data = database.read(email)

                    if not user_data:
                        print_log("error", "User not found.")

                        return JSONResponse(status_code=400, content={"message": "USER NOT IDENTIFIED!"})

                    user_embeddings = user_data["embeddings"]

                    for user_embedding in user_embeddings:
                        result_verify = DeepFace.verify(
                            current_embedding,
                            user_embedding,
                            model_name="Facenet512",
                            distance_metric="euclidean_l2",
                            silent=True
                        )

                        if result_verify["verified"]:
                            print_log("info", "User identified successfully.")
                            print_log("info", "Similarity: {:.4f}".format(result_verify["distance"]))

                            database.update(email, {
                                "name": user_data["name"],
                                "embeddings": user_embeddings + [current_embedding]
                            })

                            image = Image.fromarray(color_matrix_image)

                            buffer = BytesIO()
                            image.save(buffer, format="PNG")

                            base64_image = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

                            return JSONResponse(content={"message": "success", "name": user_data["name"], "image": base64_image})

                    print_log("error", "User not identified.")

                    return JSONResponse(status_code=400, content={"message": "USER NOT IDENTIFIED!"})

        @self.app.post("/capture", response_class=JSONResponse)
        async def capture(request: Request):
            print_log("info", "[POST] /capture")
            print_log("info", "Connecting to serial port...")

            communication = Communication()
            communication.connect()

            communication.write("capture\r\n")

            print_log("info", "Capture command sent to serial port.")

            while True:
                data = communication.readline()

                if data:
                    if data.startswith("[ERROR]"):
                        error = data.replace("[ERROR] ", "")

                        print_log("error", "Error capturing image.")
                        print_log("error", f"Error: {error}")

                        return JSONResponse(status_code=400, content={"message": error.upper()})

                    matrix_image = convert_hex_to_maxtrix_image(data)
                    matrix_image = np.array(matrix_image, dtype=np.uint8)

                    image = Image.fromarray(matrix_image)

                    buffer = BytesIO()
                    image.save(buffer, format="PNG")

                    base64_image = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

                    print_log("info", "Image captured successfully.")

                    return JSONResponse(content={"image": base64_image})


fastapi_app = FastAPIApp().app

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="localhost", port=8000, access_log=False)
