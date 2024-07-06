from app.api.v1.base import RestController

class VectoriseRestController(RestController):
    def register_routes(self):
        @self.router.get("/")
        async def vectorise():
            return {"message": "Vectorise API"}
