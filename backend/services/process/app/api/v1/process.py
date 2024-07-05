from app.api.v1.base import RestController


class ProcessController(RestController):
    def register_routes(self):
        @self.router.get("/")
        async def vectorise():
            return {"message": "Process API"}
