class AppBaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

#PDF Error
class PDFProcessingError(AppBaseException):
    def __init__(self, message: str = "Failed to process PDF file"):
        super().__init__(message , status_code=422)

#Vector Stor Error
class VectorStoreError(AppBaseException):
    def __init__(self, message: str = "Vector store operation failed"):
        super().__init__(message, status_code = 500)

#Company id Error
class CompanyNotFoundError(AppBaseException):
    def __init__(self, company_id: str):
        super().__init__(
            f"Company with id '{company_id}' not found",
            status_code=404 
        )

#LLM Error
class LLMError(AppBaseException):
    def __init__(self, message: str = "LLM service is unavailable"):
        super().__init__(message, status_code = 503)

#Answer not found in document Error
class NoAnswerFoundError(AppBaseException):
    def __init__(self):
        super().__init__(
            "I could not find an answer in the provided documents.",
            status_code = 404
        )